# Old script. Not used in final analysis.
# Reference: https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da, 15.1.2021.

# Imports
from sys import argv
from pathlib import Path
import os
import json
import csv
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

# Set argv to directly run script from console/shell using:
# python load_preprocess.py n
# where n = some integer representing the topN entities.

script, topN = argv

topN = int(topN)


# Define paths

articles_path = Path("../resources/articles")
csv_path = Path("../resources")


# Define functions

def get_entities(date, topN):
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
        A string containing the names of the topN entities mentionned in the
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
        tmpEntities = [(x.text, x.label_) for x in tmpOutput.ents \
                       if x.label_ not in filterList]
        entities += tmpEntities

    # Create a collections.Counter object
    # Use method .most_common(n) to get the n most common entities
    # or use entitiesCount[key] to get the count for a specific entity.
    entitiesCount = Counter(entities)
    # Get the entity name, label and count of the topN entities in this month.
    fullOut = entitiesCount.most_common(topN)
    # Reduce fullOut to output only a string of topN entity names.
    entityString = ""
    for entity in fullOut:
        entityString += entity[0][0] + " "
    output = entityString.rstrip()

    return output

def create_csv(topN):
    """Wrapper for get_entities(). Loops through all articles (jsos) and produces
    one vector per month with the topN entities. Saves the output to a
    csv (in the project folder).
    """
    all_dates = os.listdir(articles_path)
    header = ['month', 'entities']
    output = []
    for date in all_dates[0:11]:
        output.append([date[:-3], get_entities(date, topN)])
    file = open(csv_path / 'entity_vectors.csv', mode='w+', newline='', encoding='utf-8')
    with file:
        write = csv.writer(file)
        write.writerow(header)
        write.writerows(output)


if __name__ == "__main__":
    create_csv(topN)
