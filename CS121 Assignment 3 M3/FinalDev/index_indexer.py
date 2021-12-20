import ast
import re
from collections import defaultdict
import os.path

INDEX_CONST = 10000 #Number of lines read before we make a "bookmark" on the character position in tfidfindex.txt
DOCID_CONST = 500 #Number of lines read before we "bookmark" the DocIDPageIdentifier.txt


#Used to create an index of the tfidf index (Which is around a million lines large)
#The function returns a list of [term, bytes to skip] pairs which can be used
#in main.py's query searching process. This way, we can quickly identify the tfidfs for a
#certain term by seeking the closest term in the index's index, and reading lines from there on.
def get_index_of_index_list(path):
    counter = 0
    position = 0
    index_list = []
    myPattern = re.compile("^([a-zA-Z0-9]+=)")
    with open(path, "r") as f:
        for line in f:
            if counter % 10000 == 0:
                word = (myPattern.match(line)).group(1)
                word = word[0:len(word)-1]
                index_list.append([word, position])
            position += len(line) + 1
            counter += 1
    return index_list

#Indexes the DocIDPageIdentifier page, which is around 55,000 lines long
def get_doc_index_list(path):
    counter = 0
    position = 0
    index_list = []
    with open(path, "r") as f:
        for line in f:
            if counter % 500 == 0:
                index_list.append([counter, position])
            position += len(line) + 1
            counter += 1
    return index_list


if __name__ == "__main__":
    pass



    
        
