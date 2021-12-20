import re
import ast
import os.path

#Merge the indexes two at a time.
if __name__ == "__main__":
    #Only run one set of these 3 lines of code below at once

    #file1 = open(os.path.join("FinalDev", "offloadindex1.txt"))
    #file2 = open(os.path.join("FinalDev", "offloadindex2.txt"))
    #file3 = open(os.path.join("FinalDev", "1and2.txt"), "w")

    #file1 = open(os.path.join("FinalDev", "1and2.txt"))
    #file2 = open(os.path.join("FinalDev", "offloadindex3.txt"))
    #file3 = open(os.path.join("FinalDev", "1and2and3.txt"), "w")

    #file1 = open(os.path.join("FinalDev", "1and2and3.txt"))
    #file2 = open(os.path.join("FinalDev", "offloadindex4.txt"))
    #file3 = open(os.path.join("FinalDev", "1and2and3and4.txt"), "w")

    #file1 = open(os.path.join("FinalDev", "1and2and3and4.txt"))
    #file2 = open(os.path.join("FinalDev", "offloadindex5.txt"))
    #file3 = open(os.path.join("FinalDev", "1and2and3and4and5.txt"), "w")

    file1 = open(os.path.join("FinalDev", "1and2and3and4and5.txt"))
    file2 = open(os.path.join("FinalDev", "LastOffload.txt"))
    file3 = open(os.path.join("FinalDev", "1and2and3and4and5andLast.txt"), "w")

    #Only run one set of these 3 lines of code above at once

    line1 = file1.readline()
    line2 = file2.readline()
    myPattern = re.compile("^([a-zA-Z0-9]+=)")
    word1 = (myPattern.match(line1)).group(1)
    word2 = (myPattern.match(line1)).group(1)

    #Keep reading lines if either file has terms, postings pairs
    while (line1 != "" or line2 != ""):
        #If file1 still has term but file 2 doesn't, then just write file1 line1 to merged index.
        if(line1 == "" and line2 != ""):
            file3.write(line2)
            line2 = file2.readline()
        #vice versa as previous
        elif(line1 != "" and line2 == ""):
            file3.write(line1)
            line1 = file1.readline()
        #Merge the postings for term that was in both documents
        elif(word1 == word2):
            first = (ast.literal_eval(line1[len(word1):]))
            second = (ast.literal_eval(line2[len(word2):]))
            newList = first + second
            newList = sorted(newList)
            file3.write(word1 + str(newList) + "\n")
            line1 = file1.readline()
            line2 = file2.readline()
        #If line1 from file1 has a word that comes before line2 file2, then add line1 to merged index.
        elif(word1[0:len(word1)-1] < word2[0:len(word2)-1]):
            file3.write(line1)
            line1 = file1.readline()
        #vice versa as previous
        elif(word1[0:len(word1)-1] > word2[0:len(word2)-1]):
            file3.write(line2)
            line2 = file2.readline()
        else:
            print("This message should never be printed. This is a sanity check.", word1, word2)

        #Get a new line1 and line2 from file1 and file2 respectively.
        if(line1 != ""):
            word1 = (myPattern.match(line1)).group(1)
        if(line2 != ""):
            word2 = (myPattern.match(line2)).group(1)

    file1.close()
    file2.close()
    file3.close()
