'''
This module scrapes each post page fetched from the scroll-able pages.

The structure is returned as a JSON-format. E.g.,

{"POST" :
    {"POST_LINK": link},
    {"USER_NAME" : user_name},
    {"USER_PROFILE_LINK" : profile_link},
    {"POST_TITLE" : title},
    {"POST_BODY" : body},
    {"POST_DATE" : post_date},
    {"POST_ID" : id},
    {"RESPONSES" :
        {"RESPONSE" :
            {"USER_NAME" : user_name},
            {"USER_PROFILE_LINK" : profile_link},
            {"RESPONSE_BODY" : body},
            {"RESPONSE_DATE" : response_date},
            {"RESPONSE_ID" : id},
            {"COMMENTS" :
                {"COMMENT" :
                    {"USER_NAME" : user_name},
                    {"USER_PROFILE_LINK" : profile_link},
                    {"COMMENT_BODY" : body},
                    {"COMMENT_DATE" : comment_date},
                    {"COMMENTE_ID" : id}
                }
            }
        }
    }

    ...
}

The fetched information is returned as Python dict and would be converted to JSON later.
'''

from scrollpage_scraper import get_post_link
from scrollpage_scraper import get_scrolled_page
from page_retriever import get_page
from directory_manager import *
from json_manager import save_as_json
from lxml import html

BASE_URL = "https://medhelp.org"

# path_titles is the key in the dicts stored in the frontier
def run(path_titles: tuple, url: str):
    path = _build_path(path_titles, "post.html")
    if not file_exists(path):
        page = get_scrolled_page(url)
        create_file(path, page)
    else:
        page = read_file(path, 'rb')

    for post_link in _get_posts(page):
        post_id = _get_post_id(post_link)
        post_file_name = _build_post_file_name(post_id)
        post_path = _build_path(path_titles, post_file_name)
        if not file_exists(post_path):
            post_page = get_page(post_link)
            create_file(post_path, post_page)
        else:
            post_page = read_file(post_path, 'r')
        post_dict = _fetch_info(post_page, post_id, post_link)
        save_as_json(post_dict, _build_path(path_titles, _build_post_json_name(post_id)))
        
def _build_path(path_titles: tuple, file_name: str):
    return path_titles[0] + "\\" + path_titles[1] + "\\" + file_name

def _get_post_id(post_link):
    return post_link[len(post_link) - post_link[::-1].find('/'):]

def _build_post_file_name(post_id):
    return "post_" + post_id + ".html"

def _build_post_json_name(post_id):
    return "post_" + post_id + ".json"

def _get_posts(page) -> list:
    doc = html.fromstring(page)
    return [BASE_URL + a.attrib["href"] for a in doc.xpath('//h2[@class="subj_title "]//a')]

def _fetch_info(page, post_id, post_link):
    doc = html.fromstring(page)
    header = doc.xpath('//div[@class="subj_header"]')[0]
    post_title = header.xpath('.//h1[@class="subj_title"]')[0].text_content().strip()
    post_user_name = _get_user_name(header)
    post_user_link = BASE_URL + header.xpath('.//div[@class="subj_info"]//a')[0].attrib["href"]
    post_date = _get_date(header)
    post_body = doc.xpath('//div[@id="subject_msg"]')[0].text_content().strip()
    responses = _fetch_resp(doc)
    return _build_post_dict(
        post_link, post_title, post_user_name, post_user_link, post_date, post_body, post_id, responses
    )


def _fetch_resp(doc) -> list:
    resp_list = doc.xpath('//div[@class="post_list_ctn"]')
    responses = list()
    if resp_list:
        for answer in resp_list[0].xpath('.//div[@itemprop="suggestedAnswer"]'):
            info = answer.xpath('.//div[@class="resp_info"]')[0]
            resp_user_name = _get_user_name(info)
            resp_user_link = BASE_URL + info.xpath('.//div[@class="username"]//a')[0].attrib["href"]
            resp_date = _get_date(info)
            resp_body = answer.xpath('.//div[@class="resp_body "]')[0].text_content().strip()
            resp_id = _get_resp_id(answer.xpath('.//div[@class="resp_header"]')[0].attrib["id"])
            comments = list()
            comment_list = answer.xpath('.//div[@class="comment_list"]')
            if comment_list:
                comment_list = comment_list[0]
                for comment in comment_list.xpath('.//div[@class="comment_ctn"]'):
                    comment_user_name = comment.xpath('.//div[@class="username"]//a')[0].text_content()
                    comment_user_link = BASE_URL + comment.xpath('.//div[@class="username"]//a')[0].attrib["href"]
                    comment_date = comment.xpath('.//div[@class="username"]//span')[0].text_content()
                    comment_body = comment.xpath('.//div[@class="comment_body "]')[0].text_content().strip()
                    comment_id = _get_resp_id(comment.attrib["id"])
                    comments.append(_build_comment_dict(
                        comment_user_name, comment_user_link, comment_date, comment_body, comment_id))
            responses.append(_build_resp_dict(
                resp_user_name, resp_user_link, resp_date, resp_body, resp_id, comments
            ))
    return responses


def _get_user_name(element):
    return element.xpath('.//span[@itemprop="name"]')[0].text_content()

def _get_date(element):
    return element.xpath('.//time')[0].attrib["datetime"]

def _get_resp_id(id_str):
    return id_str[id_str.find('_') + 1:]

def _build_comment_dict(user_name, user_link, date, body, id):
    return {
        "COMMENT" : [
            {"USER_NAME" : user_name},
            {"USER_PROFILE_LINK" : user_link},
            {"COMMENT_BODY" : body},
            {"COPMMENT_DATE" : date},
            {"COMMENT_ID" : id}
        ]
    }

def _build_resp_dict(user_name, user_link, date, body, id, comments):
    return {
        "RESPONSE" : [
            {"USER_NAME" : user_name},
            {"USER_PROFILE_LINK" : user_link},
            {"RESPONSE_BODY" : body},
            {"RESPONSE_DATE" : date},
            {"RESPONSE_ID" : id},
            {"COMMENTS" : comments}
        ]
    }

def _build_post_dict(link, title, user_name, user_link, date, body, id, responses):
    return {
        "POST" : [
            {"POST_LINK": link},
            {"USER_NAME" : user_name},
            {"USER_PROFILE_LINK" : user_link},
            {"POST_TITLE" : title},
            {"POST_BODY" : body},
            {"POST_DATE" : date},
            {"POST_ID" : id},
            {"RESPONSES" : responses}
        ]
    }
