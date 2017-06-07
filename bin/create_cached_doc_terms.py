'''

@author: thomas
'''

from ocio.textmining.extraction import UnstructuredTextTermExtractor, TextExtractorModel

import logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
#logging.getLogger('ocio').setLevel(logging.DEBUG)
#logging.getLogger('ocio.textmining').setLevel(logging.DEBUG)
#logging.getLogger('ocio.textmining.extraction').setLevel(logging.DEBUG)
logging.getLogger('gensim').setLevel(logging.WARN)

# the mininmum times we need a feature to occur
# before accepting it into our featureset
MIN_TERM_OCCUR = 1

def loadData (inputfile):
    import npd.parser as parser

    LOG.info(" * Parsing text from file")
    documents = [ req['content'] for req in parser.parse(inputfile)] 

    LOG.info("   Got "+str(len(documents))+" documents to process")
    return documents

def getTermsByDoc (documents, term_extractor):
    
    LOG.info(" * Extracting terms")

    import time
    count = 0
    data = []
    for doc in documents:

        start_time = time.time()
        LOG.debug(" * Extracting terms")
        terms = set(term_extractor.find_terms ( [doc], highest_colocation=5, 
                                                         min_term_count=MIN_TERM_OCCUR)
                                              )

        LOG.debug("TERMS: "+str(terms))
        data.append(terms)

        count = count + 1
        end_time = time.time()
        LOG.debug("pulled terms from abstract in doc:"+str(count)+" in "+str(end_time-start_time)+" sec") 

    return data

if __name__ == '__main__':
    import argparse
    import pickle
    ''' Run the application '''
    
    # Use nargs to specify how many arguments an option should take.
    ap = argparse.ArgumentParser(description='Training Appliance -- creates term lists by document for later use in training LDADomainLikelyhoodEstimator.')
    ap.add_argument('-i', '--input', type=str, help='Input austen text file')
    ap.add_argument('-o', '--output', type=str, help='File to write pickled output doc term lists')
    ap.add_argument('-m', '--term_model', type=str, help='Input model file to use to find terms in text with (a file in pickled form)')
   
    # parse argv
    opts = ap.parse_args()
    
    if not opts.input:
        print ("the --input <file> parameter must be specified")
        ap.print_usage()
        exit()
        
    if not opts.output:
        print ("the --output <file> parameter must be specified")
        ap.print_usage()
        exit()
        
    if not opts.term_model:
        print ("the --term_model <file> parameter must be specified")
        ap.print_usage()
        exit()
    
    documents = loadData (opts.input)
    
    LOG.info(" * Loading dict and processing rules models")
    term_model = TextExtractorModel().load_from_file(opts.term_model)
    
    # create our term/feature extractor
    term_extractor = UnstructuredTextTermExtractor(term_model)
    
    # get the input for training NBC ConceptExtractor
    data = getTermsByDoc(documents, term_extractor)
    
    LOG.info(" * Writing pickled output to file:"+ opts.output)
    with open(opts.output, 'wb+') as f:
        pickle.dump(data, f)

    LOG.info(" * Finished")


