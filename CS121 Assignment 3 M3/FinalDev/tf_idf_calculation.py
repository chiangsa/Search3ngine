import re
import ast
import math
import os.path

NUM_DOCUMENTS = 55393 #The number of documents in DEV folder
MAX_POSTINGS = 3000 #The maximum number of tfidf postings that can be associated with a term

#Used in lambda sorting below
def getSecondElement(iterable):
    return iterable[1]


if __name__ == "__main__":
    file1 = open(os.path.join("FinalDev","1and2and3and4and5andLast.txt"), "r")
    file2 = open(os.path.join("FinalDev","TfIdfIndex3000.txt"), "w")
    myPattern = re.compile("^([a-zA-Z0-9]+=)")

    #Read each line in the final, merged index and calculate the tfidf
    #of each term for each document
    line1 = file1.readline()
    while(line1 != ""):
        #In the form TERM=[(posting),]
        word = (myPattern.match(line1)).group(1)
        word_index_list = (ast.literal_eval(line1[len(word):]))
        #Calculate the number of documents that have this term
        num_doc_with_term = len(word_index_list)
        new_list = []
        for doc in word_index_list:
            #Doc is the postings, doc[0] is the id, doc[1] is term frequency
            doc_id = doc[0]
            #TF SCORE
            tf_score = 1 + math.log10(doc[1])
            #IDF SCORE
            idf_score = math.log10(NUM_DOCUMENTS/num_doc_with_term)
            #TFIDF SCORE
            tf_idf_score = tf_score * idf_score
            new_list.append(tuple([doc_id, round(tf_idf_score, 5)]))

        #Sort the list of tfidfs, and then get the top ranking 3,000 tfidf documents 
        #if there are over 3,000 postings for a term.
        new_list.sort(key = getSecondElement, reverse = True)
        if len(new_list) > MAX_POSTINGS:
            new_list = new_list[0:MAX_POSTINGS]
        file2.write(word + str(new_list) + "\n")

        line1 = file1.readline()
    
    file1.close()
    file2.close()

    