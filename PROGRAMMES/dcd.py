# -*- coding: utf-8 -*-

import re
import copy

def read_text(file_path):
  with open(file_path, "r", encoding="utf-8") as f:
      return f.read()

def read_lexicon(file_path):
  with open(file_path, "r", encoding="ISO-8859-1") as f:
      return [line.strip() for line in f]
      
def dict_transform_lexicon(lexicon):
    result = {}
    for element in lexicon:
        mot = element.split('\t')[0]
        if len(element.split('\t')) == 2:
            etiquette = element.split('\t')[1]
            if mot not in result:
                result[mot] = etiquette
        elif len(element.split('\t')) > 2 :
            elements = element.split('\t')
            elements.pop(0)
            if mot not in result:
                result[mot] = elements
            # print(elements)
    # print(result)
    return result
    
def increment_occurrence(word, dict, tag):
      if tag not in dict:
        dict[tag] = {}
      if word not in dict[tag]:
          dict[tag][word] = 1
      else:
          dict[tag][word] += 1

def clean_line(line):
    return re.split(r"( |,|\"|!|\?|:|;|\.|j'|J'|t'|T'|n'|N'|l'|L'|d'|D'|s'|S'|m'|M'|c'|C'|qu'|-je|-tu|-il|-elle|-on|-nous|-vous|-ils|-elles|-t-on|-t|\(|\)|\[|\])", line)
  
def find_in_text(text, lexicon, tags):
  #print(lexicon)
  verbs = {}
  for line in text.split("\n"):
      #print(line)
      words = clean_line(line)
      while (" " in words):
        words.remove(" ")
      while ("" in words):
        words.remove("")
      # print(words)
      for word in words:
          # print(word)
          if word in lexicon.keys():
              for tag in tags:
                if tag in lexicon[word]:
                    increment_occurrence(word, verbs, tag)
  return verbs
  
def trier_dictionnaire(dictionnaire):
    def key_func(item):
        return item[0]
    return dict(sorted(dictionnaire.items(), key=key_func))
  
def output_result(dict, output_file_path):
    with open(output_file_path, "w") as f:
        for tag in dict:
            dict[tag] = trier_dictionnaire(dict[tag])
            for word in dict[tag]:
                    f.write(f"{word}\t{tag}\t{dict[tag][word]}\n")
                    
def output_result_bis(dict, output_file_path):
    with open(output_file_path, "w") as f:
        for segment in dict:
                    f.write(f"{segment}\t{dict[segment]}\n")

def merge_result(res1, res2, number):
    dict1 = read_lexicon(res1)
    dict1 = dict_transform_lexicon(read_lexicon(res1))
    dict2 = dict_transform_lexicon(read_lexicon(res2))
    # print(dict1)
    dict3 = {}
    for key in dict1.keys():
        if key in dict2.keys():
            dict3[key] = { dict1[key][0]: str(int(dict1[key][1]) + int(dict2[key][1])) }
        else:
            dict3[key] = { dict1[key][0]: dict1[key][1] }
    for key in dict2.keys():
        if key not in dict1.keys():
            dict3[key] = { dict2[key][0]: dict2[key][1] }
    print(dict3)
    output_result(dict3, "RESULTATS/merge_quest" + str(number) + "_verne.txt")
    return dict3
    
def merge_result_bis(res1, res2):
    dict1 = read_lexicon(res1)
    dict1 = dict_transform_lexicon(read_lexicon(res1))
    dict2 = dict_transform_lexicon(read_lexicon(res2))
    # print(dict1)
    dict3 = {}
    for key in dict1.keys():
        if key in dict2.keys():
            dict3[key] = str(int(dict1[key]) + int(dict2[key]))
        else:
            dict3[key] = dict1[key]
    for key in dict2.keys():
        if key not in dict1.keys():
            dict3[key] = dict2[key]
    print(dict3)
    output_result_bis(dict3, "RESULTATS/merge_quest4_verne.txt")
    return dict3
    
def check_tag(tags1, tags2):
    for tag1 in tags1:
        if tag1 in tags2:
            return True
    return False

