import frontier
import post_scraper

if __name__ == "__main__":
    lst = frontier.build()
    for dct in lst:
        for key in dct:
            post_scraper.run(key, dct[key])
            