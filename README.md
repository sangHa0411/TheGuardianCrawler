# TheGuardianCrawler

## Goal 
  * Crawling News Data (Article texts, images)
  * Apply multiprocessing to reduce crawling time

## ToDo List
  1. Pretrained Model(GPT, BERT)
  2. Open Domain Question Answering
  3. Image Classification
  4. Vision Question Answering

## Directory Tree 
```
├── ArticleCrawler.ipynb
├── README.md
├── asset
├── article.py
├── crawler.py
└── writer.py
```

## Library Version
  1. bs4 : '4.6.0'
  2. pandas : '1.1.5'
  3. requests : ''2.24.0'

## Termianl
```
python crawler.py
```

### 1. Main Page
  1. Source : TheGuardian (international edition)
  2. URL : 'https://www.theguardian.com/international'
  3. Image
    ![mainpage](./asset/mainpage.png)

### 2. News Category
  1. The number of total articles : 204201
  2. Crawling category
        * world
        * uk
        * technology
        * business
        * sport
        * environment
        * culture
  3. Image
    ![category](./asset/category.png)

### 3. Crawling Information
  1. Title (News Title)
  2. Date (Published Date)
  3. Category
  4. Text (Article Text)
  5. Image (Article Image)
  6. Image Description
  7. Image
    ![articelexample](./asset/articleexample.png)
