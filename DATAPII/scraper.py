import urllib.request
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urlparse


def url_ok(url):
    try:
        r = urllib.request.urlopen(url).getcode()
        return r == 200
    except:
        return False

def get_data(url):
    r = requests.get(url)
    return r.text

def get_destination_redirect(page_url):
    redirect = requests.get(page_url).url.replace('www.', '')
    print(redirect)
    return redirect

# Create an empty dictionary for href links
dict_href_links = {}
word_exclusion = ['.pdf', 'jpg', '/fr/', '/en/', '/be-fr/', '/be-en/']

def get_links(website_link):
    html_data = get_data(website_link)
    soup = BeautifulSoup(html_data, "html.parser")
    list_links = []

    for link in soup.find_all("a", href=True):
        href = str(link['href'])
        if not any(word in href for word in word_exclusion):
            if href.startswith((website_link)):
                list_links.append(get_destination_redirect(href))
            if href.startswith("/"):
                full_link = website_link + href[1:]
                if full_link not in dict_href_links:
                    dict_href_links[full_link] = None
                    list_links.append(get_destination_redirect(full_link))

    # Convert list of links to a dictionary with "Not-checked" values
    dict_links = dict.fromkeys(list_links, "Not-checked")
    return dict_links

def get_subpage_links(links):
    for link in links:
        if links[link] == "Not-checked":
            subpage_links = get_links(link)
            links[link] = "Checked"
        else:
            subpage_links = {}
        links = {**subpage_links, **links}
    return links

def get_all_pages(website):
    hostname = "http://" + urlparse(website).hostname
    print(hostname)
    dict_links = {hostname: "Not-checked"}

    counter, counter2 = None, 0
    while counter != 0:
        counter2 += 1
        dict_links2 = get_subpage_links(dict_links)
        counter = sum(value == "Not-checked" for value in dict_links2.values())
        dict_links = dict_links2

    return dict_links

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_webpage(webpage):
    body = get_data(webpage)
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)
