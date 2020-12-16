import json
import requests

# url = 'https://content.guardianapis.com/search'
# api_key = '?pages=30&api-key=389d51f6-216c-4143-a91e-500a36e3303d'


api_key = 'api-key=389d51f6-216c-4143-a91e-500a36e3303d'
url1 = 'https://content.guardianapis.com/search?page-size=50&page=1&%s' % api_key


def do_http_call(url_to_call):
    response = requests.get(url_to_call)
    response.raise_for_status()
    return response.json()

def write_json_to_file(file_name, json_content):
    with open('../resources/articles/2020-03-01/'+file_name, 'w') as f:
        json.dump(json_content, f)

url_with_filter = ('https://content.guardianapis.com/search?page-size=50&page=%s&' + api_key + '&to-date=2020-03-30&from-date=2020-03-01')
url_details = 'https://content.guardianapis.com/politics/live/2020/dec/15/uk-coronavirus-live-covid-christmas-rules-restrictions-brexit-latest-updates?show-fields=bodyText,headline&%s' % api_key

initial_result = do_http_call(url_with_filter % str(1))

nr_pages = int(initial_result['response']['pages'])

for i in range(1, nr_pages + 1):
    print("nr of pages:" + str(i)+ " of "+ str(nr_pages))
    search_result = do_http_call(url_with_filter % str(i))

    for result in search_result['response']['results']:

        api_url = result['apiUrl']
        print('calling:' + api_url)
        article = do_http_call(api_url + '?' + api_key +'&show-fields=bodyText,headline')
        id = article['response']['content']['id']
        id = id.replace('/','-') # we do not want to have '/' in the file name
        write_json_to_file(id + '.json', article)

