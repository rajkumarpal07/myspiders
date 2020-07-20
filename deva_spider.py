import scrapy
import bs4
import bleach

class deva_spider(scrapy.Spider):
    name = "padals"
    allowed_domains = ["dvaaram.org"]

    def start_requests(self):
        start_urls = [
            'http://www.dvaaram.org/thirumurai_1/onepage.php?thiru=1&Song_idField=1001',
        ]
        for url in start_urls:
            print("Entered URL Loop======================================\n\n\n")
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        songfield = response.url.split("&")[-1]
        pathigamID = int(songfield.split("=")[-1]) - 1000
        print(pathigamID)
        unicodestr = response.body
        soup = bs4.BeautifulSoup(unicodestr, "lxml")

        alldiv = soup.find_all('div',{'class':'Padal'})

        allbob = soup.find_all('h3',{'id':'bobcontent1-title'})
        head_tag = allbob[0]
        tname = head_tag.span.string

        pannstr = head_tag.next_sibling.next_sibling
        pann = (pannstr.split(":")[-1])

        allpurai = []
        for div in soup.find_all('h3',{'id':'bobcontent1-title'}):
            if div.next_sibling.string != None:
                allpurai.append(div.next_sibling.string)

        self.log(len(allpurai))
        path = 'quotes.txt'
        padals_file = open(path, 'a', encoding="UTF-8")
        padal = []
        count = 0
        for adiv, aurai in zip(alldiv, allpurai):
            padal = adiv.contents
            urai = aurai
            lines = ""
            for line in padal:
                lines = lines + str(line).lstrip(' ').rstrip(' ')
                lines = lines.replace("\r\n", " ")
                lines = lines.replace("<br/>", "\\\\n")

            padals_file.write('{\n')
            padals_file.write('"book_id": ' + '1' +',\n')
            padals_file.write('"pathigam_id":' + str(pathigamID) +',\n' )
            padals_file.write('"verse_id": '  + str(count + 1) +',\n')
            padals_file.write('"temple_name": "' + tname + '"' +',\n')
            padals_file.write('"pann": "' + pann + '"' +',\n')
            padals_file.write('"verse": "'+ lines + '"' +',\n')
            padals_file.write('"explanation": "'+ str(urai) + '"' +',\n')
            padals_file.write('"translation": "'+ '' + '"' +',\n')
            padals_file.write('},\n\n')

            count = count + 1

        padals_file.close()
        pathigamID = pathigamID + 1

        next_page = 'http://www.dvaaram.org/thirumurai_1/onepage.php?thiru=1&Song_idField=' + str(pathigamID+1000)

        yield response.follow(next_page, self.parse)



