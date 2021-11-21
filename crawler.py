import requests
import pandas as pd
import multiprocessing
import parmap
from bs4 import BeautifulSoup
from article import ArticleCrawler
from writer import Writer
from tqdm import tqdm

def crawl_data(base_url : str, size : int) -> list :
    article_data = []
    for i in tqdm(range(1,size)) :
        try :
            url = base_url + '?page=' + str(i)
    
            response = requests.get(url)
            bs = BeautifulSoup(response.text, 'html.parser')
            
            page_url = bs.find('link' , {'rel' : 'canonical'})
            page_url = page_url['href']
            
            if url != page_url :
                break
    
            article_info = bs.findAll('a', {'data-link-name' : 'article'})
        
            article_list = [article['href'] for article in article_info]
            article_list = list(set(article_list))
        
            article_data.extend(article_list)
        except :
            continue
    article_data = list(set(article_data))
    return article_data

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
        'uk-news', 
        'technology' , 
        'business' , 
        'environment' , 
        'climate-crisis',
        'science',
        'global-development',
        'technology',
        'coronavirus-outbreak'
    ]

    num_cores = multiprocessing.cpu_count()

    article_data = []
    for cate in CATEGORY :
        print('Category : %s' %cate)
        url = BASE_URL+cate
        article_list = crawl_data(url, DATA_SIZE)
        print('Size of articles : %d\n' %len(article_list))
        article_data.extend(article_list)
        
    article_data = [article for article in article_data if isinstance(article, str)]
    article_data = list(set(article_data))
    print('Total size of data : %d ' %len(article_data))
    
    article_df = pd.DataFrame({'ID' : range(1, len(article_data)+1), 'URL' : article_data})
    article_df.to_csv('./Info/theguardians_article_url.csv')
   
    article_crawler = ArticleCrawler()
    writer = Writer('./Data')

    article_info = [writer(article) for article in article_data]
    article_info = [info for info in article_info if isinstance(info, tuple)]

    info_df = pd.DataFrame(article_info, columns=['title', 'date', 'category', 'text'])
    info_df.to_csv('./Info/theguardians_article_info.csv')
