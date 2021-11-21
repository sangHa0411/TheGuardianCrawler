
import requests
from bs4 import BeautifulSoup

class ArticleCrawler :
    def __init__(self, ) :
        pass
    
    def connect(self, url) :
        assert isinstance(url, str)
        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'html.parser')
        return bs
    
    def get_title(self, bs) :
        title_info = bs.title.text
        index = title_info.find(' | The Guardian')
        return title_info[:index]
    
    def get_date(self, bs) :
        date_info = bs.find('meta', {'property' : 'article:published_time'})
        date = date_info['content']
        
        date_str = date.split('T')[0]
        return date_str
            
    def get_image_url(self, bs) :
        url_info = bs.find('meta', {'property' : 'og:image'})
        image_url = url_info['content']
        return image_url
    
    def get_image_text(self, bs) :
        for tag in bs.findAll('img') :
            if 'alt' in tag.attrs :
                return tag['alt']
            
        raise Exception('There is not img alt Attribute')
        
    def get_text(self, bs) :
        main_content = bs.find('div' , {'class' : "dcr-185kcx9"})
        p_list = main_content.findAll('p')
        
        text_data = [p.text for p in p_list]
        text_data = '\n'.join(text_data)
        return text_data
    
    def __call__(self, url) :
        bs = self.connect(url)
        
        title = self.get_title(bs)
        date = self.get_date(bs)
        #image_url = self.get_image_url(bs)
        #image_text = self.get_image_text(bs)
        text = self.get_text(bs)
        category = url.split('/')[3]
        
        return {'title' : title, 
            'date' : date, 
            #'image_url' : image_url,
            #'image_text' : image_text,
            'category' : category,
            'text' : text
        }
        