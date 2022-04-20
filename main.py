
from __future__ import unicode_literals
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
 
 
    


class doc_element:

  def __init__(self, doc_ID, word_index):
    self.doc_ID = doc_ID
    self.word_positions = set()
    self.word_positions.add(word_index)

  def add_new_position_for_word(self,word_index):
    self.word_positions.add(word_index)
  
  def get_doc_ID(self):
    return self.doc_ID
  
  def __str__(self):
      return str(self.doc_ID) + ":" + str(self.word_positions) + "\n"

# def check_duplicate_word(words_list, word):

#   for word_element in words_list:
#       if word_element.get_word_name() == word:
#         return True
#   return False

   
f = open('data/sample.json', encoding='utf-8')
words_dictionary = {}

all_documents = json.load(f)

normalizer = Normalizer()
# tagger = POSTagger(model='resources/postagger.model')

for doc_ID in all_documents: 
  tokens = word_tokenize(normalizer.normalize(all_documents[doc_ID]["content"]))
  # print(tokens)
  word_index =  0
  for word in tokens:
    if word in words_dictionary:
      related_doc_element = words_dictionary[word].get_doc_element(doc_ID)

      if related_doc_element is None:

        new_doc_item = doc_element(doc_ID, word_index)
        words_dictionary[word].add_new_doc(new_doc_item)

      else:

        related_doc_element.add_new_position_for_word(word_index)

    else:
      new_doc_item = doc_element(doc_ID, word_index)
      words_dictionary[word] = word_postings_element(word,1,new_doc_item)
    word_index += 1
  
  # words_list[news_ID] = data[news_ID]["content"]

for word in words_dictionary:
  print("----------------------------------------------------\n")
  print(word)
  print(words_dictionary[word].__str__())
  print("----------------------------------------------------\n")

f.close()

