import scrapy
import bleach
import re
import urllib
import w3lib

from scrapy.http import Request, TextResponse

class mlr_spider(scrapy.Spider):
    name = "malar"
    downloadDirectory = 'C:\Pyroot\scrape'
    allowed_domains = ['www.dmalar.com']

    baseUrl = 'http://www.dmalar.com/news_detail.asp?id='
    global articleId
    articleId = "2036863"
    newsUrl = baseUrl + articleId

    global start_urls
    start_urls = [newsUrl]

    def start_requests(self):

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, encoding='utf-8')


    def parse(self, response):
        unicodestr = response.text
        news = unicodestr.rsplit('<!--<article')[1].rsplit('<!--</article')[0]
        ans = re.sub('[\t+]', '', news)
        ans = re.sub('[\r\n+]', '', ans)
        ans = ans.rsplit('scrollbars=yes\');}')[1]
        newsstr = bleach.clean(ans, tags=[], strip=True)
        newsstr = newsstr.lstrip().rstrip()
        cleaned = newsstr.lstrip('0123456789 ')
        self.log('Extracted data ::\n' + cleaned)

        pattern = "news_detail\.asp\?id=([0-9]{7})"
        matches = re.findall(pattern, unicodestr)
        for match in matches:
            if(match != articleId):
                if match not in start_urls:
                    start_urls.append('http://www.dmalar.com/news_detail.asp?id='+ match)
        print("\n\n ====> ONE ITER OVER !!!! \n\n")

        fileid = "1";
        path = './dmlr-' + fileid + '.txt'
        articles_file = open(path, 'a', encoding="UTF-8")
        articles_file.write("\n" + articleId + "::::\t" + cleaned)
        articles_file.close()

        yield response.follow(next_page, self.parse)







