import requests
from lxml import html
from time import sleep
import logging

FORMAT = "[%(asctime)s] - [%(levelname)s] - [%(funcName)s] - %(message)s"
logging.basicConfig(level=20, format=FORMAT)

"""
def scp_url(scp_num):
    return "http://www.scp-wiki.net/scp-{}".format(str(scp_num).zfill(3))
"""


def get_text(html_str):
    tree = html.fromstring(html_str)
    text = tree.xpath("//div[@id='page-content']")[0].text_content()
    return text


def get_page(url):
    r = requests.get(url)
    if r.status_code != 200:
        logging.error("HTTP {} Error: Unable to crawl {}".format(r.status_code, url))
    else:
        sleep(0.5)
        return r.content.decode("utf-8")


def clean_text(text):
    s = text.find("Item #: SCP")
    e = text.rfind("«") - 1
    return text[s:e].strip()


def main():
    scp = lambda s: str(s).zfill(3)
    scp_url = lambda scp_num: "http://www.scp-wiki.net/scp-{}".format(
        str(scp_num).zfill(3)
    )
    for i in range(2, 101):
        logging.info("Crawling SCP-{}".format(scp(i)))
        text = clean_text(get_text(get_page(scp_url(i))))
        with open("SCPFiles/scp{}.txt".format(scp(i)), "w", encoding="utf-8") as F:
            F.write(text)
    logging.info("Collection complete! Ended at SCP-{}".format(scp(i)))


if __name__ == "__main__":
    main()
