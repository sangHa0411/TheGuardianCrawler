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
    num_cores = multiprocessing.cpu_count()

    world_articles = parmap.map(crawl_data, range(1,DATA_SIZE+1), 'https://www.theguardian.com/world', pm_pbar=True, pm_processes=num_cores) 
    world_articles = sum(world_articles, [])
    uk_articles  = parmap.map(crawl_data, range(1,DATA_SIZE+1), 'https://www.theguardian.com/uk-news', pm_pbar=True, pm_processes=num_cores) 
    uk_articles  = sum(uk_articles , [])
    tech_articles = parmap.map(crawl_data, range(1,DATA_SIZE+1), 'https://www.theguardian.com/technology', pm_pbar=True, pm_processes=num_cores) 
    tech_articles = sum(tech_articles, [])
    business_articles  = parmap.map(crawl_data, range(1,DATA_SIZE+1), 'https://www.theguardian.com/business', pm_pbar=True, pm_processes=num_cores) 
    business_articles  = sum(business_articles , [])
    sport_articles = parmap.map(crawl_data, range(1,DATA_SIZE+1), 'https://www.theguardian.com/sport', pm_pbar=True, pm_processes=num_cores) 
    sport_articles = sum(world_articles, [])
    environment_articles  = parmap.map(crawl_data, range(1,DATA_SIZE+1), 'https://www.theguardian.com/environment', pm_pbar=True, pm_processes=num_cores) 
    environment_articles  = sum(environment_articles , [])
    culture_articles  = parmap.map(crawl_data, range(1,DATA_SIZE+1), 'https://www.theguardian.com/culture', pm_pbar=True, pm_processes=num_cores) 
    culture_articles  = sum(culture_articles , [])

    article_data = world_articles + \
        uk_articles + \
        tech_articles + \
        environment_articles + \
        business_articles + \
        sport_articles + \
        culture_articles
    article_data = [article for article in article_data if article != None]
    article_data = list(set(article_data))

    print('Total size of data : %d ' %len(article_data))
    
    article_df = pd.DataFrame({'ID' : range(1, len(article_data)+1), 'URL' : article_data})
    article_df.to_csv('./Info/theguardians_article_url.csv')
   
    article_crawler = ArticleCrawler()
    writer = Writer('./Data')
    article_info = parmap.map(save_data, article_data, article_crawler, writer, pm_pbar=True, pm_processes=num_cores) 
    article_info = [info for info in article_info if info != None]

    info_df = pd.DataFrame(article_info, columns=['title', 'date', 'category', 'text', 'image', 'image_text'])
    info_df.to_csv('./Info/theguardians_article_info.csv')
