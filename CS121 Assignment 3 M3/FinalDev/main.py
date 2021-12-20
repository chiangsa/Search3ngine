from indexer import porter_tokenizer
from nltk.stem import PorterStemmer
import time
import ast
from collections import defaultdict
import re
from index_indexer import *
import math
import os.path

#The tfidf index document we are using
TFIDF_INDEX = "TfIdfIndex3000.txt"

#Returns the last element of an iterable size 4
def getLastElement(iterable):
    return iterable[3]

#Further modifies the tfidf score of a document. Dividing its score by log10('number of unique terms in the document')
#Returns this "density" score. The higher the density, the more likely the document is to contain the desired search query information.
def density(path, tup, doc_index_list):
    #DocIDPageIdentifier.txt in format "[doc_i] -- [num unique terms] -- [url]"
    myPattern = re.compile("^([0-9]+) -- ([0-9]+) -- (.+)")
    with open(path, "r") as f:
        i = 0
        skip_chars = doc_index_list[i][1]
        #Use the index to quickly find where in the file to start searching for the document and get it's information
        while(i < len(doc_index_list) and int(doc_index_list[i][0]) <= tup[0]):
            skip_chars = doc_index_list[i][1]
            i += 1
        f.seek(skip_chars)
        current_line = f.readline()
        myMatch = myPattern.match(current_line)

        #Once finding the closest index to start searching from, iterates down file until it finds the document information
        while (int(myMatch.group(1)) != tup[0]):
            current_line = f.readline()
            myMatch = myPattern.match(current_line)
        numUniqueTerms = myMatch.group(2)

        return myMatch.group(3), float(tup[1]) / math.log10(int(numUniqueTerms))


if __name__ == "__main__":
    myPattern = re.compile("^([a-zA-Z0-9]+=)")
    ps = PorterStemmer()
    #Load the index on the inverted index
    print("---Loading Inverted Index---")
    index_list = get_index_of_index_list(os.path.join("FinalDev", TFIDF_INDEX))
    print("---Inverted Index Loaded---")
    #Load the index on the document identifier index
    print("---Loading Document Retrieval Index---")
    doc_index_list = get_doc_index_list(os.path.join("FinalDev", "DocIDPageIdentifier.txt"))
    print("---Document Retrieval Index Loaded---")

    DevMode = False
    #If user wants to see the raw tfidf and modified tfidf scores afterwards.
    YorN = input("Would you like to see the TFIDF weights (DevMode)? Y or N\n")
    if (YorN == "Y"):
        DevMode = True

    query = input("Enter your search query\n")
    print()
    t0 = time.time() #START TAKING TIME AFTER THEY INPUT QUERY
    porter_query_terms = porter_tokenizer(query) #TOKENIZE THEIR TERMS USING SAME TOKENIZER WE USED FOR CREATING INVERTED INDEX
    searches = dict()
    for term in porter_query_terms:
        temp = term + "="
        searches[temp] = len(temp)

    urlsDict = defaultdict(int)
    linesread = 0
    urlsList = []
    with open(os.path.join("FinalDev", TFIDF_INDEX), "r") as f:
        for term in porter_query_terms:
            i = 0
            skip_chars = index_list[i][1]
            #Use the index that we made on the inverted index, to quickly seek() past terms.
            while (i < len(index_list) and index_list[i][0] <= term):
                skip_chars = index_list[i][1]
                i += 1
            f.seek(skip_chars)
            current_line = f.readline()
            skip_chars += len(current_line) + 1
            linesread += 1
            current_lines_read = 0
            #Once we find correct seek() spot, look if term exists here. If more than 10000 iterations pass, the term doesn't exist.
            while current_line[0:len(term)+1] != (term + "=") and current_lines_read <= 10000:
                current_line = f.readline()
                linesread += 1
                current_lines_read += 1

            #Check if the line we ended on actually is the term we want. If so, take the postings and their tfidf
            #scores, and add them to our current dictionary of results
            if current_line[0:len(term)+1] == (term + "="):
                myTerm = myPattern.match(current_line).group(1)
                documents_tfidf_list = (ast.literal_eval(current_line[len(myTerm):]))
                for word in documents_tfidf_list:
                    urlsDict[word[0]] += word[1]
            
    #Just take the top 20 results in our URL dictionary that have the highest tfidf scores.
    sortedList = sorted(urlsDict.items(), key = lambda x : (x[1]), reverse=True)[:20]
    temp =[]

    #Calculate our modified tfidf density ranking. Document with high tfidf and lower word count usually means 
    # #HIGHER quality, dense information related to our query.
    for tup in sortedList:
        url, weighting = density(os.path.join("FinalDev", "DocIDPageIdentifier.txt"), tup, doc_index_list)
        temp.append([tup[0], tup[1], url, weighting, tup[1]])

    temp.sort(key = getLastElement, reverse = True)

    #If our URL list is empty, then we didn't get any search results.
    if(len(temp) == 0):
        print("No search results found for query", query)
    else:
        counter = 1
        for x in temp:
            #Print information nicely.
            if DevMode:
                print('{place:<5}URL: {url:<120}Modified TFIDF: {dscore:<10}RAW TFIDF:{tfidf:<10}'.format(place = counter, url = x[2], dscore = round(x[3], 5), tfidf = round(x[4], 5)))
                counter += 1
            else:
                print('{place:<5}URL: {url:<120}'.format(place = counter, url = x[2]))
                counter += 1

    print()
    t1 = time.time()
    difference_times = t1 - t0
    #Output the time the query took.
    print("Search took", round(difference_times*1000, 10), "milliseconds")
