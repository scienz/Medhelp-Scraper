import frontier
import post_scraper

if __name__ == "__main__":
    lst = frontier.build()
    dct = lst[0]
    for key in dct:
        post_scraper.run(key, dct[key])
