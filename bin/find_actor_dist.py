''' 
   Find the distance between actors based on Normalized Damerau Levenshtein distance 
   we calculated.

   Example:

python bin/find_actor_dist.py -X True -w Results -f Results_9_13_17_Rqts\ Review_NISTMAP.xlsx > out

   Created on Sept 13, 2017

   @author: thomas
'''

def _key(index1, index2):
    if index1 >= index2:
        return str(index2) + '_' + str(index1)
    else:
        return str(index1) + '_' + str(index2)

def find_distance(data):

    #print("RUNNING on "+str(len(data))+" lines of data") 

    results = {}
    # gather up scores by paired combos
    for datum in data:
        # grab data
        actor1 = datum['actor1'].strip().replace(',',' ') 
        actor2 = datum['actor2'].strip().replace(',',' ') 
        dist = float(datum['dist']) 

        # TODO: flip dist ance from 0->1 to 1->0
        dist = 1. - dist

        # get key for results
        key = _key(actor1, actor2) 
        if key not in results.keys(): # and actor1 != actor2:
            results[key] = 0

        # add it in
        results[key] = results[key] + dist 

    return results

if __name__ == '__main__':
    import argparse
    import operator
    from npd.parser import parse

    # Use nargs to specify how many arguments an option should take.
    ap = argparse.ArgumentParser(description='XLSM requirements db loader')
    ap.add_argument('-f', '--file', type=str, help='Name of the Excel file which holds the data')
    ap.add_argument('-w', '--worksheet', type=str, default='Rqmts', help='Name of the worksheet where the requirements are held')
    ap.add_argument('-X', '--excel', type=bool, default=False, help='Whether file is in Excel format')

    # parse argv
    opts = ap.parse_args()

    if not opts.file:
        print ("the --file <file> parameter must be specified")
        ap.print_usage()
        exit()

    data = []
    if opts.excel:
        colmap = { 'Row1' : None, 'Row2' : None, 'Distance' : 'dist', 
                   'Actor1' : 'actor1', 'Actor2' : 'actor2',
                   'Requirement1' : None, 'Requirement2' : None, 
                   'Actor Analysis' : None, 'Req Analysis' : None
                 }
        data = parse(opts.file, opts.worksheet, colmap)
    else:
        with open(opts.file, 'r') as f:
            for item in f.readlines():
                data.append({'content':item}) 

    distances = find_distance(data)

    for result in sorted(distances.items(), key=operator.itemgetter(1), reverse=True):
        out = result[0].split('_')
        out.append(str(result[1]))
        out_str = ', '.join(out)
        print (out_str)




