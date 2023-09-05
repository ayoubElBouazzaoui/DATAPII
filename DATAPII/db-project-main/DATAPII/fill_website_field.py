from bs4 import BeautifulSoup
import requests
import time

def fill_site(ondernemingsnummer):

    time.sleep(10)

  
    url = f"https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer={ondernemingsnummer}&actionLu=Zoek"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    
    rows = soup.find(id="table").find_all("tr")

    count = 0
    web_row = ""

    for row in rows:
        if count >= 12:
           
            web_row = row.find_all("td")[1].getText()
            break
        count += 1


    time.sleep(10)

    if "Geen gegevens opgenomen in KBO." in web_row:
        return None
    else:
        return web_row

