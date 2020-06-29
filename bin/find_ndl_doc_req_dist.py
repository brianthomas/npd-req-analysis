''' 
   Find the Normalized Damerau Levenshtein distance between a PDF document 
   and individual requirements held in a spreadsheet.

   Created on July 5, 2017

   @author: thomas
'''

def _key(index1, index2):
    return str(index1) + '_' + str(index2)

def _get_para_text(p):
    paragraph_txt = ""
    if p:
        paragraph_txt = p.strip()
    return paragraph_txt

def _get_req_text(req):
    req_txt = ""
    if req['content']:
        req_txt = req['content'].strip()
    return req_txt

def find_distance(paragraphs, reqs):
    from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance

    #print("RUNNING on "+str(len(reqs))+" requirements") 
    #print("RUNNING on "+str(len(paragraphs))+" paragraphs") 
    results = {} 
    id_req = 2
    for req in reqs:
        id_paragraph = 1
        for p in paragraphs:
            key = _key(id_req, id_paragraph)
            if key not in results.keys():
 
                req_txt = _get_req_text(req)
                paragraph_txt = _get_para_text(p)

                if req_txt == "" and paragraph_txt == "": 
                    # trivial case, NO text to cross compare
                    pass
                else:
                    # go ahead and calculate our nlp metric
                    results[key] = normalized_damerau_levenshtein_distance(req_txt, paragraph_txt)

            id_paragraph = id_paragraph + 1
        id_req = id_req + 1
             
    return results

def parse_doc_to_paragraphs(doc): 
    import docx

    # open the document 
    document = docx.Document(doc)

    #parse it for paragraphs, capturing metadata about document location they are in
    paragraphs = []

    #count = 0
    for para in document.paragraphs:
        paragraphs.append(para.text)

    return paragraphs

if __name__ == '__main__':
    import argparse
    import operator
    from npd.parser import parse 

    # Use nargs to specify how many arguments an option should take.
    ap = argparse.ArgumentParser(description='XLSM requirements db loader')
    ap.add_argument('-d', '--doc', type=str, help='Name of the document (NPR/NPD) we want to compare to requirements')
    ap.add_argument('-r', '--reqs', type=str, help='Name of the Excel file which holds the data')
    ap.add_argument('-i', '--include_text', type=bool, default=False, help='Whether to include matching doc text in results')
    ap.add_argument('-X', '--excel', type=bool, default=False, help='Whether req file is in Excel format')

    # parse argv
    opts = ap.parse_args()

    if not opts.doc:
        print ("the --doc <file> parameter must be specified")
        ap.print_usage()
        exit()

    if not opts.reqs:
        print ("the --reqs <file> parameter must be specified")
        ap.print_usage()
        exit()

    reqs = []
    if opts.excel:
        reqs = parse(opts.reqs)
    else:
        with open(opts.reqs, 'r') as f:
            for item in f.readlines():
                reqs.append({'content':item}) 

    # load/parse paragraphs from document
    paragraphs = parse_doc_to_paragraphs(opts.doc)

    # for dumping paragraphs
    for p in paragraphs: print(p.strip())

    '''
    # calc distances now
    distances = find_distance(paragraphs, reqs)

    # print it out
    for result in sorted(distances.items(), key=operator.itemgetter(1)):
        cols = [int(item) for item in result[0].split('_')]
        cols.append(result[1])

        if opts.include_text:
            req_txt = _get_req_text(reqs[cols[0]-2])
            cols.append(req_txt.replace('\t', ' ').replace('\n', ' '))

            para_txt = _get_para_text(paragraphs[cols[1]-1])
            cols.append(para_txt.replace('\t', ' ').replace('\n', ' '))

        print ('\t '.join(str(x) for x in cols))
        # DEBUG comparison by showing compared lines in situ of output
  #      print ('    ' + data[cols[0]-2]['content'] + " VS " + data[cols[1]-2]['content']) 
    '''


