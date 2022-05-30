
from __future__ import unicode_literals
import re
import json
# from unittest import result
from hazm import *
from news import NewsDocument

f = open('data/sample.json', encoding='utf-8')
# f = open('data/IR_data_news_12k.json', encoding='utf-8')
all_documents = json.load(f)
all_docs_count = len(all_documents)
# print(all_docs_count)
all_news = []

words_dictionary = {} # term - document frequency

previous_doc_ID = -1

for doc_ID in all_documents:
 
  print(doc_ID) 
  tokens = word_tokenize(all_documents[doc_ID]["content"])
  all_news.append(NewsDocument(doc_ID, tokens,all_docs_count))
  for word in tokens:
    if word in words_dictionary:

      if previous_doc_ID != doc_ID:
        words_dictionary[word] += 1

    else:
     
     words_dictionary[word] = 1
  
  previous_doc_ID = doc_ID

  # print(words_dictionary)

for news in all_news:
  news.create_vector(words_dictionary)


#getting query


while(True):
  input_query = input("please enter your query\n")
  if input_query == 'exit':
    break
  query_object = NewsDocument(-1, word_tokenize(input_query), all_docs_count)  # should change N ??????????????????
  query_object.create_vector(dictionary = words_dictionary)
  query_object.find_cosine_distances_from_all_news(all_news)
  top_news,cosines = query_object.get_top_nearest_news(count=10)

  i=0
  for news in top_news:
    print("docID: {}  cosine: {}".format(news.get_doc_ID(), cosines[i]))
    i+=1
