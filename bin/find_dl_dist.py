
def _key(index1, index2):
    if index1 >= index2:
        return str(index2) + '_' + str(index1)
    else:
        return str(index1) + '_' + str(index2)

def find_distance(data):
    from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance

    results = {} 
    idi = 0
    for ireq in data:
        idj = 0
        for jreq in data:
            key = _key(idi, idj)
            if key not in results.keys() and idi != idj:
                results[key] = normalized_damerau_levenshtein_distance(ireq['content'], jreq['content'])
            idj = idj + 1
        idi = idi + 1
             
    return results

if __name__ == '__main__':
    import argparse
    import operator
    from npd.parser import parse 

    # Use nargs to specify how many arguments an option should take.
    ap = argparse.ArgumentParser(description='XLSM requirements db loader')
    ap.add_argument('-f', '--file', type=str, help='Name of the Excel file which holds the data')

    # parse argv
    opts = ap.parse_args()

    if not opts.file:
        print ("the --file <file> parameter must be specified")
        ap.print_usage()
        exit()

    data = parse(opts.file)
    distances = find_distance(data)
    for result in sorted(distances.items(), key=operator.itemgetter(1)):
        cols = str(result[0]).split('_')
        cols.append(str(result[1]))
        print (str(cols))

    print ("Finished")




