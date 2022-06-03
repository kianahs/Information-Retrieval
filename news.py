import numpy as np
from heapq import nsmallest, nlargest
from numpy import NaN, linalg as LA
import math

class NewsDocument:
 

  def __init__(self, doc_ID, tokens, all_docs_count, url):

    self.doc_ID = doc_ID
    self.tokens = tokens
    self.docs_count = all_docs_count
    self.url = url

    
  def calculate_tfidf(self, word, document_frequncy_of_word):
    term_frequency = self.tokens.count(word)
    tfidf = 0
    if term_frequency > 0:
      tfidf = (1 + math.log(term_frequency)) * math.log((self.docs_count/document_frequncy_of_word))

    # if tfidf <0 :
    #   print("tfidf ", tfidf)
    
    if  tfidf < 0:
      print("negativeeeeeeeeeeeeeee")
    return  tfidf
  
  def create_vector(self, dictionary):
    self.vector_list = []

    for key in list(dictionary):
      self.vector_list.append(self.calculate_tfidf(key, dictionary[key]))
    
    self.vector = np.array(self.vector_list)

    # print(self.vector)
    
    # if not np.any(self.vector):
    #   return -1
    # return 0

  def get_doc_ID (self):
    return self.doc_ID

  def get_vector (self):

    return self.vector

  def get_url(self):
    return self.url

  def find_cosine_distance_from_query(self, query_vector):

  
    # return np.dot(self.vector,query_vector) / (LA.norm(self.vector) * LA.norm(query_vector))

    # index elimination
    indexes_of_none_zero_terms = np.where(query_vector == 0)[0]
    cosine = 0
    for index in indexes_of_none_zero_terms:
      cosine += query_vector[index] * self.vector[index]
    cosine = cosine / (LA.norm(np.nonzero(self.vector)) * LA.norm(np.nonzero(query_vector)))
    return cosine

  def find_cosine_distances_from_all_news(self, all_news, term_postings):  ############### Why is very slow

      # self.news_cosines_distances = {}

      # for news in all_news:
      #   # print(news)
      #   # print("SALAMMMMMM")
      #   news_vector = news.get_vector()
      #   # print("news vector \n {}".format(news_vector))
      #   self.news_cosines_distances[news] = np.dot(self.vector,news_vector) / (LA.norm(self.vector) * LA.norm(news_vector))
     
      # with new combination method 
    
      self.news_cosines_distances = {}
     
      related_news = set()
      for term in self.tokens:
        if term in list(term_postings):
          related_news.update(term_postings[term])


      for news in related_news:
        # print(news)
        # print("SALAMMMMMM")
        news_vector = news.get_vector()
        # print("news vector \n {}".format(news_vector))
        self.news_cosines_distances[news] = np.dot(self.vector,news_vector) / (LA.norm(self.vector) * LA.norm(news_vector))




      # # with index elimination 
      # indexes_of_none_zero_terms = np.where(self.vector == 0)[0]
      # self.news_cosines_distances = {}
     
      # related_news = set()
      # for term in self.tokens:
      #     related_news.update(term_postings[term])


      # for news in related_news:
      #   cosine = 0
      #   # print("INNN")
      #   news_vector = news.get_vector()
      #   for index in indexes_of_none_zero_terms:
      #     cosine += news_vector[index] * self.vector[index]
      #   norm = LA.norm(np.nonzero(self.vector))
      #   if norm!=0:
      #     cosine = cosine / (norm * LA.norm(np.nonzero(news_vector)))
      #   else:
      #     cosine = NaN
      #   self.news_cosines_distances[news]=cosine

  def find_cosine_distances_from_related_news(self, all_news):  ############### Why is very slow

      self.news_cosines_distances = {}

      for news in all_news:
        # print(news)
        # print("SALAMMMMMM")
        news_vector = news.get_vector()
        # print("news vector \n {}".format(news_vector))
        self.news_cosines_distances[news] = np.dot(self.vector,news_vector) / (LA.norm(self.vector) * LA.norm(news_vector))

      # # with index elimination 
      # indexes_of_none_zero_terms = np.where(self.vector == 0)[0]
      # self.news_cosines_distances = {}
     
  
      # for news in all_news:
      #   cosine = 0
      #   # print("INNN")
      #   news_vector = news.get_vector()
      #   for index in indexes_of_none_zero_terms:
      #     cosine += news_vector[index] * self.vector[index]
      #   norm = LA.norm(np.nonzero(self.vector))
      #   if norm!=0:
      #     cosine = cosine / (norm * LA.norm(np.nonzero(news_vector)))
      #   else:
      #     cosine = NaN
      #   self.news_cosines_distances[news]=cosine  

  def get_top_nearest_news(self, count):
    # print(self.title)
    top_news = nlargest(count, self.news_cosines_distances, key = self.news_cosines_distances.get)
    # print(top_journals.values())
    # print(top_journals[0].get_title())
    values =[]
    urls = []
    for news in top_news:
      values.append(self.news_cosines_distances[news])
      urls.append(news.get_url())

    return top_news,values, urls