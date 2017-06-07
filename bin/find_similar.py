
import ocio.textmining.document as d

if __name__ == '__main__':
    import argparse
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

    print ("Finished")




