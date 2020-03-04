# Medhelp-Scraper
A Python web scraper for medhelp.org
<hr>
This program uses https://medhelp.org/forums/list as an entry point, and scrapes
each question with its corresponding response / comments in each post under each category.
It saves the scraped webpage and stores information in JSON format.
<hr>
Third-party libraries used:
<ul>
  <li>lxml - handle html parsing</li>
  <li>selenium - handling infinity-scroll page scraping</li>
  <li>requests - handle web page fetching</li>
</ul>
<hr>
Example directory structure:
<pre>
Diabetes/Diabetes-Gestational/post.html
                             /post.csv
                             /post_1867426.html
                             /post_1867426.json
                             ...
        /Diabetes-Type1/...
</pre>
<hr>
The csv file contains the post link, number of answers, and number of comments
for each post in post.html.
<hr>
The JSON file structure:
<pre>
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
</pre>
