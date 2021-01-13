# Only needed when script is run from within Rstudio #
#reticulate::use_condaenv(condaenv = 'cas-text-analytics')
#reticulate::repl_python()
#exit

# Usage
# type in terminal:
# python calculate_entity_counts.py n # n = nr_months (integer); max is 240.
# For 240 months the runtime is ~ 1.5 h.

# Imports
from pathlib import Path
from sys import argv
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

def get_entities_count(date):
    """
    Parameters
    ----------
    date : str
        The folder name with the articles (.json) of a specific month.
    topN: int
        An integer (N) restricting the output to the top N
        most frequent entities per article.
        If N > than the max number of entities, N will be the max number of
        entites in that text.
    Returns
    -------
    str
        a string containing the names of the topN entities mentionned in the
        Guardian news articles of a month (date).
    """
    ## Load the .json
    jsons = os.listdir(articles_path / date)
    dictsList = []
    for _json in jsons:
        with open(articles_path / date / _json, mode='r', encoding='utf-8') as file:
            tmp = json.load(file)
        dictsList.append(tmp)
        
    ## Defining two dictionaries, one for raw text, one for meta data
    articlesRaw = {}
    for nr, _dict in enumerate(dictsList):
        rawTxt = _dict['response']['content']['fields']['bodyText']
        articlesRaw[nr] = rawTxt
        
    ## Name Entities Extraction
    entities = []
    for article in articlesRaw:
        tmpOutput = nlp(articlesRaw[article])
        filterList = ['CARDINAL', 'DATE', 'PERCENT', 'QUANTITY', 'ORDINAL', \
                      'MONEY', 'TIME']
        tmpEntities = [x.text for x in tmpOutput.ents \
                       if x.label_ not in filterList]
        entities += tmpEntities

    # Create a collections.Counter object and convert it to a dictionary
    output = dict(Counter(entities))
    
    return output


def create_csv(nr_months):
    """Wrapper for get_entities_count(). Loops through all articles (jsos) and
    produces one dictionary vector per month with the entity counts. Saves the 
    output to a csv file (in the project folder). Use argument nr_months to 
    define the number of months you'd like to include (max 240).
    """
    all_dates = os.listdir(articles_path)
    header = ['month', 'entities']
    output = []
    for date in all_dates[:nr_months]:
        output.append([date[:-3], get_entities_count(date)])
    if nr_months == len(all_dates):
        nr_months = "all"
    file = open(csv_path / f'count_vectors_{nr_months}.csv', mode='w+', \
                newline='', encoding='utf-8')
    with file:
        write = csv.writer(file)
        write.writerow(header)
        write.writerows(output)


if __name__ == "__main__":
    script, nr_months = argv
    nr_months = int(nr_months)
    create_csv(nr_months)
