from novaprinter import prettyPrinter
from helpers import retrieve_url

class knaben(object):
    url = 'https://knaben.eu'
    name = 'Knaben'
    supported_categories = {'all': 'all'}

    def search(self, what, cat='all'):
        search_url = f"{self.url}/search/{what}"
        html = retrieve_url(search_url)
        
        self.parse(html)

    def parse(self, html):
        from lxml import html as lh
        tree = lh.fromstring(html)
        
        results = tree.xpath('//table[@class="table"]/tbody/tr')
        for result in results:
            title = result.xpath('.//td[@class="title"]/a/text()')[0]
            link = result.xpath('.//td[@class="title"]/a/@href')[0]
            size = result.xpath('.//td[@class="size"]/text()')[0]
            seeders = result.xpath('.//td[@class="seeders"]/text()')[0]
            leechers = result.xpath('.//td[@class="leechers"]/text()')[0]
            
            prettyPrinter({
                'name': title,
                'size': size,
                'seeds': seeders,
                'leech': leechers,
                'link': self.url + link,
                'desc_link': self.url + link,
                'engine_url': self.url,
                'file': self.url + link
            })

# Testing
if __name__ == "__main__":
    engine = knaben()
    engine.search('test')
