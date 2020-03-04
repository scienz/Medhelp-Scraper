import requests

def get_page(url: str):
    headers = {
        "Referer": "https://www.medhelp.org",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    r = requests.get(url, headers = headers)
    return r.text
