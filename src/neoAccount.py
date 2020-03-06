import time
import re
from bs4 import BeautifulSoup
from collections import deque


def initialize_auction_queue(href, price, count):
    d = deque()
    for x in range(0, count):
        auction = [href[x], price[x]]
        d.append(auction)
    return d


def visit_auction(session, headers):
    time.sleep(6)
    res = session.get('http://www.neopets.com/auctions.phtml', headers=headers)

    body = res.content
    soup = BeautifulSoup(body, 'html.parser')

    href = soup.find_all(href=re.compile('auction_id'))
    href = href[1::2]  # removes every other item from array, handles duplicates

    price = soup.select("td > b")
    price = [x for x in price if not '[NF]' in x]   # removes NF tags
    price = price[13:len(price) - 1]  # trims extraneous items from array
    price = price[2::3]

    count = len(href)

    for x in range(0, count):
        href_search = re.search('_id=(.+?)">', str(href[x]))
        if href_search:
            href[x] = href_search.group(1)
        price_search = re.search('<b>(.+?)</b>', str(price[x]))
        if price_search:
            price[x] = price_search.group(1)

    return [href, price, count]


class NeoAccount:
    def __init__(self, user, pw):
        self.user = user
        self.pw = pw
        self.referer = ''

    def __str__(self):
        return '%s:%s' % (self.user, self.pw)

    def login(self, session, headers):
        print('%s:%s logging in' % (self.user, self.pw))
        res = session.get('http://www.neopets.com/index.phtml', headers=headers)
        print(res.headers)
        print(res.content)
        time.sleep(4)
        res = session.post('http://www.neopets.com/login.phtml', {'username': self.user,
                                                                  'password': self.pw,
                                                                  'destination': ''}, headers=headers)
        print(res.headers)
        print(res.content)