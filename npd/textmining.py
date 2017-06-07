'''

Some general processing tools/code for NPD text.

Created on June 6, 2017

@author: thomas
'''

from ocio.textmining.extraction import StemmingTool, ProcessTextTool

import logging
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class EnglishStemmer (StemmingTool):
    
    def stem_tokens(self, token_list):
        from nltk.stem import SnowballStemmer

        stemmer = SnowballStemmer('english')

        for i in range(len(token_list)):
            # IF its not an acronym, lets stem it
            if token_list[i] != token_list[i].upper():
                token_list[i] = stemmer.stem(token_list[i])
         
        return token_list

    def __init__(self): pass
    
class DocTextProcessor (ProcessTextTool):
    
    # Rules for processing tokens which we may miss with ordinary
    # processing engine. Rules which match will cause all whitespace
    # to be changed into underscores so that the words will be picked
    # up as a group 
    _Special_Token_Patterns = []
    
    # some common formatting patterns we need to clean out
    _Format_Token_Replacement_Patterns = { '\r' : ' ', '\n' : ' ', '\ufeff' : '', 
                                          ':': '', '[': '', ']': '',  '(': '',
                                          ')': '', '\'': '', '=': '', '&': 'and', '\\': '',
                                          '/ >': '', '~' : '', 'and/or' : '',
                                        } 
    
    # some replacement patterns germane to just Austen data
    # includes some particular misspellings and duplications
    _Austen_Token_Repl_Patterns = { 'balck': 'black', }
    
    @staticmethod
    def process (corpus):
        ''' process our text, which assumed to be in a list ''' 

        LOG.debug (" - Processing corpii text")
        processed_corpus=[]
        for corpii in corpus:
            processed_corpus.append(DocTextProcessor._process_one(corpii))
                
        return processed_corpus

    @staticmethod
    def _process_one (document):
        import re
        
        # initialize processing rules from expected patterns
        processing_rules = dict( DocTextProcessor._Format_Token_Replacement_Patterns, 
                                 **DocTextProcessor._Austen_Token_Repl_Patterns
                               )
    
        # process it to pull out sources, changing spaces to underscore so we make
        # sure to capture the term fully
        for pattern in DocTextProcessor._Special_Token_Patterns:
            results = re.findall(pattern, document)
            replacement_labels = {}
            if results:
                for result in results:
                     
                    #clean up XML-ish formatting
                    result = re.sub('\<\/?\w+\>', '', result)
                     
                    # store the processing rule for downstream use
                    # replace spaces with underscore so we ensure tokenization
                    #processing_rules[result] = result.replace(' ','_')
                    document = document.replace(result, result.replace(' ','_'))
        
        # apply all of the processing rules now 
        for rule in processing_rules:
            #LOG.debug("Running processing rule:["+str(rule)+"]")
            document = document.replace(rule, processing_rules[rule])
            
        # finally, trim leading and trailing whitespace
        # and return
        return document.strip()
        
    def __init__(self): pass
    

