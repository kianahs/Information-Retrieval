
from __future__ import unicode_literals
import re
import json
import pickle
# from unittest import result
from hazm import *
from news import NewsDocument



def creating_dictionary_and_vectors():

  # f = open('data/sample.json', encoding='utf-8')
  f = open('data/IR_data_news_12k.json', encoding='utf-8')
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
  i = 0
  for news in all_news:
    print(i)
    news.create_vector(words_dictionary)
    i+= 1


  #saving data

  file = open("words_dictionary.pkl","wb")
  pickle.dump(words_dictionary, file) 
  file.close()
  file = open("all_news.pkl","wb")
  pickle.dump(all_news, file) 
  file.close()

  return words_dictionary, all_news

def get_data_from_files():

  #oppening data files 
  file = open("pickleFiles/words_dictionary.pkl", "rb")
  words_dictionary = pickle.load(file)
  file.close()
  file = open("pickleFiles/all_news.pkl", "rb")
  all_news = pickle.load(file)
  file.close()
  return words_dictionary, all_news





# words_dictionary, all_news = get_data_from_files()
words_dictionary, all_news = creating_dictionary_and_vectors()

#getting query


while(True):
  input_query = input("Please enter your query\n")
  if input_query == 'exit':
    break
  query_object = NewsDocument(-1, word_tokenize(input_query), len(all_news))  # should change N ??????????????????
  query_object.create_vector(dictionary = words_dictionary)
  query_object.find_cosine_distances_from_all_news(all_news)
  count = input("Enter number of k for showing top k results\n")
  top_news,cosines = query_object.get_top_nearest_news(count=int(count))

  i=0
  for news in top_news:
    print("docID: {}  cosine: {}".format(news.get_doc_ID(), cosines[i]))
    i+=1
