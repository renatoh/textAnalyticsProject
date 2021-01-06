# Only needed when script is run from within Rstudio #
#reticulate::use_condaenv(condaenv = 'cas-text-analytics')
#reticulate::repl_python()
#exit

# Imports
from pathlib import Path
import os
import json
import csv
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()


# Define paths

articles_path = Path("../resources/articles")
csv_path = Path("../resources")


# Define functions

def get_entities(date):
    """
    Parameters
    ----------
    date : str
        The folder name with the articles (json) of a specific month.

    Returns
    -------
    str
        a string containing the names of the entities mentionned in the
        Guardian news articles of a month (date argument).
    """
    ## Load the jsons
    jsons = os.listdir(articles_path / date)
    dictsList = []
    for _json in jsons:
        with open(articles_path / date / _json, mode='r', encoding='utf-8') \
        as file:
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
        
    ## Name Entities Extraction
    entities = []
    for article in articlesRaw:
        tmpOutput = nlp(articlesRaw[article])
        filterList = ['CARDINAL', 'DATE', 'PERCENT', 'QUANTITY', 'ORDINAL', \
                      'MONEY', 'TIME']
        tmpEntities = [x.text for x in tmpOutput.ents \
                       if x.label_ not in filterList]
        entities += tmpEntities
    output = " ".join(entities) # Could use another separator than whitespace.
    return output

def create_csv():
    """Wrapper for get_entities(). Loops through all articles (jsos) and 
    produces one string vector per month with the entities. Saves the output to 
    a csv file (in the project folder).
    """
    all_dates = os.listdir(articles_path)
    header = ['month', 'entities']
    output = []
    for date in all_dates[0:11]:
        output.append([date[:-3], get_entities(date)])
    file = open(csv_path / 'entity_vectors.csv', mode='w+', newline='', \
                encoding='utf-8')
    with file:
        write = csv.writer(file)
        write.writerow(header)
        write.writerows(output)
        

if __name__ == "__main__":
    create_csv()
