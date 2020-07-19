import os
import scrape

STUFF_DIR = os.getcwd() + os.sep + "stuff"
PAGES_DIR = os.getcwd() + os.sep + "pages"
MENU_TEMPLATE = STUFF_DIR + os.sep + "menu_template.html"
CHAPTER_TEMPLATE = STUFF_DIR + os.sep + "chapter_template.html"


class EpubPages:
    def __init__(self, name):
        self.name = name
        self.path = PAGES_DIR + os.sep + name
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.pages = []

    def create_pages(self, chapters):
        self.__create_menu(chapters)
        self.__create_chapters(chapters)

    def __create_menu(self, chapters):
        with open(MENU_TEMPLATE, 'r', encoding='utf-8') as f:
            contents = ''
            menu_html = self.path + os.sep + "menu.html"
            for chapter in chapters:
                contents += '<p><a href="%(index)s" class="calibre1">' % {'index': chapter.index + ".html"} + \
                    chapter.name + '</a></p>\n'
            with open(menu_html, 'w', encoding='utf-8') as m:
                m.write(f.read() % {'book': self.name, 'book_menu': contents})
                m.close()
                self.pages.append(menu_html)
            f.close()

    def __create_chapters(self, chapters):
        for chapter in chapters:
            file = self.path + os.sep + chapter.index + ".html"
            if os.path.exists(file):
                continue
            self.__create_chapter(file, chapter)

    def __create_chapter(self, file, chapter):
        if chapter.text == '':
            print(chapter.name + " is empty")
            return
        with open(CHAPTER_TEMPLATE, 'r', encoding='utf-8') as f:
            with open(file, 'w', encoding='utf-8') as html:
                context = f.read() % {'book': self.name, 'chapter_id': os.path.splitext(os.path.basename(file))[0],
                                      'chapter_name': chapter.name, 'chapter_content': chapter.text}
                html.write(context)
                html.close()
                self.pages.append(file)
            f.close()

    def get_pages(self):
        return self.pages
