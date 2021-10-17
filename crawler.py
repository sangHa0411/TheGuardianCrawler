import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

from article import ArticleCrawler
from writer import Writer

def crawl_data(base_url: str, size: int) -> list :
    article_data = []
    for i in tqdm(range(1, size)) :
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
    print('\nData Size of Articles : %d \n' %len(article_data))
    return article_data

def save_data(article_list: list, 
    article_crawler: ArticleCrawler, 
    writer: Writer) -> pd.DataFrame :
    title_list, date_list, cate_list, text_paths, img_paths, img_texts = [[] for i in range(6)]
    for article_url in tqdm(article_list) :
        try :
            article_info = article_crawler(article_url)
            title, date, category, text_path, image_path, image_text = writer(article_info)
        except :
            continue
    
        title_list.append(title)
        date_list.append(date)
        cate_list.append(category)
        text_paths.append(text_path)
        img_paths.append(image_path)
        img_texts.append(image_text)
    
    data_df = pd.DataFrame({'title' : title_list, 
        'date' : date_list,
        'category' : cate_list, 
        'text' : text_paths, 
        'image' : img_paths, 
        'image_texts' : img_texts}
    )
    return data_df


if __name__ == '__main__' :
    DATA_SIZE = 2000

    world_articles = crawl_data('https://www.theguardian.com/world', DATA_SIZE)
    uk_articles = crawl_data('https://www.theguardian.com/uk-news', DATA_SIZE)
    tech_articles = crawl_data('https://www.theguardian.com/technology', DATA_SIZE)
    business_articles = crawl_data('https://www.theguardian.com/business', DATA_SIZE)
    sport_articles = crawl_data('https://www.theguardian.com/sport', DATA_SIZE)
    environment_articles = crawl_data('https://www.theguardian.com/environment', DATA_SIZE)
    culture_articles = crawl_data('https://www.theguardian.com/culture', DATA_SIZE)

    article_data = world_articles + \
        uk_articles + \
        tech_articles + \
        environment_articles + \
        business_articles + \
        sport_articles + \
        culture_articles

    article_data = list(set(article_data))
    print('Total size of data : %d ' %len(article_data))

    article_df = pd.DataFrame({'ID' : range(1, len(article_data)+1), 'URL' : article_data})
    article_df.to_csv('./Info/theguardians_article_url.csv')

    article_crawler = ArticleCrawler()
    writer = Writer('./Data')
    info_df = save_data(article_data, article_crawler, writer)
    info_df.to_csv('./Info/theguardians_article_info.csv')