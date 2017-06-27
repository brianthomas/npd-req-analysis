
''' generate some random data so we can estimate the false discovery rate for ndl metric
'''

def _key(index1, index2):
    if index1 >= index2:
        return str(index2) + '_' + str(index1)
    else:
        return str(index1) + '_' + str(index2)

def find_distance(data):
    from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance

    # print("RUNNING on "+str(len(data))+" lines of data") 
    results = {} 
    idi = 2
    for ireq in data:
        idj = 2
        for jreq in data:
            key = _key(idi, idj)
            if key not in results.keys() and idi != idj:
 
                ireq_txt = ""
                if ireq['content']: 
                    ireq_txt = ireq['content'].strip()
                jreq_txt = ""
                if jreq['content']: 
                    jreq_txt = jreq['content'].strip()
                if ireq_txt == "" and jreq_txt == "": 
                    # trivial case, NO requirements text to cross compare
                    pass
                else:
                    results[key] = normalized_damerau_levenshtein_distance(ireq_txt, jreq_txt)
            idj = idj + 1
        idi = idi + 1
             
    return results

def randomize_data(data):
    ''' change data to be randomized word assortment with same occurance 
        as original population.
    '''
    randomized_data = []
    random_words = make_random_word_list(data)

    for item in data:
        content = item['content']
        new_content = ""
        if content:
            # build new content based on word count of original content
            nrof_words = len(content.split(' '))
            while (nrof_words > 0):
                new_content = new_content + ' ' + random_words.pop()
                nrof_words = nrof_words - 1
            
        randomized_data.append({'content': new_content})

    return randomized_data

def make_random_word_list (data):
    ''' create a list of random words with same occurance as in original data
    '''
    from random import shuffle 
    random_words = []
    for content in data:
        text = content['content']
        if text:
            for word in content['content'].split(' '):
                random_words.append(word)
    # print (random_words[0])
    shuffle(random_words)
    return random_words

if __name__ == '__main__':
    import argparse
    import operator
    from npd.parser import parse 

    # Use nargs to specify how many arguments an option should take.
    ap = argparse.ArgumentParser(description='XLSM requirements db loader')
    ap.add_argument('-f', '--file', type=str, help='Name of the Excel file which holds the data')
    ap.add_argument('-X', '--excel', type=bool, default=False, help='Whether file is in Excell format')

    # parse argv
    opts = ap.parse_args()

    if not opts.file:
        print ("the --file <file> parameter must be specified")
        ap.print_usage()
        exit()

    data = []
    if opts.excel:
        data = parse(opts.file)
    else:
        with open(opts.file, 'r') as f:
            for item in f.readlines():
                data.append({'content':item}) 

    data = randomize_data(data)
    # print ("Randomized data, first item: "+data[0]['content'])

    distances = find_distance(data)
    for result in sorted(distances.items(), key=operator.itemgetter(1)):
        cols = [int(item) for item in result[0].split('_')]
        cols.append(result[1])
        print (', '.join(str(x) for x in cols))
        # DEBUG comparison by showing compared lines in situ of output
  #      print ('    ' + data[cols[0]-2]['content'] + " VS " + data[cols[1]-2]['content']) 




