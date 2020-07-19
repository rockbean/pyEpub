import zipfile
import os

PAGES_DIR = os.getcwd() + os.sep + "pages"
EPUBS_DIR = os.getcwd() + os.sep + "epubs"
STUFF_DIR = os.getcwd() + os.sep + "stuff"

MAIN_CONTENT = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
        <package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId">
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:title>%(book_name)s</dc:title>
        <dc:language>en</dc:language>
        <dc:creator>%(book_owner)s</dc:creator>
        <dc:identifier id="Bookid">urn:uuid:12345</dc:identifier>
        <meta name="cover" content="cover_jpg" />
        </metadata>
        <manifest>
            %(manifest)s
        </manifest>
        <spine toc="ncx">
            %(spine)s
        </spine>
        <guide>
            <reference href="OEBPS/menu.html" title="Contents" type="toc"/>
            <reference href="OEBPS/cover.html" title="Cover" type="cover"/>
        </guide>
    </package>
    '''

TOC_CONTENT = '''<?xml version="1.0" encoding="UTF-8"?>
		<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">
		<head>
			<meta name="dtb:uid" content="cool"/>
			<meta name="dtb:depth" content="1"/>
			<meta name="dtb:totalPageCount" content="0"/>
			<meta name="dtb:maxPageNumber" content="0"/>
		</head>
		<docTitle>
			<text>%(book_name)s</text>
		</docTitle>
		<navMap>
			%(navpoint)s
		</navMap>
		</ncx>
		'''


class MyEpub:
    def __init__(self, name):
        self.name = name

    def __open_epub(self):
        self.epub = zipfile.ZipFile(EPUBS_DIR + ".epub", 'w')

    def __close_epub(self):
        self.epub.close()

    def __create_mimetype(self):
        self.epub.write(STUFF_DIR+os.sep+"mimetype", 'mimetype',
                        compress_type=zipfile.ZIP_DEFLATED)

    def __create_container(self):
        self.epub.write(STUFF_DIR+os.sep+"container.xml", 'META-INF/container.xml',
                        compress_type=zipfile.ZIP_DEFLATED)

    def __create_assets(self):
        self.epub.write(STUFF_DIR + os.sep + "stylesheet.css", 'OEBPS/stylesheet.css',
                        compress_type=zipfile.ZIP_DEFLATED)
        self.epub.write(STUFF_DIR + os.sep + "page_styles.css", 'OEBPS/page_styles.css',
                        compress_type=zipfile.ZIP_DEFLATED)
        self.epub.write(STUFF_DIR + os.sep + self.name + os.sep + "cover.jpg", 'OEBPS/cover.jpg',
                        compress_type=zipfile.ZIP_DEFLATED)

    def __create_content(self, chapters):
        manifest = '<item  id = "css" href = "OEBPS/stylesheet.css" media-type = "text/css"/>\n'
        manifest += '<item id = "page_css" href = "OEBPS/page_styles.css" media-type = "text/css"/>\n'
        manifest += '<item id="cover" href="OEBPS/cover.html" media-type="application/xhtml+xml"/>\n'
        manifest += '<item id="menu" href="OEBPS/menu.html" media-type="application/xhtml+xml"/>\n'
        manifest += '<item id="cover_jpg" href="OEBPS/cover.jpg" media-type="image/jpeg"/>\n'
        manifest += '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>\n'

        spine = '<itemref idref="cover"/>\n'
        spine += '<itemref idref="menu"/>\n'

        page_path = PAGES_DIR + os.sep + self.name + os.sep
        self.epub.write(STUFF_DIR + os.sep + "cover.html", 'OEBPS/cover.html',
                        compress_type=zipfile.ZIP_DEFLATED)
        self.epub.write(page_path + "menu.html", 'OEBPS/menu.html',
                        compress_type=zipfile.ZIP_DEFLATED)

        for chapter in chapters:
            chapter_html = chapter.index + ".html"
            manifest += '<item id="%s" href="OEBPS/%s" media-type="application/xhtml+xml"/>\n' % (
                chapter.index, chapter_html)
            spine += '<itemref idref="%s"/>\n' % (chapter.index)
            self.epub.write(page_path + chapter_html, 'OEBPS/' + chapter_html,
                            compress_type=zipfile.ZIP_DEFLATED)
        self.epub.writestr('content.opf', MAIN_CONTENT % {
            'book_name': self.name,
            'book_owner': "J.K.Rowling",
            'manifest': manifest,
            'spine': spine},
            compress_type=zipfile.ZIP_STORED)

    def __create_toc(self, chapters):
        navpoint = '<navPoint id = "cover" playOrder = "0" ><navLabel><text>Cover</text></navLabel><content src="OEBPS/cover.html"/></navPoint>\n'
        navpoint += '<navPoint id = "menu" playOrder = "1" ><navLabel><text>Contents</text></navLabel><content src="OEBPS/menu.html"/></navPoint>\n'
        i = 2
        for chapter in chapters:
            navpoint += '<navPoint id = "%s" playOrder = "%d" ><navLabel><text>%s</text></navLabel><content src="OEBPS/%s"/></navPoint>\n' % (
                chapter.index, i, chapter.name, chapter.index + ".html"
            )
            i += 1
        self.epub.writestr('toc.ncx',
                           TOC_CONTENT % {
                               'book_name': self.name,
                               'navpoint': navpoint},
                           compress_type=zipfile.ZIP_STORED)

    def create_epub(self, chapters):
        self.__open_epub()
        self.__create_mimetype()
        self.__create_container()
        self.__create_assets()
        self.__create_content(chapters)
        self.__create_toc(chapters)
        self.__close_epub()
