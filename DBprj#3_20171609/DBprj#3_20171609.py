#-*- coding: utf-8 -*-
import datetime
import time
import sys
import MeCab
import operator
import math
from pymongo import MongoClient
from bson import ObjectId
from itertools import combinations
import re


def printMenu():
    print "1. WordCount"
    print "2. TF-IDF"
    print "3. Similarity"
    print "4. MorpAnalysis"
    print "5. CopyData"


#In this project, we assume a word seperated by a space is a morpheme.
def MorphAnalysis(docs, col_tfidf):
	print("MorpAnalysis")

	# Step(1) Read stopword list from file named stopwrod_list.txt
	stop_word = {}
	f = open("stopword_list.txt", "r")
	while True:
		line = f.readline()
		if not line: break
		stop_word[line.strip('\n')] = line.strip('\n')
	f.close()

	# Step(2) Anlaysis Morpheme in given text and delete stopword
	for doc in docs:
		content = doc['text']
		#Delete non-alphabetical characters
		content = re.sub('[^a-zA-Z]', ' ', content)
		#change all capital letter to small letter
		content = content.lower().split()

		#delete stopword in a given text dataset
		MorpList = []

		for arg in content:
			if not arg in stop_word:
				MorpList.append(arg)
	# Step(3) Store processed morpheme data into MongoDB
		col_tfidf.update({'_id':doc['_id']}, {'$set': {'morph': MorpList}}, True)

	input_id = str(raw_input("Insert Object ID: "))
	find0 = col_tfidf.find({'_id': ObjectId(input_id)})
	for i in find0:
		for j in i['morph']:
			print j

def WordCount(docs, col_tfidf):
	print("WordCount")
	#TO-DO
	stop_word={}
	f=open("stopword_list.txt","r")
	while True:
	    line=f.readline()
	    if not line: break
	    stop_word[line.strip('\n')]=line.strip('\n')
	f.close()
	
	for doc in docs:
            CountArray={}
	    content=doc['text']
	    content=re.sub('[^a-zA-Z]',' ',content)
	    content= content.lower().split()
		
	    for arg in content:
		if not arg in stop_word:
		    CountArray[arg] = CountArray.get(arg,0) + 1

	    col_tfidf.update({'_id':doc['_id']},{'$set':{'word_count':CountArray}},True)	

    
        id_input = str(raw_input("Insert Object ID: "))
	find1 = col_tfidf.find({'_id': ObjectId(id_input)})
	for i in find1:
	    result = i['word_count']
	    result2 = i
	    for j in result:
		print j,":", result[j]
		temp2 = result2
	


def TfIdf(docs, col_tfidf):
	print("TF-IDF")
	count = 0
	count22 = 0
	for doc in docs:
            arraytfidf = {}
            cnt_doc = 0
            tf = 0
            idf = 0
                
	    wordcountArray = doc['word_count']
	    wordcountArrayKey = wordcountArray.keys()

	    if 'tf_idf' in doc:
		continue
		
            for q in wordcountArrayKey:
                        
		cnt = 0
		count_docs2 = 0
		sizelen = len(doc['morph'])                        
		tf = float(wordcountArray[q])/sizelen
			
		cnt_doc = cnt_doc + 1
		docs2 = col_tfidf.find()
                for p in docs2:
		    count_docs2 = count_docs2 + 1
		    temp = count_docs2
		    if q in p['morph']:
			cnt = cnt + 1
			
		idf = math.log(float(count_docs2)/cnt)
		cnt_doc = cnt_doc + 1
		arraytfidf[q] = tf * idf

	    col_tfidf.update({'_id':doc['_id']}, {'$set': {'tf_idf': arraytfidf}}, True)
	
        id_input = str(raw_input("Input ID: "))
	find2 = col_tfidf.find({'_id': ObjectId(id_input)})

	
	for i in find2:
            lentf = len(i['tf_idf'])
	    for j in sorted(i['tf_idf'], key = i['tf_idf'].get, reverse = True):
                count22 = 1
                print j, "\t", i['tf_idf'][j]
                count = count + 1
                if count >= 10:
                    count22 = 0
                    break
	
def Similarity(docs, col_tfidf):
	print("Similiarity")

        findarr1 = []
        findarr2 = []
	findmorph1 = []
	findmorph2 = []
	countaa = 0
	countbb = 0
	result1 = []
	result2 = []
	ab = 0
	aa = 0
	bb = 0
	switch1 = 0
	
	
	inputID1 = raw_input("Insert Object ID(1): ")
	inputID2 = raw_input("Insert Object ID(2): ")

	a1 = col_tfidf.find({'_id': ObjectId(inputID1)})
	for i in a1:
	    findarr1 = i['tf_idf']
	    countaa = countaa + 1
	    findmorph1 = i['morph']

	countbb = countbb + 1
        countaa = 0
	
	a2 = col_tfidf.find({'_id': ObjectId(inputID2)})
	for i in a2:
	    findarr2 = i['tf_idf']
	    countaa = countaa + 1
	    findmorph2 = i['morph']

	hapList = list(set(findmorph1 + findmorph2))

	countbb = countbb + 1
        countaa = 0

	for i in hapList:
	    if i in findarr1:
		result1.append(findarr1[i])
		switch1=0
	    else:
		result1.append(0)
		switch1=1

            temp = i
            
	    if i in findarr2:
		result2.append(findarr2[i])
		switch1=0
	    else:
		result2.append(0)
		switch1=1

	#print(switch1)
	sizeoflist = len(hapList)
	for i in range(sizeoflist):
	    ab = ab + result1[i]*result2[i]
	    aa = aa + result1[i]*result1[i]
	    bb = bb + result2[i]*result2[i]
		
	if (aa == 0) or (bb == 0):
            totalresult = 0.0
        else :
            totalresult = float(ab)/(math.sqrt(aa) * math.sqrt(bb))
            
	print totalresult



def copyData(docs, col_tfidf):
	col_tfidf.drop()
	for doc in docs:
		contentDic = {}
		for key in doc.keys():
			if key != "_id":
				contentDic[key] = doc[key]
		col_tfidf.insert(contentDic)
def p2(id_input):
	col1 = db['tweet_tfidf']
	for doc in col1.find({"_id":id_input}):
		for word in doc['morph']:
			print word


#Access MongoDB
conn = MongoClient('localhost')

#fill it with your DB name - db+studentID ex) db20120121
db = conn['db20171609']

#fill it with your MongoDB( db + Student ID) ID and Password(default : 1234)
db.authenticate('db20171609', '1234')

col = db['tweet']

col_tfidf = db['tweet_tfidf']

if __name__ == "__main__":
	printMenu()
	selector = input()

	if selector == 1:
    		docs = col_tfidf.find()
	    	WordCount(docs, col_tfidf)

	elif selector == 2:
                docs = col_tfidf.find()
		TfIdf(docs, col_tfidf)

	elif selector == 3:
		docs = col_tfidf.find()
		Similarity(docs, col_tfidf)

	elif selector == 4:
		docs = col_tfidf.find()
		MorphAnalysis(docs, col_tfidf)

	elif selector == 5:
		docs = col.find()
		copyData(docs,col_tfidf)

