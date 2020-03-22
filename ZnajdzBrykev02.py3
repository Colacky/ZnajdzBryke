import requests
from bs4 import BeautifulSoup


def gatherOffers():
    
    print("Jakiego auta szukasz?")
    query = input()
    print(f"Szukam {query}")
    
    allOffers = []        
    offerTemp = []
    
    querySPRZE = query.replace(" ","+")    
    URLSPRZEDAJEMY = f'https://sprzedajemy.pl/szukaj?schm2=ls&catCode=6bea9f&inp_text%5Bv%5D={querySPRZE}&inp_category_id=6&inp_location_id=1&sort=inp_srt_date_d&items_per_page=30'
    pageSPRZE = requests.get(URLSPRZEDAJEMY)

    soupSPRZE = BeautifulSoup(pageSPRZE.content, 'html.parser')
    resultsSPRZE = soupSPRZE.find(class_='list normal')
    car_resultsSPRZE = resultsSPRZE.find_all('article', class_='element')

    try:
        for car_result0 in car_resultsSPRZE:
            car_name = car_result0.find('h2', class_='title')
            car_locdate = car_result0.find('div', class_='address')
            car_price = car_result0.find('div', class_='pricing')
            car_offer = (car_name.text.strip() + ',' + car_locdate.text.strip() + ',' + car_price.text.strip())
            offerTemp = [car_name.text.strip(),car_locdate.text.strip(),car_price.text.strip()]
            allOffers.append(offerTemp)
            #print(allOffers)
            #print("Oferty z SPRZEDAJEMY.PL:"+(car_offer + '\n'))

    except:
        pass
    
    queryOTOMOTO = query.replace(" ","-")
    URLOTOMOTO = f'https://www.otomoto.pl/osobowe/q-{queryOTOMOTO}/?search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D='
    pageOTO = requests.get(URLOTOMOTO)

    soupOTO = BeautifulSoup(pageOTO.content, 'html.parser')
    resultsOTO = soupOTO.find(class_='offers list')
    car_resultsOTO = resultsOTO.find_all('article', class_= 'adListingItem offer-item is-row is-active ds-ad-card-experimental')

    for car_result1 in car_resultsOTO:
        car_name = car_result1.find('h2', class_='offer-title ds-title')
        car_locdate = car_result1.find('h4', class_='ds-location hidden-xs')
        car_price = car_result1.find('div', class_='offer-item__price')
        car_offer = (car_name.text.strip() + ',' + car_locdate.text.strip() + ',' + car_price.text.strip())
        offerTemp = [car_name.text.strip(),car_locdate.text.strip(),car_price.text.strip()]
        allOffers.append(offerTemp)

    queryOLX = query.replace(" ","-")
    URLOLX = f'https://www.olx.pl/motoryzacja/samochody/q-{queryOLX}/'
    pageOLX = requests.get(URLOLX)

    soupOLX = BeautifulSoup(pageOLX.content, 'html.parser')
    resultsOLX = soupOLX.find(id='offers_table')
    car_resultsOLX = resultsOLX.find_all('tr',class_='wrap')


    for car_result in car_resultsOLX:
        car_name = car_result.find('h3',class_="lheight22 margintop5")
        car_locdate = car_result.find('td',class_="bottom-cell" )
        car_price = car_result.find('td',class_="wwnormal tright td-price" )
        
        car_offer = (car_name.text.strip() + "," + car_locdate.text.strip() + "," + car_price.text.strip())
        offerTemp = [car_name.text.strip(),car_locdate.text.strip(),car_price.text.strip()]
        allOffers.append(offerTemp)
    
    #print(allOffers)
    for i in allOffers:
        print(i)