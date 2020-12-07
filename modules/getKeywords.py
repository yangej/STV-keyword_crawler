import requests
import os.path
import re
import csv
import time
from bs4 import BeautifulSoup

def writeKeywordFile(tags):
    dirPath = os.path.abspath(os.getcwd()) + '/data'
    time = datetime.now().strftime("%Y%m%d")
    file = time + '_keywords.csv'
    path = os.path.join(dirPath, file)

    keys = tags.keys()

    with open(path, 'w', encoding = 'utf-8', newline = '') as outfile:
        fieldNames = ['keywords', 'count', 'link']
        writer = csv.DictWriter(outfile, fieldnames = fieldNames)

        writer.writeheader()

        for key in keys:
            writer.writerow({ 'keywords': key, 'count': tags[key]['count'], 'link': tags[key]['link']})

def getKeywords(links):
    tags = {}
    regex = r'\(\d+\)'

    all = len(links)
    current = 1

    prefix = 'https://scitechvista.nat.gov.tw'

    # get tags from articles
    for link in links:
        if current % 100 == 0:
            time.sleep(2)
            print('sleeping!')

        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        tagTitle = soup.find(class_ = 'ul-title same_line tag')

        if tagTitle != None:
            aList = tagTitle.find_all('a')

            for a in aList:
                tag = re.sub(regex, '', a.text)
                link = prefix + a.get('href')

                if tags.get(tag) == None:
                    tags[tag] = { 'count': 1, 'link': link }
                else:
                    tags[tag]['count'] += 1

        print('Working progress: ' + str(current) + '/' + str(all))
        current += 1

    # write tag infos into file
    writeKeywordFile(tags)