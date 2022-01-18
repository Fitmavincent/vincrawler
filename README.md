# VinCrawler

A Crawler project because I'm damn boring. 

## Prequisite 

Obviously you need Python. 

## Run it locally

Install ```scrapy``` and ```scrapyrt```

```python
pip install scrapy
```

```py
pip install scrapyrt
```

Run ```scrapyrt```

```
scrapyrt -p 3000
```
Make request

```
http://localhost:3000/crawl.json?start_requests=true&spider_name=ozb
```
Or do it in a cool way

```docker-compose up```

Make a request

```
http://localhost:9080/crawl.json?start_requests=true&spider_name=ozb
```

## Roadmap

Nothing to see here