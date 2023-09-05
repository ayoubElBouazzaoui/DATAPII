import scraper
import db_data
from multiprocessing.pool import Pool

fiscaal_jaar = 2021

def scrape(kmo):
    onderneming_id, onderneming_url = kmo
    print(f'ID: {onderneming_id} - URL: {onderneming_url}')

    if scraper.url_ok(onderneming_url):
        results = []  # FiscaalJaar, OndernemingID, Pagina
        complete_website = ""

        for page in scraper.get_all_pages(onderneming_url):
            print(page)
            page_text = scraper.text_from_webpage(page)
            complete_website += page_text + "/n"

        db_data.insert_website_text(fiscaal_jaar, onderneming_id, complete_website.trim())

    db_data.update_scrape_log(fiscaal_jaar, onderneming_id)

if __name__ == '__main__':
    kmo_urls = db_data.get_ondernemingen(fiscaal_jaar)

    # Create and configure the process pool
    with Pool() as pool:
        pool.map(scrape, kmo_urls)
