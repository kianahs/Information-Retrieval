
from __future__ import unicode_literals
import re
import json
import pickle
# from unittest import result
from hazm import *
from news import NewsDocument

from unittest import result
from itertools import combinations
import matplotlib.pyplot as plt
import math
import pickle

garbage = ['۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰', 'a', 'b', 'c', 'd', 'e', 't', 'o', 'p', 'x', 'y', 'z',
           'https', '،', '.', ':', '**', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '?', '**', '[', ']',
           '(', ')', '://', '/?', '=', '&', '/', '؛', '&', '/', '.', '_', '،', '?**', ":", "%", ">>", "<<", "!","#"
           "*", "«", "»"]

normalizer = Normalizer()
lemmatizer = Lemmatizer()
stemmer = Stemmer()
stop_words_list = stopwords_list()

def creating_dictionary_and_vectors():

  # f = open('data/sample.json', encoding='utf-8')
  f = open('data/IR_data_news_12k.json', encoding='utf-8')
  all_documents = json.load(f)
  all_docs_count = len(all_documents)
  print(all_docs_count)
  all_news = []

  words_dictionary = {} # term - document frequency
  term_postings = {} # term - postings list
  # previous_doc_ID = -1

  for doc_ID in all_documents:
  
    print(doc_ID) 
    initial_tokens = word_tokenize(normalizer.normalize(all_documents[doc_ID]["content"]))
    tokens = preprocess_tokens(initial_tokens)
    doc_object = NewsDocument(doc_ID, tokens, all_docs_count, all_documents[doc_ID]["url"])
    all_news.append(doc_object)
    
    for word in tokens:
      if word in words_dictionary:

        
        term_postings[word].add(doc_object)
        words_dictionary[word] = len(term_postings[word])

      else:
      
       term_postings[word] = set()
       term_postings[word].add(doc_object)
       words_dictionary[word] = len(term_postings[word])
      #  previous_doc_ID = doc_ID

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
  file = open("term_postings.pkl","wb")
  pickle.dump(term_postings, file) 
  file.close()

  return words_dictionary, all_news, term_postings

def get_data_from_files():

  #oppening data files 
  print("getting dictionary ......")
  file = open("pickleFiles/words_dictionary.pkl", "rb")
  words_dictionary = pickle.load(file)
  file.close()
  print("getting documents ......")
  file = open("pickleFiles/all_news.pkl", "rb")
  all_news = pickle.load(file)
  file.close()
  print("getting champion list ......\n")
  file = open("pickleFiles/champion_list.pkl", "rb")
  term_champion_list = pickle.load(file)
  file.close()
  print("getting term postings ......\n")
  file = open("pickleFiles/term_postings.pkl", "rb")
  term_postings = pickle.load(file)
  file.close()
  print("Done \n")

  return words_dictionary, all_news, term_champion_list, term_postings

def search_query(input_query, count, dictionary, all_news, term_postings):
  tokens = preprocess_tokens(word_tokenize(normalizer.normalize(input_query)))
  query_object = NewsDocument(-1, tokens, len(all_news), None)  # should change N ??????????????????
  query_object.create_vector(dictionary)
  query_object.find_cosine_distances_from_all_news(all_news, term_postings)
  # count = input("Enter number of k for showing top k results\n")
  top_news,cosines,urls = query_object.get_top_nearest_news(count=int(count))
  # print(cosines)
  return top_news,cosines,urls

def create_champions_list(count, words_dictionary, all_news, term_postings):
  term_champion_list = {}
  print("creating champions list ...")
  i=0
  for term in list(words_dictionary):
    top_news, _ , urls = search_query(term, count, words_dictionary, all_news, term_postings)
    term_champion_list[term] = top_news
    print(term, i)
    i += 1
  
  file = open("champion_list.pkl","wb")
  pickle.dump(term_champion_list, file) 
  file.close()
  print("Done \n")

def search_using_champion_list(input_query, words_dictionary, all_news, term_champion_list):

  # print("getting champion list ......\n")
  # file = open("pickleFiles/champion_list.pkl", "rb")
  # term_champion_list = pickle.load(file)
  # file.close()
  related_news = []
  
  query_tokens = preprocess_tokens(word_tokenize(normalizer.normalize(input_query)))
  
  for token in query_tokens:
    related_news.extend(term_champion_list[token])


  query_object = NewsDocument(-1, query_tokens, len(all_news), None)  # should change N ??????????????????
  query_object.create_vector(words_dictionary)
  query_object.find_cosine_distances_from_related_news(related_news)
  count = input("Enter number of k for showing top k results\n")
  top_news,cosines,urls = query_object.get_top_nearest_news(count=int(count))
  
  return top_news,cosines,urls

def preprocess_tokens(tokens):

  tokens_without_stop_words = []

  for token in tokens:
    token = re.sub(r'[^\w\s]','', token)
    if token not in stop_words_list:
      tokens_without_stop_words.append(token)
   
  for token in tokens_without_stop_words:
    for s in garbage:
      if s in token:
        # print("token garbage", token)
        tokens_without_stop_words.remove(token)
        break

  pure_root_tokens = list(map(lambda word: lemmatizer.lemmatize(stemmer.stem(word)), tokens_without_stop_words))
 
  return pure_root_tokens



if __name__ == "__main__":

  words_dictionary, all_news, term_champion_list, term_postings = get_data_from_files()
  # words_dictionary, all_news = get_data_from_files()
  # words_dictionary, all_news, term_postings = creating_dictionary_and_vectors()
  print(len(words_dictionary))
  # create_champions_list(20, words_dictionary, all_news, term_postings)

  # term_champion_list={}

  #getting query
  
  # for doc in term_postings['پیکان']:
  #   print(doc.get_doc_ID())

  while(True):
    input_query = input("Please enter your query\n")
    if input_query == 'exit':
      break
    method = input("1.normal 2.champion\n")
    top_news, cosines, urls = None, None, None

    if int(method) == 1:
      count = input("Enter number of k for showing top k results\n")
      top_news,cosines,urls = search_query(input_query, count, words_dictionary, all_news, term_postings)

      # query_object = NewsDocument(-1, preprocess_tokens(word_tokenize(normalizer.normalize(input_query))), len(all_news), None)  # should change N ??????????????????
      # query_object.create_vector(words_dictionary)
      # query_object.find_cosine_distances_from_all_news(all_news)
      # count = input("Enter number of k for showing top k results\n")
      # top_news,cosines,urls = query_object.get_top_nearest_news(count=int(count))
    elif int(method) == 2:
      top_news,cosines,urls = search_using_champion_list(input_query, words_dictionary, all_news, term_champion_list)
      # continue
    i=0
    for news in top_news:
      print("docID: {}  cosine: {}  url: {}".format(news.get_doc_ID(), cosines[i], urls[i]))
      i+=1



  