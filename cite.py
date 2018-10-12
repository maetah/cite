from chardet import detect
from lxml.etree import HTML
from time import localtime, strftime, strptime
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

class Pub:
    def __init__(self, url):
        self.url = url.lstrip('http://').lstrip('https://')
        self.host = urlsplit(url).netloc
        req = Request(url, headers = {'content-type': 'text/html', 'User-Agent': 'Mozilla/5.0'})
        res = urlopen(req)
        self.access = localtime()
        date = res.headers['Last-Modified']
        self.date = None if date == None else strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
        page = res.read()
        html = HTML(page.decode(detect(page)['encoding']))
        author = html.xpath('//meta[@name="author"or@property="author"][1]/@content')
        self.author = None if author == [] else author[0]
        site = html.xpath('//meta[@property="og:site_name"][1]/@content')
        self.site = None if site == [] else site[0]
        title = html.xpath('//meta[@property="og:title"][1]/@content')
        self.title = html.xpath('//title[1]/text()')[0] if title == [] else title[0]

def mla(pub, author = None, publisher = None):
    if author == None:
        author = pub.author
        if author == None:
            author = ''
        else:
            author += '. '
    title = pub.title.strip()
    if title[-1] not in '.!?':
        title += '.'
    if publisher == None:
        publisher = pub.site
        if publisher == None:
            publisher = pub.host
    date = pub.date
    date = '' if date == None else strftime(', %d %b %Y', date)
    access = strftime('%d %b %Y', pub.access)
    return '{}"{}" {}{}. Accessed {}. {}. '.format(author, title, publisher, date, access, pub.url)
