from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import os.path
import csv


def get_data(url):
    try:
        with get(url, stream=True) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def scrape(sub, beds):
    raw_html = open("raw_html.html")
    html = BeautifulSoup(raw_html, 'html.parser')
    name = "Scrapes/rentcom/" + sub + beds + ".csv"
    if html.find('div',{'class':'-warning'}):
        return False
    if os.path.isfile(name):
        f = open(name, 'a', newline = '')
        writer = csv.writer(f)
    else:
        f = open(name, 'w', newline = '')
        writer = csv.writer(f)
        writer.writerow(["link", "address", "price", "price_num", "beds", "bath", "cars","suburb","walkability"])

    for listing in html.find_all("article",{'class':'property-cell'}):
        link = listing.find("a")['href']
        address = listing.find("h2",{"class":"address"}).text
        try:
            price = listing.find('span',{"class":"price"}).text
        except:
            continue
        price_num = [int(c) for c in price.replace('.',' ').replace('$','').replace(",",'').split() if c.isdigit()]
        if price_num != []:
            price_num = sum(price_num) / len(price_num)
        else: 
            price_num = ""
        extras = [0,0,0]
        for i in range(0,3):
            extras[i] = ''.join(c for c in listing.find_all('span',{'class':'value'})[i].text if c.isdigit())
        walk = listing.find('span',{"class":"lbl"}).text
        writer.writerow([link, address, price, price_num, extras[0], extras[1], extras[2], sub, walk])
    return True
    


def run(sub, beds):
    count = 1
    url = "https://www.rent.com.au/properties/{3}/p{4}?rent_low={1}&rent_high={2}&bedrooms={0}&surrounding_suburbs=0".format(beds, minprice, maxprice, sub, count)
    raw_html = get_data(url)
    match = True
    while match:
        print(sub + str(raw_html[:100]))
        f = open('raw_html.html',"wb")
        f.write(raw_html)
        match = scrape(sub, beds)
        count += 1
        url = "https://www.rent.com.au/properties/{3}/p{4}?rent_low={1}&rent_high={2}&bedrooms={0}&surrounding_suburbs=0".format(beds, minprice, maxprice, sub, count)
        raw_html = get_data(url)


def test():
    run(suburb, minbeds)

suburb = "strathfield"
minbeds = "0"
minprice = "0"
maxprice = "100000"

with open("cleansubs.txt",'r') as f:
    line = f.readline()
    while line:
        run(line.strip(),'0')
        line = f.readline()
