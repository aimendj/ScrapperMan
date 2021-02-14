
from bs4 import BeautifulSoup
import pandas as pd
from proxy import getChromeDriver, getFirefoxDriver

def main():
    products = []  # List to store name of the product
    prices = []  # List to store price of the product
    categories = []  # List to store rating of the product
    localisations = []

    features = "html.parser"
    nextPage = "https://www.leboncoin.fr/ventes_immobilieres/1883524518.htm"
    #driver=None
    #while(driver == None):
    driver=getChromeDriver(nextPage)

    content = driver.page_source
    soup = BeautifulSoup(content, features)

    for a in soup.findAll('article', href=False, attrs={'class': 'css-1kxq1f8'}):
        name = a.find('div', attrs={'class': 'styles_adDetails__1qVAk'})
        price = a.find('div', attrs={'class': 'styles_Price__1tlGj'})
        date = a.find('div', attrs={'class': 'styles_secondaryInformations__GkW_2'})
        tel = 'N/A'
        x = driver.find_element_by_css_selector("button[data-qa-id='adview_button_phone_contact']")
        x.click()
        tel=a.find('a', attrs={'class': '_2qvLx _3osY2 _35pAC _1Vw3w _kC3e _3x0kP _11dBH _PypL sczyl _30q3D _1y_ge _3QJkO'})['href']

        criterias = a.find('div', attrs={'class': 'styles_Criteria__2sVPt'})
        x=driver.find_element_by_css_selector("button[data-qa-id='criteria_more']")
        x.click()

        # begin criterias
        criterias=a.find('div', attrs={'class': 'styles_Criteria__2sVPt'})
        typeVente = 'N/A'
        typeBien = 'N/A'
        surface = 'N/A'
        pieces = 'N/A'
        energie = 'N/A'
        ges = 'N/A'
        honoraires = 'N/A'
        reference='N/A'

        for i in range(len(criterias.contents)):
            criteria = criterias.contents[i].find('p', attrs={'class': '_2k43C _1pHkp Dqdzf cJtdT _3j0OU'})
            value=criterias.contents[i].find('p', attrs={'class': '_3eNLO _137P- P4PEa _35DXM'})
            if(criteria.text == 'Type de vente'):
                typeVente=value.text
            elif(criteria.text == 'Type de bien'):
                typeBien=value.text
            elif (criteria.text == 'Surface'):
                surface = value.text
            elif (criteria.text == 'Pièces'):
                pieces = value.text
            elif (criteria.text == 'Classe énergie'):
                energie = value.text
            elif (criteria.text == 'GES'):
                ges = value.text
            elif (criteria.text == 'Honoraires'):
                honoraires = value.text
            elif (criteria.text == 'Référence'):
                reference = value.text
        #end criterias

    #description=a.find('div', attrs={'class': '_2BMZF _137P- P4PEa _3j0OU'})



    driver.close()

    df = pd.DataFrame({'Product Name': products, 'Price': prices, 'Category': categories, 'Localisation': localisations})
    df.to_csv('products.csv', index=False, encoding='utf-8')

main()