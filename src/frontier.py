'''
The entry point of the program. It - 
 - creates the hierarchy of directories. e.g.,
   Diabetes\\Diabestes-Type1

 - builds a list of dicts with the following example format:
   { ("Diabetes", "Diabetes-Type1") : LINK_TO_Diabetes-Type1 }

The links will be used in the post_scraper.
'''

from page_retriever import get_page
from lxml import html
from directory_manager import *
from str_format import *
import re

BASE_URL = "https://www.medhelp.org/forums/list"
INITIAL_URL = "https://www.medhelp.org"

def build():
    page = get_page(BASE_URL)
    res = list()
    if page:
        doc = html.fromstring(page)
        list_body = doc.xpath('//div[@id="popular_forums_list"]')[0]
        for element in list_body.find_class("forum_group"):
            title = elim_space(element.find_class("forum_group_title")[0].text_content())
            for a in element.xpath('.//div[@class="forums_link"]//a'):
                map = dict()
                group_title = elim_space(a.text_content())
                create_dir(normalize_path_name(title) + "/" + normalize_path_name(group_title))
                map[(normalize_path_name(title), normalize_path_name(group_title))] = _build_link(a.attrib['href'])
                res.append(map)
    return res

def _build_link(link):
  if "www." in link:
    return link
  else:
    return INITIAL_URL + link

# For test only
if __name__ == "__main__":
    build()
