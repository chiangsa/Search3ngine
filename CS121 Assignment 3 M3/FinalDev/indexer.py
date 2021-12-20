import os
import json
from bs4 import BeautifulSoup
import lxml
from nltk.stem import PorterStemmer
import re
from collections import defaultdict
import sys
import cysimdjson
import time

OFFLOAD_TRIGGER = 10000 #How many json webpages before we offload inverted index.
BASE_PATH = 'DEV' #Folder of where json webpages are stored


def porter_tokenize(text):
    token_list = []
    raw_tokens = re.split('[^a-zA-Z0-9]', text)
    for token in raw_tokens:
        if token.isalnum():
            token_list.append(ps.stem(token.lower()))
    return token_list

#duplicate function, main.py needs to call it when tokenizer the user's search query
def porter_tokenizer(text):
    ps = PorterStemmer() #Needed when another file calls this function
    token_list = []
    raw_tokens = re.split('[^a-zA-Z0-9]', text)
    for token in raw_tokens:
        if token.isalnum():
            token_list.append(ps.stem(token.lower()))
    return token_list

#compute dict with key:term, value:frequency for a given document's token_list
def compute_word_freq(token_list):
    token_dict = defaultdict(int)
    for token in token_list:
        token_dict[token] += 1
    return token_dict

#Increase the term frequency score of terms in titles, headers, or that are bolded
def compute_important_words(porter_token_dict, soup):
    #Find all titles, headers, and bolds in the soup object
    titles = soup.find_all("title")
    headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8"])
    bolds = soup.find_all(["strong", "b"])

    #Terms in titles receive a 10x term frequency boost
    for title in titles:
        porter_titles_text = porter_tokenize(title.get_text())
        for token in set(porter_titles_text):
            porter_token_dict[token] += 10
    
    #Terms in headers (1st-8th headers) receive a 6x term frequency boost
    for header in headers:
        porter_headers_text = porter_tokenize(header.get_text())
        for token in set(porter_headers_text):
            porter_token_dict[token] += 6
    
    #Terms that are bolded receive a 4x term frequency boost
    for bold in bolds:
        porter_bolds_text = porter_tokenize(bold.get_text())
        for token in set(porter_bolds_text):
            porter_token_dict[token] += 4
    
    return porter_token_dict

#If document threshhold is met (10,000 webpages/docs) we will offload inverted index into a .txt file.
def offload_index(inverted_index_dict):
    offloadFile = "offloadindex" + str(document_count // OFFLOAD_TRIGGER) + ".txt"
    writeFile = os.path.join("FinalDev", offloadFile)
    myFile = open(writeFile, "w")
    #Sort the dictionary before writing it to text file, for easier merging later on.
    sorted_dict = sorted(inverted_index_dict.keys(), key = lambda x: x.lower())
    for item in sorted_dict:
        myFile.write(item + "=" + str(inverted_index_dict[item]) + "\n")
    myFile.close()
    #Clear inverted index
    inverted_index_dict.clear()


if __name__ == '__main__':
    timeBegin = time.time()
    document_count = 1 #keep track of what document we are on
    inverted_index = defaultdict(list) #inverted index of term, postings
    ps = PorterStemmer() #Porter Stemmer tokenization
    #wordset = set() #keep track of all porter tokens we have, for sanity check purposes
    basepath = BASE_PATH
    #For each folder in DEV
    for entry in os.listdir(basepath):
        if os.path.isdir(os.path.join(basepath, entry)):
            fullpath = basepath + "/" + entry
            print("Indexing", fullpath)
            json_pages = os.listdir(fullpath)
            f2 = open(os.path.join("FinalDev", "DocIDPageIdentifier.txt"), "a")

            #Each json in folder
            for page in json_pages:
                page_path = fullpath + "/" + page
                with open(page_path) as f:
                    #Load json data and feed it to beautiful soup library that converts it into text
                    data = json.load(f)
                    soup = BeautifulSoup(data['content'],'lxml')
                    text = soup.get_text()
                    pt_list = porter_tokenize(text) #tokenize all the content
                    pt_dict = compute_word_freq(pt_list) #add tokens to a dict with key=token, value=frequency
                    pt_dict = compute_important_words(pt_dict, soup) #increase weighting of tokens in titles, headers, and bolded/strong

                    #for word in pt_dict:
                    #    wordset.add(word) #just to keep track of how many words we have
                    for word, frequency in pt_dict.items():
                        inverted_index[word].append((document_count,frequency),) #add the (doc_id, term num) tuples to the inverted index.
                    
                    doc_unique_words = len(pt_dict) #tally of how many unique tokens a document has
                      
                    f2.write(str(document_count) + " -- " + str(doc_unique_words) + " -- " + data['url'] + "\n")
                    
                    if(document_count % OFFLOAD_TRIGGER == 0): #if index gets too large, store index in disk and reset to save memory
                        offload_index(inverted_index)

                    document_count += 1 #Once program terminates, total documents is 1 less than this integer
            f2.close()
                
    print("FINAL OFFLOADING") #Last offload
    f1 = open(os.path.join("FinalDev", "LastOffload.txt"), "w")
    sorted_dict = sorted(inverted_index.keys(), key = lambda x: x.lower())
    for item in sorted_dict:
        f1.write(item + "=" + str(inverted_index[item]) + "\n")
    f1.close()

    print("A total of", str(document_count-1), "files were indexed.")
    #print("Number of unique Porter tokens was", len(wordset))
    print("Size of last offload index was", sys.getsizeof(inverted_index), "bytes")
    
    timeEnd = time.time()
    f1 = open(os.path.join("FinalDev", "Analytics.txt"), "a")
    f1.write("Total documents indexed: " + str(document_count - 1) + "\n")
    #f1.write("Number of unique Porter tokens: " + str(len(wordset)) + "\n")
    f1.write(str(timeEnd - timeBegin) + "\n")
    f1.close()
            


    
