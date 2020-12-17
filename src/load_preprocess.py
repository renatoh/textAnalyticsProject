# Only needed in Rstudio #
#reticulate::use_condaenv(condaenv = 'cas-text-analytics')
#reticulate::repl_python()
#exit

# 1) Loading the data

## Imports
from pathlib import Path
import os
import json

## Define project folder
project_path = Path("C:/Users/Urs/Documents/DS Projects/CAS MAIN/Text Analytics Project/")

## Load the .json
jsons = os.listdir(project_path / 'jsons')
dictsList = []
for _json in jsons:
    with open(project_path / 'jsons' / _json, mode='r', encoding='utf-8') as file:
        tmp = json.load(file)
    dictsList.append(tmp)

   
## Defining two dictionaries, one for raw text, one for meta data
articlesRaw = {}
articlesMeta = {}
for nr, _dict in enumerate(dictsList):
    title = _dict['response']['content']['webTitle']
    section = _dict['response']['content']['sectionId']
    pubDate = _dict['response']['content']['webPublicationDate']
    rawTxt = _dict['response']['content']['fields']['bodyText']
    articlesRaw[nr] = rawTxt
    articlesMeta[nr] = [title, section, pubDate]
    
# 2) Name Entities Extraction

## Imports
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

## Test nlp on one article
test = nlp(articlesRaw[0])

## Print all entity names and categories in test article
print([(X.text, X.label_) for X in test.ents])

## Count the entities by category
labels = [x.label_ for x in test.ents]
Counter(labels)

## Get the 10 most frequent entities
entities = [x.text for x in test.ents]
Counter(entities).most_common(10)

## Display/mark entities in a sentence (works in jupyter only)
sentences = [x for x in test.sents]
print(sentences[20])
displacy.render(nlp(str(sentences[20])), jupyter=True, style='ent')
