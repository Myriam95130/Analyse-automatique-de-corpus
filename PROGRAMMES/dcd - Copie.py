def read_text(file_path):
  with open(file_path, "r", encoding="utf-8") as f:
      return f.read()

def read_lexicon(file_path):
  with open(file_path, "r", encoding="utf-8") as f:
      return [line.strip() for line in f]
      
def dict_transform_lexicon(lexicon):
    result = {}
    for element in lexicon:
        mot = element.split('\t')[0]
        etiquette = element.split('\t')[1]
        if mot not in result:
            result[mot] = etiquette
    return result
    
def increment_occurrence(word, dict, tag):
      if tag not in dict:
        dict[tag] = {}
      if word not in dict[tag]:
          dict[tag][word] = 1
      else:
          dict[tag][word] += 1

def find_verbs_at_infinitive(text, lexicon):
  #print(lexicon)
  verbs_at_infinitive = {}
  for line in text.split("\n"):
      #print(line)
      delimiters = [" ","(",")","[","]","{","}",",",'"',"!","?",":",";",".","j'","t'","n'","l'","d'","s'","m'","c'","qu'","-je","-tu","-t","-il","-elle","-on","-nous","-vous","-ils","-elles"]
      parts = []
      for delimiter in delimiters:
        split_text = text.split(delimiter)
        if delimiter in split_text:
            index = split_text.index(delimiter)
            parts.extend([split_text[index], delimiter])
            text = delimiter.join(split_text[index + 1:])
        # line = " ".join(line.split(delimiter))
      parts.extend(text.split())
      words = line.split()
      print(parts)
      for word in words[1:]:
          #print(word)
          if word in lexicon.keys():
              if lexicon[word] == "VNCFF":
                increment_occurrence(word, verbs_at_infinitive, "VNCFF")
              elif lexicon[word] == "ANCFF":
                increment_occurrence(word, verbs_at_infinitive, "ANCFF")
              elif lexicon[word] == "ENCFF":
                increment_occurrence(word, verbs_at_infinitive, "ENCFF")
  return verbs_at_infinitive
  
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

###


corpus = ["les_revoltes_de_La_bounty_texte.txt", "le_tour_du_monde_texte.txt", "memoires_dun_touriste_texte.txt"]   # Remplacez par le chemin du fichier texte réel
lexicon_file_path = "etiquettes_utf8.txt"  # Remplacez par le chemin du fichier lexicon réel

for text in corpus:
    verbs_at_infinitive = find_verbs_at_infinitive(read_text("TEXTES\\" + text), dict_transform_lexicon(read_lexicon(lexicon_file_path)))
    #print(verbs_at_infinitive)
    output_result(verbs_at_infinitive,"RESULTATS\\" + text + "_result.txt")