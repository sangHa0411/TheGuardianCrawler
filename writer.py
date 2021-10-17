import os
import urllib

class Writer :
    def __init__(self, dir_path) :
        self.dir_path = dir_path
        
    def __call__(self, article_data: dict) :
        assert None not in list(article_data.values())
        
        title = article_data['title']
        date = article_data['date']
        category = article_data['category']
        image_url = article_data['image_url']
        image_text = article_data['image_text']
        text = article_data['text']
        
        image_path = self.save_image(image_url, title)
        text_path = self.save_text(text, title)
        
        return title, date, category, text_path, image_path, image_text
        
    def save_image(self, image_url: str, title: str) -> str :
        image_path = os.path.join(self.dir_path, 'image', title)
        image_path = image_path + '.jpg'
        
        urllib.request.urlretrieve(image_url, image_path)
        return image_path
        
    def save_text(self, text: str, title: str) -> str :
        text_path = os.path.join(self.dir_path, 'text', title)
        text_path = text_path + '.txt'
        
        with open(text_path, 'w') as f:
            f.write(text)
        return text_path
                