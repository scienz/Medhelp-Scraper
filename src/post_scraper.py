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
from csv_manager import save_as_csv
from lxml import html

BASE_URL = "https://medhelp.org"

# path_titles is the key in the dicts stored in the frontier
def run(path_titles: tuple, url: str):
    print("Crawling", path_titles[0], path_titles[1])
    save_as_csv(_build_path(path_titles, "post.csv"), 'w', [["Post Link", "Answer Number", "Comment Number"]])
    path = _build_path(path_titles, "post.html")
    if not file_exists(path):
        print("Local webpage doesn't exist. Crawling page " + url)
        page = get_scrolled_page(url)
        create_file(path, page)
    else:
        print("Local webpage found. Reading file " + path)
        page = read_file(path, 'rb')

    entries = _get_entry(page)
    count = 0
    for entry in entries:
        count += 1
        post_link = _get_post(entry)
        post_id = _get_post_id(post_link)
        post_file_name = _build_post_file_name(post_id)
        post_path = _build_path(path_titles, post_file_name)
        if not file_exists(post_path):
            post_page = get_page(post_link)
            create_file(post_path, post_page)
        else:
            post_page = read_file(post_path, 'rb')
        post_dict = _fetch_info(post_page, post_id, post_link)
        print("[" + str(round((count / len(entries) * 100), 2)) + "%] ", end = '')
        save_as_json(post_dict, _build_path(path_titles, _build_post_json_name(post_id)))
        ans_num, com_num = _get_ans_com_nums(entry)
        save_as_csv(_build_path(path_titles, "post.csv"), 'a', [[post_link, ans_num, com_num]])
    print("Finished Crawling " + path_titles[0] + " " + path_titles[1])
        
def _build_path(path_titles: tuple, file_name: str):
    return path_titles[0] + "/" + path_titles[1] + "/" + file_name
    
def _get_ans_com_nums(entry):
    spans = entry.xpath('.//div[@class="subj_stats"]//span')
    if len(spans) > 1:
        ans_num_text = spans[0].text_content()
        ans_num = ans_num_text[:ans_num_text.find(' ')]
    else:
        ans_num = 0

    if len(spans) > 2:
        com_num_text = spans[2].text_content()
        com_num = com_num_text[:com_num_text.find(' ')]
    else:
        com_num = 0

    return ans_num, com_num

def _get_post_id(post_link):
    return post_link[len(post_link) - post_link[::-1].find('/'):]

def _build_post_file_name(post_id):
    return "post_" + post_id + ".html"

def _build_post_json_name(post_id):
    return "post_" + post_id + ".json"

def _get_entry(page) -> list:
    doc = html.fromstring(page)
    return [e for e in doc.xpath('//div[@class="subj_entry"]')]

def _get_post(entry) -> list:
    link = entry.xpath('.//h2[@class="subj_title "]//a')[0]
    return BASE_URL + link.attrib["href"]

def _fetch_info(page, post_id, post_link):
    try:
        doc = html.fromstring(page)

        header = None
        temp = doc.xpath('//div[@class="subj_header"]')
        if temp:
            header = temp[0]

        post_title = None
        temp = header.xpath('.//h1[@class="subj_title"]')
        if temp:
            post_title = temp[0].text_content().strip()

        post_user_name = _get_user_name(header)

        post_user_link = None
        temp = header.xpath('.//div[@class="subj_info"]//a')
        if temp:
            post_user_link = BASE_URL + temp[0].attrib["href"]

        user_id = None
        if post_user_link:
            user_id = _get_post_id(post_user_link)
        post_date = _get_date(header)

        post_body = None
        temp = doc.xpath('//div[@id="subject_msg"]')
        if temp:
            post_body = temp[0].text_content().strip().replace(u"\u00a0", "")

        responses = _fetch_resp(doc)
        return _build_post_dict(
            post_link, post_title, post_user_name, post_user_link, post_date, post_body, post_id, user_id, responses
        )
    except Exception as e:
        print("Exception in _fetch_info: " + str(e))
        pass


def _fetch_resp(doc) -> list:
    resp_list = doc.xpath('//div[@class="post_list_ctn"]')
    responses = list()
    if resp_list:
        for answer in resp_list[0].xpath('.//div[@itemprop="suggestedAnswer"]'):

            info = None
            temp = answer.xpath('.//div[@class="resp_info"]')
            if temp:
                info = temp[0]

            resp_user_name = _get_user_name(info)

            resp_user_link = None
            temp = info.xpath('.//div[@class="username"]//a')
            if temp and "href" in temp[0].attrib:
                resp_user_link = BASE_URL + temp[0].attrib["href"]

            resp_date = _get_date(info)

            resp_body = None
            temp = answer.xpath('.//div[@class="resp_body "]')
            if temp:
                resp_body = temp[0].text_content().strip().replace(u"\u00a0", "")

            resp_id = None
            temp = answer.xpath('.//div[@class="resp_header"]')
            if temp:
                resp_id = _get_resp_id(temp[0].attrib["id"])

            comments = list()
            comment_list = answer.xpath('.//div[@class="comment_list"]')
            if comment_list:
                comment_list = comment_list[0]
                for comment in comment_list.xpath('.//div[@class="comment_ctn"]'):

                    comment_user_name = None
                    temp = comment.xpath('.//div[@class="username"]//a')
                    if temp:
                        comment_user_name = temp[0].text_content()

                    comment_user_link = None
                    temp = comment.xpath('.//div[@class="username"]//a')
                    if temp:
                        comment_user_link = BASE_URL + temp[0].attrib["href"]

                    comment_date = None
                    temp = comment.xpath('.//div[@class="username"]//span')
                    if temp:
                        if "data-timestamp" in temp[0].attrib:
                            comment_date = temp[0].attrib["data-timestamp"]
                        else:
                            comment_date = temp[0].text_content()

                    comment_body = None
                    if comment.xpath('.//div[@class="comment_body "]'):
                        comment_body = comment.xpath('.//div[@class="comment_body "]')[0].text_content().strip().replace(u"\u00a0", "")
                    elif comment.xpath('.//div[@class="comment_body"]'):
                        comment_body = comment.xpath('.//div[@class="comment_body"]')[0].text_content().strip().replace(u"\u00a0", "")
                    
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

def _build_post_dict(link, title, user_name, user_link, date, body, post_id, user_id, responses):
    return {
        "POST" : [
            {"POST_LINK": link},
            {"USER_NAME" : user_name},
            { "USER_ID" : user_id},
            {"USER_PROFILE_LINK" : user_link},
            {"POST_TITLE" : title},
            {"POST_BODY" : body},
            {"POST_DATE" : date},
            {"POST_ID" : post_id},
            {"RESPONSES" : responses}
        ]
    }
