This document gives a brief overview of what the 5 .py files in the FinalDev folder do

-----------------------------------------------------------------------------------------------------------
Indexing Process

indexer.py      	---> Reads json files from Dev folder (not included in this zip file) and creates many small indexes

mergeindex.py   	---> Merges the smaller indexes created by indexer.py

tf_idf_calculation.py   ---> Calculates the tfidf using the full index created by mergeindex.py

-----------------------------------------------------------------------------------------------------------
Searching Process

index_indexer.py	---> Indexes the td_idf index, so we can perform seek() operations to quickly retrieve
			     term tfidf scores.

main.py			---> THE ACTUAL SEARCH ENGINE/INTERACTABLE PART OF PROGRAM
			     User can type Y or N if they want develop mode to see the modified tfidf and
			     raw tfidf scores used in ranking the queries.

-----------------------------------------------------------------------------------------------------------