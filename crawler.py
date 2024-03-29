import requests
import pandas as pd
import multiprocessing
import parmap
from bs4 import BeautifulSoup
from article import ArticleCrawler
from writer import Writer

def crawl_data(index : int, base_url: str) -> list :
    try :
        url = base_url + '?page=' + str(index)
        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'html.parser')

        page_url = bs.find('link' , {'rel' : 'canonical'})
        page_url = page_url['href']            

        article_info = bs.findAll('a', {'data-link-name' : 'article'})
        article_list = [article['href'] for article in article_info]
        article_list = list(set(article_list))        
        return article_list
    except :
        return None

def save_data(article_url: str, article_crawler: ArticleCrawler, writer: Writer) -> tuple :
    try :
        article_info = article_crawler(article_url)
        article_data = writer(article_info)
        return article_data
    except :
        return None

if __name__ == '__main__' :
    DATA_SIZE = 1900
    BASE_URL = 'https://www.theguardian.com/'
    CATEGORY = ['world', 
        'world/europe-news',
        'uk-news', 
        'technology' , 
        'business' , 
        'environment' , 
        'environment/climate-crisis',
        'science',
        'culture',
        'global-development',
        'technology',
        'sport',
        'world/coronavirus-outbreak'
    ]

    num_cores = multiprocessing.cpu_count() // 2
    print('The number of Cores : %d \n' %num_cores)

    article_data = []
    for cate in CATEGORY :
        print('Category : %s' %cate)
        url = BASE_URL+cate
        article_list = parmap.map(crawl_data, range(1,DATA_SIZE+1), url, pm_pbar=True, pm_processes=num_cores) 

        article_list = [article for article in article_list if article != None]
        article_list = sum(article_list, [])
        article_data.extend(article_list)
        print('Size of articles : %d\n' %len(article_list))
        
    article_data = list(set(article_data))
    print('Total size of data : %d ' %len(article_data))

    article_df = pd.DataFrame({'ID' : range(1, len(article_data)+1), 'URL' : article_data})
    article_df.to_csv('./Info/theguardians_article_url.csv')

    article_df = pd.read_csv('./Info/theguardians_article_url.csv')
    article_data = list(article_df['URL'])
    print('Size of articles : %d' %len(article_data))

    article_crawler = ArticleCrawler()
    writer = Writer('./Data')

    article_info = parmap.map(save_data, article_data, article_crawler, writer, pm_pbar=True, pm_processes=4) 
    article_info = [info for info in article_info if info != None]
    print('Size of articles (Saved) : %d' %len(article_info))

    info_df = pd.DataFrame(article_info, columns=['title', 'date', 'category', 'text'])
    info_df.to_csv('./Info/theguardians_article_info.csv')
    