# email_scraper
### An assessment tool to discover which emails are published on your site

<p align="center">
<img src="scraper.png" width=300>
</p>


### What is email_scraper
__email_scraper__ is a tool to extract emails from a website and from its linked websites.
It's an OSINT (Open Source Intelligence) tool devised to gather (*scrape*) the publicly available emails in one or more websites. 
Attackers use emails more and more as a way to deliver malicious payloads through attachments (*phishing*), so being aware of which emails
are published on the Internet is crucial to keep under control your organization's attack surface. 
You could run this tool entering one URL of your organization, setting a proper crawling threshold for the number of pages to be visited,
and then waiting to see which emails can be publicily retrieved from an attacker.

### How to Run
All the code is packed inside a Python script, so you basically need to download [Python 3](https://www.python.org/downloads/), and to ensure that 
the *requests* module is installed (`pip install requests`). 
Then, adjust the global variables at the beginning of the script, and simply run with 
`Python email_scraper.py`

### Features

- __Crawl Limit__ : set the maximum number of pages that you want to crawl. Setting this value to 1 will only crawl emails from the provided webpage, setting a high value will navigate more webpages, possibly exiting form the starting domain.
- __Finds Disguised Emails__: for some strange reasons, people are convinced that if they substitute the *@* simbol of their emails with something like *AT*, or *(AT)*, or even *[AT]*, that will be a good protection to avoid that their email is not being crawled. Well, with a single line of code (a.k.a. *regular expression*) we show to these ~University Professors~, ehm, guys, how much they are mistaken. 
- __Avoid Already Visited Pages__: when fetching a new page to be visited from the queue of discovered webpages, we check that we have not already visited it!
- __HTML Search__: the search is done all the HTML code and is not limited to visible text only.

### Demo
In the following Demo, I feed the tool with an url from The Times and I set the limit
of crawled pages to 10. The tool visits the discovered webpages in a FIFO order (First In - First Out),
stopping after visiting 10 distinct web pages. At the end, it outputs the list of emails found on these pages.

![Alt Text](https://github.com/Balzu/email_scraper/blob/main/demo.gif)


### Blog Post

If want to read the associated blog post, please take a look [here!](http://thebytemachine.com/an_OSINT_tool_to_crawl_a_list_of_publicly_available_emails_from_websites)


### What's next?

- If we are really interested only in those emails published on our organization's site, we could limit the search to only those pages belonging to the same, source domain. 
- Some smart guys write their email on Paint, save it as image and then upload it to their website. FOr the moment being, we are not able to catch those emails, although I believe that tools used by attacker possibly have that feature, at least for targeted attacks. I will think about adding it in the future.

