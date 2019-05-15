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
    name = "Scrapes/" + sub + beds + ".csv"
    if html.find('p',{'class':'noMatch'}):
        return False
    if os.path.isfile(name):
        f = open(name,'a')
        writer = csv.writer(f)
    else:
        f = open(name,'w')
        writer = csv.writer(f)
        writer.writerow(["link", "address", "price", "price_num", "beds", "bath", "cars","suburb"])
    
    for listing in html.find_all("article"):
        link = "https://www.realestate.com.au" + listing.find("a")['href']
        address = listing.find("a",{"rel":"listingName"}).text
        try:
            price = listing.find('p',{"class":"priceText"}).text
        except:
            continue
        price_num = [int(c) for c in price.replace('.',' ').replace('$','').replace(",",'').split() if c.isdigit()]
        if price_num != []:
            price_num = sum(price_num) / len(price_num)
        else: 
            price_num = ""
        extras = [0,0,0]
        for i in range(0,len(listing.find_all("dd"))):
            extras[i] = listing.find_all("dd")[i].text
        writer.writerow([link, address, price, price_num, extras[0], extras[1], extras[2], sub])
    return True

def run(sub, beds):
    count = 1
    url = "https://www.realestate.com.au/rent/with-{0}-bedrooms-between-{1}-{2}-in-{3}/list-{4}?activeSort=price-asc&includeSurrounding=false".format(beds, minprice, maxprice, sub, count)
    print(url)
    raw_html = get_data(url)
    match = True
    while match:
        print(raw_html[:100])
        f = open('raw_html.html',"wb")
        f.write(raw_html)
        match = scrape(sub, beds)
        count += 1
        raw_html = get_data("https://www.realestate.com.au/rent/with-{0}-bedrooms-between-{1}-{2}-in-{3}/list-{4}?activeSort=price-asc&includeSurrounding=false".format(beds, minprice, maxprice, sub, count))

def test():
    run(suburb, minbeds)

suburb = "abbotsbury"
minbeds = "0"
minprice = "0"
maxprice = "0"

test()

#with open("cleansubs.txt",'r') as f:
#    line = f.readline()
#    while line:
#        print(line)
#        run(line.strip(),'2')
#        line = f.readline()
