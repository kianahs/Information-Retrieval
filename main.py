
from __future__ import unicode_literals
import re
from unittest import result
from hazm import *
import json
import re
from itertools import combinations
 
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
 
  def get_postings_doc_IDs(self):

    result = set()
    for doc_element in self.postings_set:
      result.add(doc_element.get_doc_ID())
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

  def get_word_positions(self):
    return self.word_positions

def print_dict():
  for word in words_dictionary:
    print("----------------------------------------------------\n")
    print(word)
    print(words_dictionary[word].__str__())
    print("----------------------------------------------------\n")

def check_order_in_positions(positions_list):

  count = len(positions_list)-1
  for i in range(len(positions_list)):

    if i != len(positions_list)-1:

      for j in range(i+1, len(positions_list)):

        for element in positions_list[i]:

          if check_element_is_in_list(positions_list[j],element+1):
            print("order!")
            count -= 1
            break

  if count == 0:
    return True
  return False

def check_element_is_in_list(taregt_list, element):
  if element in taregt_list:
    return True
  return False

def get_and_queries_result(final_query_combinations_list, words_dictionary):
 
  full_result = set()
 
  for final_query in final_query_combinations_list:
      result = set()
      for query_word in final_query:
        # print(query_word)
        if query_word in words_dictionary:
          # print("yesss")

          if len(result) == 0:
            result.update(words_dictionary[query_word].get_postings_set_info())
            # print(result)
            # print(words_dictionary[query_word].get_postings_set_info())
          else:
            result.intersection_update(words_dictionary[query_word].get_postings_set_info())
        else:
          result.clear()
          break
        
        full_result.update(result)

  # print("res ", full_result)
  return full_result

def preprocess_input_query():

  # preprocess query
  query = input("enter your query\n")
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

  qutation_indexes = [m.start() for m in re.finditer('"', query)]
  statement = "" 
  if qutation_indexes:
    statement = query[qutation_indexes[0]+1:qutation_indexes[1]]

  statement_tokens = word_tokenize(normalizer.normalize(statement))


  final_query = list(map(lambda word: lemmatizer.lemmatize(word), query_tokens))
  not_final_query = list(map(lambda word: lemmatizer.lemmatize(word), not_tokens_list))
  statement_query = list(map(lambda word: lemmatizer.lemmatize(word), statement_tokens))

  for item in statement_query:
    final_query.remove(item)
  if '«' in final_query or '»' in final_query:
    final_query.remove('«')
    final_query.remove('»')
  print(final_query, not_final_query, statement_query)
  return final_query, not_final_query, statement_query

def find_results(words_dictionary):
  #find result

  final_query, not_final_query, statement_query = preprocess_input_query()

  if len(statement_query) == 0 and len(not_final_query) == 0:
      number_of_combinations = len(final_query)
      ranked_result = {}
      # print()
      rank = 1
    
      for i in range(number_of_combinations, 0 , -1):
        ranked_result["rank {}".format(rank)] = get_and_queries_result(list(combinations(final_query, i)), words_dictionary)
        rank += 1

      print(ranked_result)


  else:

    # not queries
    not_result = set()
    for query_word in not_final_query:
      if query_word in words_dictionary:
      
        not_result.update(words_dictionary[query_word].get_postings_set_info())
        

    # and queries
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

      else:
        result.clear()
        break
    # result.difference_update(not_result)

    # print(result)

    # statement queries
    statement_result = set()
    final_statement_result = set()
    statement_result_info = set()
    for query_word in statement_query:

      if query_word in words_dictionary:
        # print("yesss")

        if len(statement_result) == 0:
          statement_result.update(words_dictionary[query_word].get_postings_doc_IDs())
          # print(statement_result)
          # print(words_dictionary[query_word].get_postings_doc_IDs())
        else:
          statement_result.intersection_update(words_dictionary[query_word].get_postings_doc_IDs())
          # print(statement_result)
    if len(statement_result) > 0:

      for result_id in statement_result:
        words_positions_in_single_doc = []
        for word_statement in statement_query:
          words_positions_in_single_doc.append(list(words_dictionary[word_statement].get_doc_element(result_id).get_word_positions()))
        # print(words_positions_in_single_doc)
        if check_order_in_positions(words_positions_in_single_doc) == True:
          print("order found in doc_id: {}".format(result_id))
          final_statement_result.add(result_id)
      
      print("order check finished")

    #processing final result

    if len(final_statement_result) > 0:
      for doc_id in final_statement_result:
        statement_result_info.add(words_dictionary[statement_query[0]].get_doc_element(doc_id).get_doc_info())

    if len(result) > 0 and len(final_statement_result)> 0:  
      result.intersection_update(statement_result_info)
    else:
      result.update(statement_result_info)

    result.difference_update(not_result)
    print(result)



# f = open('data/sample.json', encoding='utf-8')
f = open('data/IR_data_news_12k.json', encoding='utf-8')

words_dictionary = {}

all_documents = json.load(f)

normalizer = Normalizer()
lemmatizer = Lemmatizer()
# tagger = POSTagger(model='resources/postagger.model')

stop_words_list = stopwords_list()

for doc_ID in all_documents:
  print(doc_ID) 
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
while True:
  find_results(words_dictionary)

