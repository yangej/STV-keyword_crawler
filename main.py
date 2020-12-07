from modules.getAllLinks import getAllLinks
from modules.getKeywords import getKeywords

def main():
    # get all article links from the website
    links = getAllLinks()
    # generate keyword file into /data
    getKeywords(links)

main()
