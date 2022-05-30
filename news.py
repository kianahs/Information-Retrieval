import numpy as np
from heapq import nsmallest, nlargest
from numpy import linalg as LA
import math

class NewsDocument:
 

  def __init__(self, doc_ID, tokens, all_docs_count):

    self.doc_ID = doc_ID
    self.tokens = tokens
    self.docs_count = all_docs_count


    
  def calculate_tfidf(self, word, document_frequncy_of_word):
    term_frequency = self.tokens.count(word)
    return (1 + math.log(term_frequency)) * math.log((self.docs_count/document_frequncy_of_word)) if term_frequency > 0 else 0
  
  def create_vector(self, dictionary):
    self.vector_list = []

    for key in list(dictionary):
      self.vector_list.append(self.calculate_tfidf(key, dictionary[key]))
    
    self.vector = np.array(self.vector_list)
    
    # if not np.any(self.vector):
    #   return -1
    # return 0

  def get_doc_ID (self):
    return self.doc_ID

  def get_vector (self):

    return self.vector


  def find_cosine_distance_from_query(self, query_vector):

  
    return np.dot(self.vector,query_vector) / (LA.norm(self.vector) * LA.norm(query_vector))


  def find_cosine_distances_from_all_news(self, all_news):

      self.news_cosines_distances = {}

      for news in all_news:
        news_vector = news.get_vector()
        self.news_cosines_distances[news] = np.dot(self.vector,news_vector) / (LA.norm(self.vector) * LA.norm(news_vector))


  def get_top_nearest_news(self, count):
    # print(self.title)
    top_news = nlargest(count, self.news_cosines_distances, key = self.news_cosines_distances.get)
    # print(top_journals.values())
    # print(top_journals[0].get_title())
    values =[]
    for news in top_news:
      values.append(self.news_cosines_distances[news])

    return top_news,values