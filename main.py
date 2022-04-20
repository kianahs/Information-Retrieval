
from __future__ import unicode_literals
import re
from unittest import result
from hazm import *
import json
 
class word_postings_element:
  def __init__(self, word, frequency, doc_element):
    self.word = word
    self.frequency = frequency
    self.postings_set = set()
    self.postings_set.add(doc_element)
  
  def __str__(self):

    postings_string = ""

    for doc_item in self.postings_set:

      postings_string += doc_item.__str__() 
    return "frequency: "+str(self.frequency) + "\npostings list:\n" + postings_string

  def add_new_doc(self, new_doc_element):
    self.postings_set.add(new_doc_element)
    self.frequency += 1

  def get_word_name(self):
    return self.word

  def get_doc_element(self, doc_ID):

    for doc_item in self.postings_set:
      if doc_item.get_doc_ID() == doc_ID:
        return doc_item
    return None

  def get_postings_set_info(self):

    result = set()
    for doc_element in self.postings_set:
      result.add(doc_element.get_doc_info())
    return result
 
class doc_element:

  def __init__(self, doc_ID, word_index, doc_title, doc_url):
    self.doc_ID = doc_ID
    self.word_positions = set()
    self.word_positions.add(word_index)
    self.doc_title = doc_title
    self.doc_url = doc_url

  def add_new_position_for_word(self,word_index):
    self.word_positions.add(word_index)
  
  def get_doc_ID(self):
    return self.doc_ID
  
  def __str__(self):
      return str(self.doc_ID) + ":" + str(self.word_positions) + "\n"
  
  def get_doc_info(self):
    return "doc_ID:  " + str(self.doc_ID) + "   title:  " + str(self.doc_title) + "   Url:  " + str(self.doc_url)

def print_dict():
  for word in words_dictionary:
    print("----------------------------------------------------\n")
    print(word)
    print(words_dictionary[word].__str__())
    print("----------------------------------------------------\n")



f = open('data/sample.json', encoding='utf-8')
words_dictionary = {}

all_documents = json.load(f)

normalizer = Normalizer()
lemmatizer = Lemmatizer()
# tagger = POSTagger(model='resources/postagger.model')

stop_words_list = stopwords_list()

for doc_ID in all_documents: 
  tokens = word_tokenize(normalizer.normalize(all_documents[doc_ID]["content"]))
  
  for token in tokens:
    if token in stop_words_list:
      tokens.remove(token)

  root_tokens = list(map(lambda word: lemmatizer.lemmatize(word), tokens))
 
  # print(tokens)
  word_index =  0
  for word in root_tokens:
    if word in words_dictionary:
      related_doc_element = words_dictionary[word].get_doc_element(doc_ID)

      if related_doc_element is None:

        new_doc_item = doc_element(doc_ID, word_index, all_documents[doc_ID]["title"],all_documents[doc_ID]["url"])
        words_dictionary[word].add_new_doc(new_doc_item)

      else:

        related_doc_element.add_new_position_for_word(word_index)

    else:
      new_doc_item = doc_element(doc_ID, word_index, all_documents[doc_ID]["title"],all_documents[doc_ID]["url"])
      words_dictionary[word] = word_postings_element(word,1,new_doc_item)
    word_index += 1
  
  # words_list[news_ID] = data[news_ID]["content"]
f.close()
# print_dict()

# preprocess query
query = "تهران !پیکان"
query_tokens = word_tokenize(normalizer.normalize(query))

for token in query_tokens:
    if token in stop_words_list:
      query_tokens.remove(token)

not_tokens_list = []

flag = False
for token in query_tokens.copy():
  if flag == True:
    not_tokens_list.append(token)
    flag == False
    query_tokens.remove(token)
  if token == "!":
    flag = True
    query_tokens.remove(token)




final_query = list(map(lambda word: lemmatizer.lemmatize(word), query_tokens))
not_final_query = list(map(lambda word: lemmatizer.lemmatize(word), not_tokens_list))
print(final_query, not_final_query)
 
#find result
not_result = set()
for query_word in not_final_query:
  if query_word in words_dictionary:
   
    not_result.update(words_dictionary[query_word].get_postings_set_info())
    


result = set()

for query_word in final_query:

  if query_word in words_dictionary:
    # print("yesss")

    if len(result) == 0:
      result.update(words_dictionary[query_word].get_postings_set_info())
      # print(result)
      # print(words_dictionary[query_word].get_postings_set_info())
    else:
      result.intersection_update(words_dictionary[query_word].get_postings_set_info())
      # print(result)
result.difference_update(not_result)
print(result)
