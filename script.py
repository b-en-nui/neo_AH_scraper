import requests
from src.neoAccount import NeoAccount, visit_auction, initialize_auction_queue

s = requests.Session()
file = open('login.txt', 'r')
login_info = list(file)[0].split(',')
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
headers = {'User-Agent': user_agent,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'en-us,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'referer': 'http://www.neopets.com/index.phtml'}
login_url = 'http://www.neopets.com/login.phtml'
payload = {
    'destination': '',
    'username': login_info[0],
    'password': login_info[1]
}

acc = NeoAccount(payload['username'], payload['password'])

login_attempt = acc.login(s, headers)
visit_attempt = visit_auction(s, headers)
deque = initialize_auction_queue(visit_attempt[0], visit_attempt[1], visit_attempt[2])

print(deque)

