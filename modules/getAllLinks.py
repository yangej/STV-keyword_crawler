import requests
from bs4 import BeautifulSoup
import os.path

def getLinks(soup, prefix, links):
    boxes = soup.find_all(class_='pic_box1 pull-left')

    hrefs = []
    for box in boxes:
        aList = box.find_all('a')
        for a in aList:
            hrefs.append(a.get('href'))

    for href in hrefs:
        links.append(prefix + href)

    return links

def getTotalPage(soup, articlePerPage):
    articleNum = int(soup.find(id='ctl00_html_content_RadListView1_RadDataPager1_ctl03_TotalItemsLabel').text)
    totalPage = 0

    if articleNum % articlePerPage != 0:
        totalPage = articleNum / articlePerPage + 1
    else:
        totalPage = articleNum / articlePerPage

    return int(totalPage)

def getAllLinks():
    articlePerPage = 6
    nodePrefix = 'https://scitechvista.nat.gov.tw/subject_classification.aspx?subject='
    nodePostfix = '_' + str(articlePerPage)
    subjects = [
        'UwAxAFoAQQB0AFMARgBwAFIAeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'VABVAFoAQQBtAFUAbQBWAFIAeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'UwBEAE4AQQBXAGMARwBOAG4AeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'WQBWAGgAQQBKAFIAMgBSAEIAeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'UgBtAHgAQQBPAE4ARgBkADMAeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'WgBVAGQAQQBXAE4ARgBkADMAeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'YwBUAFYAQQBHAFEAMgBSAG4AeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'ZAB6AEUAQQA0AFIAMgBSAEIAeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'TQBGAGgAQQB0AFEAVgBsAG4AeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'YwAwAGgAQQBUAFIARgBkAEIAeABLADAARgBFAE0ARQBGAFEAVQBTADAAIQA!&RadListView1=',
        'ZABXAHMAQQAxAFoAVwAxAEoAeABaAEcAeABFAGIAVgBrAHIAUQBVAFEAdwBMAFEAIQAhAA!!&RadListView1=',
        'VQBHADUAQQByAFIARgBvADUAeABSAGoAVgBsAFIAbgBNAHIAUQBVAFEAdwBMAFEAIQAhAA!!&RadListView1=',
        'UwBEAE4AQQBWAE4AMgBKAGsAeABSAGoAVgBsAFIAbgBNAHIAUQBVAFEAdwBMAFEAIQAhAA!!&RadListView1='
    ]

    prefix = 'https://scitechvista.nat.gov.tw/article'
    links = []
    subjectCount = 0

    dirPath = os.path.abspath(os.getcwd()) + '/data'
    file = 'links.txt'
    path = os.path.join(dirPath, file)

    for sub_i in range(0, len(subjects)):
        url = nodePrefix + subjects[sub_i] + '1' + nodePostfix
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        totalPage = getTotalPage(soup, articlePerPage)

        print('read subject: ' + str(sub_i) + ' ;has page: ' + str(totalPage))

        for i in range(1, totalPage + 1):
            currentPage = str(i)
            url = nodePrefix  + subjects[sub_i] +  currentPage + nodePostfix
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            tempLinks = getLinks(soup, prefix, links)

        links = links + tempLinks

    return links