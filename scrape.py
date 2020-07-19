from requests.adapters import HTTPAdapter
from requests_html import HTMLSession
import re
import time
import os

PAGES_DIR = os.getcwd() + os.sep + "pages"


class BookChapter:
    def __init__(self, name, index, url):
        self.name = name
        self.index = index
        self.url = url
        self.text = ''


class BookScraper:
    def __init__(self, name, url):
        self.name = name
        self.homepage = url
        self.chapters = []

    def parse_home(self):
        session = HTMLSession()
        session.mount('http://', HTTPAdapter(max_retries=3))
        session.mount('https://', HTTPAdapter(max_retries=3))
        print("parsing: " + self.homepage + "/read-the-story/")
        try:
            with session.get(self.homepage + "/read-the-story/", timeout=(5, 10)) as buf:
                chapters = buf.html.find('#chapters', first=True)
                if chapters == None:
                    return
                chapter_list = chapters.find('.chapter__box')
                for chapter in chapter_list:
                    url = chapter.links.pop()
                    name = re.sub(r'Chapter [\d]*', '',
                                  chapter.full_text.strip())
                    name = name.strip()
                    index = re.search(
                        r'Chapter [\d]*', chapter.full_text.strip())
                    index = index.group()
                    chapter = BookChapter(name, index, url)
                    self.chapters.append(chapter)
        except Exception as e:
            print(e)
        print("finish: " + self.homepage + "/read-the-story/")
        session.close()

    def parse_chapters(self):
        session = HTMLSession()
        session.mount('http://', HTTPAdapter(max_retries=3))
        session.mount('https://', HTTPAdapter(max_retries=3))
        for chapter in self.chapters:
            html = PAGES_DIR + os.sep + self.name + os.sep + chapter.index + ".html"
            if os.path.exists(html):
                continue
            self.parse_chapter(session, chapter)
            time.sleep(5)
        session.close()

    def parse_chapter(self, session, chapter):
        print("parsing: " + self.homepage + chapter.url)
        try:
            with session.get(self.homepage + chapter.url, timeout=(5, 10)) as buf:
                content = buf.html.find('.entry-content', first=True)
                if content != None:
                    chapter.text = content.html.encode("utf-8").decode("utf-8")
        except Exception as e:
            print(e)
        print("finish: " + self.homepage + chapter.url)

    def get_chapters(self):
        return self.chapters
