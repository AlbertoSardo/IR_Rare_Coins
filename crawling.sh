# pip install scrapy


rm data/numismatica.json
rm data/delcampe.json
rm data/cavalierenumismatica.json

scrapy crawl numismatica -o data/numismatica.json

scrapy crawl delcampe -o data/delcampe.json

scrapy crawl numiscorner -o data/cavalierenumismatica.json