def find_segment_in_text(text, lexicon):
  tags_prv = ['PRV:sg', 'PRV:pl']
  tags_ecj = ['ECJ:sg', 'ECJ:pl', 'ACJ:sg', 'ACJ:pl']
  tags_par = ['VPAR:sg', 'VPAR:pl', 'ADJ1PAR:sg', 'ADJ2PAR:sg', 'ADJ2PAR:pl']
  segment_word = []
  segment_tag = []
  res = []
  for line in text.split("\n"):
      if len(segment_tag) == 3:
        segment_word.pop(0)
        segment_tag.pop(0)
      words = clean_line(line)
      while (" " in words):
        words.remove(" ")
      while ("" in words):
        words.remove("")
        
      for word in words:

          if len(segment_tag) == 3:
            counter = 0
            for i in range(len(segment_tag)):
                for tag in segment_tag[i]:
                    if i == 0 and check_tag(tags_prv, tag):
                        counter += 1
                    if i == 1 and check_tag(tags_ecj, tag) and counter == 1:
                        counter += 1
                    if i == 2 and check_tag(tags_par, tag) and counter == 2:
                        counter += 1
                        # print("hhhhh"+str(segment_tag))
                        res.append(copy.deepcopy(segment_word))
                        # print("hhhhh"+str(segment_word))
            segment_word.pop(0)
            segment_tag.pop(0)

          if word in lexicon.keys():
            segment_word.append(word)
            if type(lexicon[word]) is not list:
                segment_tag.append([lexicon[word]])
            else:
                segment_tag.append(lexicon[word])
          else:
            segment_word.append(word)
            segment_tag.append(['MOT_INCONNU'])
          
  # print(res)
  dict = {}
  for elt in res:
    if str(elt) not in dict.keys():
        dict[str(elt)] = 1
    else:
        dict[str(elt)] += 1
  print(dict)
  return dict


###


corpus = ["les_revoltes_de_La_bounty_texte.txt", "le_tour_du_monde_texte.txt", "memoires_dun_touriste_texte.txt"]
lexicon_file_path = "etiquettes_utf8.txt"

# Question 2
for text in corpus:
    tags = ["VNCFF", "ANCFF", "ENCFF"]
    verbs_at_infinitive = find_in_text(read_text("TEXTES/" + text), dict_transform_lexicon(read_lexicon(lexicon_file_path)), tags)
    print(verbs_at_infinitive)
    output_result(verbs_at_infinitive, "RESULTATS/" + "infinitive_verbs_" + text)
    

merge_result("RESULTATS/infinitive_verbs_le_tour_du_monde_texte.txt", "RESULTATS/infinitive_verbs_les_revoltes_de_La_bounty_texte.txt", 2)


# Question 3 

for text in corpus:
    tags = ["VCJ:pl", "VCJ:sg", "VPAR:sg", "ADJ1PAR:sg", "ADJ1PAR:pl", "ADJ2PAR:sg", "ADJ2PAR:pl", "VPAR:pl", "VNCFF", "VNCNT", "ECJ:pl", "ACJ:pl", "ECJ:sg", "ACJ:sg", "ENCFF", "APAR:sg", "EPAR:sg", "ENCNT", "APAR:pl", "ANCNT", "ANCFF"]
    verbs = find_in_text(read_text("TEXTES/" + text), dict_transform_lexicon(read_lexicon(lexicon_file_path)), tags)
    print(verbs)
    output_result(verbs, "RESULTATS/" + "any_verbs_" + text)
    
merge_result("RESULTATS/any_verbs_le_tour_du_monde_texte.txt", "RESULTATS/any_verbs_les_revoltes_de_La_bounty_texte.txt", 3)


# Question 4

for text in corpus:
    print('text')
    segments = find_segment_in_text(read_text("TEXTES/" + text), dict_transform_lexicon(read_lexicon(lexicon_file_path)))
    output_result_bis(segments, "RESULTATS/" + "segment_" + text)
    
    
merge_result_bis("RESULTATS/segment_le_tour_du_monde_texte.txt", "RESULTATS/segment_les_revoltes_de_La_bounty_texte.txt")