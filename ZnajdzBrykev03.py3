import requests
from bs4 import BeautifulSoup
import re

hrefSPRZE = []
hrefOTO = []
hrefOLX = []
hrefs = [hrefSPRZE, hrefOTO, hrefOLX]
allOffers = []


class Offer:
    def __init__(self,adID,link,name,price,location,picture):
        self.adID= adID
        self.link= link
        self.name= name
        self.price= price
        self.location= location
        self.picture= picture
    
    def __repr__(self):
        return str(f'ID ogloszenia: {self.adID}'+'\n'+f'Link do ogłoszenia: {self.link}'+'\n'+f'Nazwa: {self.name}'+'\n'+f'Cena: {self.price}'+'\n'+f'Lokalizacja: {self.location}'+f'Zdjęcie: {picture}'+'\n\n')

    
def getLinks():
    print("Jakiego auta szukasz?")
    query = input()
    print(f"Szukam {query}")

    allOffers = []        
    offerTemp = []
    global hrefSPRZE
    global hrefOTO
    global hrefOLX

    querySPRZE = query.replace(" ","+")    
    URLSPRZEDAJEMY = f'https://sprzedajemy.pl/szukaj?schm2=ls&catCode=6bea9f&inp_text%5Bv%5D={querySPRZE}&inp_category_id=6&inp_location_id=1&sort=inp_srt_date_d&items_per_page=30'
    pageSPRZE = requests.get(URLSPRZEDAJEMY)

    soupSPRZE = BeautifulSoup(pageSPRZE.content, 'html.parser')
    resultsSPRZE = soupSPRZE.find(class_='list normal')
    linksSPRZE = resultsSPRZE.find_all('a', href=True)
        
    for link in linksSPRZE:
        hrefSPRZE.append("https://sprzedajemy.pl"+link['href'])
    hrefSPRZE = list(dict.fromkeys(hrefSPRZE))
    #return hrefSPRZE
    
    queryOTOMOTO = query.replace(" ","-")
    URLOTOMOTO = f'https://www.otomoto.pl/osobowe/q-{queryOTOMOTO}/?search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D='
    pageOTO = requests.get(URLOTOMOTO)

    soupOTO = BeautifulSoup(pageOTO.content, 'html.parser')
    resultsOTO = soupOTO.find(class_='offers list')
    linksOTO = resultsOTO.find_all('a', href=True)
    
    for link in linksOTO:
        hrefOTO.append(link['href'])
    hrefOTO = list(dict.fromkeys(hrefOTO))
    #return hrefOTO
    
    queryOLX = query.replace(" ","-")
    URLOLX = f'https://www.olx.pl/motoryzacja/samochody/q-{queryOLX}/'
    pageOLX = requests.get(URLOLX)

    soupOLX = BeautifulSoup(pageOLX.content, 'html.parser')
    resultsOLX = soupOLX.find(id='offers_table')
    linksOLX = resultsOLX.find_all('a', href=True)
    
    for link in linksOLX:
        hrefOLX.append(link['href'])
    hrefOLX = list(dict.fromkeys(hrefOLX))
    
    return hrefOLX, hrefSPRZE, hrefOTO
    
    
    
def getOfferSPRZE(hrefSPRZE):
    global allOffers
    link = hrefSPRZE
    hrefSPRZE = re.sub('html.*$','html',hrefSPRZE)
    offerSoup = BeautifulSoup(requests.get(hrefSPRZE).content, 'html.parser')
    offer1 = offerSoup.find('article', class_='offerDetails')
    adID = offer1.find('ul', class_='offerAdditionalInfo')
    adID = adID.text.strip()
    adID = adID[-1:-9:-1]
    adID = adID[-1::-1]
    name = offer1.find('h1', class_='offerTitle')
    price = offer1.find('div', class_='priceWrp')
    location = offer1.find('a', class_='locationName')
    picture = offer1.find('img', class_='js-gallerySlide', src=True)
    offerID = 'SPRZE'+adID
    
    print(adID)
    print(name.text.strip())
    print(price.text.strip())
    print(location.text.strip())
    print(picture['src'])
    print('\n')
    
    name = name.text.strip()
    price = price.text.strip()
    location = location.text.strip()
    picture = picture['src']
    
    offerID = Offer(adID,hrefSPRZE,name,price,location,picture)
    allOffers.append(offerID)
    return allOffers
    
def getOfferOTO(hrefOTO):
    link = hrefOTO
    hrefOTO = re.sub('html.*$','html',hrefOTO)
    offerSoup = BeautifulSoup(requests.get(hrefOTO).content, 'html.parser')
    offer1 = offerSoup.find('div', class_='flex-container-main__left')
    adID = offer1.find('div', class_='offer-meta')
    adID = adID.text.strip()
    adID = adID[-1:-11:-1]
    adID = adID[-1::-1]
    name = offer1.find('h1', class_='offer-title big-text')
    price = offer1.find('div', class_='wrapper')
    location = offer1.find('span', class_='seller-box__seller-address__label')
    picture = offer1.find_all('img', src=True)
    offerID = 'OTO'+adID
    
    print(adID)
    print(name.text.strip())
    print(price.text.strip())
    print(location.text.strip())
    print(picture[1]['src'])
    print('\n')
    
    offerID = Offer(adID,hrefOTO,name,price,location,picture)
    allOffers.append(offerID)
    return allOffers
    
def getOfferOLX(hrefOLX):
    link = hrefOLX
    hrefOLX = re.sub('html.*$','html',hrefOLX)
    offerSoup = BeautifulSoup(requests.get(hrefOLX).content, 'html.parser')
    offer1 = offerSoup.find('section', class_='offer-section')
    adID = offer1.find('div', class_='offer-titlebox__details')
    adID = adID.text.strip()
    adID = adID[-1:-10:-1]
    adID = adID[-1::-1]
    name = offer1.find('h1')
    price = offer1.find('div', class_='price-label')
    location = offer1.find('a', class_='show-map-link')
    picture = offer1.find('img', class_='vtop bigImage {nr:1}', src=True)
    offerID = 'OLX'+adID
    
    print(adID)
    print(name.text.strip())
    print(price.text.strip())
    print(location.text.strip())
    print(picture['src'])
    print('\n')
    
    offerID = Offer(adID,hrefOLX,name,price,location,picture)
    allOffers.append(offerID)
    return allOffers

def createOffers():
    global hrefSPRZE
    global hrefOTO
    global hrefOLX
    for i in hrefSPRZE:
        try:
            getOfferSPRZE(i)
        except:
            print(f'invalid link: {i}')
    for j in hrefOTO:
        try:
            getOfferOTO(j)
        except:
            print(f'invalid link: {j}')
    for y in hrefOLX:
        try:
            getOfferOLX(y)
        except:
            print(f'invalid link: {y}')
        
        