import re, requests, json, queue
from lxml import html

MAX_URLS = 10
DEBUG = True

def find_links_in_page(webpage):
    page = html.fromstring(webpage.content)
    urls = page.xpath('//a/@href')
    return [ url for url in urls if url[0:4] == 'http']

def find_emails_in_webpage(url):
    req=requests.get(url)
    text = req.text
    #emails = re.findall(r"[\w\.]+(?:@|.{0,1}AT.{0,1})[\w\.-]+\.[a-zA-Z]{2,3}", text, flags=re.IGNORECASE)
    emails = re.findall(r"[\w\.]+(?:@|\W{1}AT\W{1})[\w\.-]+\.[a-zA-Z]{2,3}", text, flags=re.IGNORECASE)
    cleaned_emails = [re.sub(r'.{0,1}AT.{0,1}', r'@', email) for email in emails]
    return cleaned_emails, req
    
def filter_emails_on_suffixes(emails):
    valid_suffixes = load_valid_suffixes()
    return [email for email in emails if has_valid_suffix(email, valid_suffixes)]
    
            
def has_valid_suffix(email, suffixes):
    return '.'+email.split('.')[-1] in suffixes
    
def load_valid_suffixes():
    # Returns the st of valid email suffixes
    suffixes = set()
    with open('internet-top-level-domain-names.json') as json_file:
        entries = json.load(json_file)
        [suffixes.add(entry['Domain_Name']) for entry in entries]
        return suffixes


def visit_url(url, q, visited_urls, scraped_emails, valid_suffixes):
    if DEBUG:
        print('\nVisiting URL {}\n'.format(url))
        print('\nvisited {} urls!\n'.format(str(len(visited_urls))))
        print('\nQueue size: {} !\n'.format(str(q.qsize())))
    emails, webpage = find_emails_in_webpage(url)
    urls = find_links_in_page(webpage)
    [q.put(url) for url in urls if url not in visited_urls]
    [scraped_emails.add(email) for email in emails if has_valid_suffix(email, valid_suffixes)]
    

def scrape_emails(q, scraped_emails, visited_urls, valid_suffixes):    
    if q.empty() or len(visited_urls) >= MAX_URLS:
        return scraped_emails
    url = q.get()
    visited_urls.add(url)
    visit_url(url, q, visited_urls, scraped_emails, valid_suffixes)
    scrape_emails(q, scraped_emails, visited_urls, valid_suffixes)
    

q = queue.Queue()
scraped_emails = set()
visited_urls = set() 
valid_suffixes = load_valid_suffixes()

url = input('Insert the url whose emails you want to retrieve\n\n')
q.put(url)

scrape_emails(q, scraped_emails, visited_urls, valid_suffixes)
print('\nFound {} emails:\n'.format(str(len(scraped_emails))))
[print(email) for email in scraped_emails]


