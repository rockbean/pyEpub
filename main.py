import scrape
import epub
import pages

book = {"name": "The Ickabog", "home": "https://theickabog.com"}

if __name__ == '__main__':
    scraper = scrape.BookScraper(
        book["name"], book["home"])
    scraper.parse_home()
    scraper.parse_chapters()

    pages = pages.EpubPages(book["name"])
    chapters = scraper.get_chapters()

    pages.create_pages(chapters)

    epub = epub.MyEpub(book["name"])
    epub.create_epub(chapters)
