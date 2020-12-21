import json
import os

import requests
import uuid

# url = 'https://content.guardianapis.com/search'
# api_key = '?pages=30&api-key=389d51f6-216c-4143-a91e-500a36e3303d'
years = ['2002','2001']
# years = ['2004','2003','2002','2001']
api_key = 'api-key=389d51f6-216c-4143-a91e-500a36e3303d'
url1 = 'https://content.guardianapis.com/search?page-size=50&page=1&%s' % api_key


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def do_http_call(url_to_call):
    response = requests.get(url_to_call)
    response.raise_for_status()
    return response.json()


def write_json_to_file(json_content, start_date):
    dic = '../resources/articles/' + start_date + '/'
    ensure_dir(dic)
    with open(dic + str(uuid.uuid4()) + '.json', 'w') as f:
        json.dump(json_content, f)


def add_leading_zero(i):
    return "0" + str(i) if i < 10 else i


def download_content_for_year(current_year):
    for i in range(1, 1q3):

        month = add_leading_zero(i)

        days_of_month = [1, 5, 9, 11, 13, 16, 19, 20, 24, 28]
        # days_of_month = [1,3,5,6,8,10,9,11,13,16]

        folder_name = current_year + '-' + str(month) + '-01'

        for day in days_of_month:

            day = add_leading_zero(day)

            start_date = current_year + '-' + str(month) + '-' + str(day)
            end_date = current_year + '-' + str(month) + '-' + str(day)
            url_with_filter = (
                    'https://content.guardianapis.com/search?page-size=20&page=%s&' + api_key + '&from-date=' + start_date + '&to-date=' + end_date)
            url_details = 'https://content.guardianapis.com/politics/live/2020/dec/15/uk-coronavirus-live-covid-christmas-rules-restrictions-brexit-latest-updates?show-fields=bodyText,headline&%s' % api_key

            initial_result = do_http_call(url_with_filter % str(1))

            nr_pages = int(initial_result['response']['pages'])

            print("current date:%s-%s-%s" % (str(current_year), str(month), day))

            search_result = do_http_call(url_with_filter % str(1))

            for result in search_result['response']['results']:

                api_url = result['apiUrl']
                print('calling:' + api_url)
                try:
                    article = do_http_call(api_url + '?' + api_key + '&show-fields=bodyText,headline')
                    # id = article['response']['content']['id']
                    # id = id.replace('/','-') # we do not want to have '/' in the file name
                    write_json_to_file(article, folder_name)
                except requests.HTTPError as e:
                    print("error in call to" + api_url)

for year in years:
    download_content_for_year(year)
