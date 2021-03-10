import comic
import bs4
import requests
import os
import re


class TWDScraper(comic.Scraper):
    pattern = re.compile(r'https:\S+.jpg')
    chapter_urls = []

    def __init__(self, chapter):
        self.chapter = chapter
        self.main_url = 'https://readcomiconline.to/Comic/The-Walking-Dead/Issue-' + str(chapter) + '#'
        self.page_url = self.main_url + str(self.site)

    def download_chapter(self):
        """
        downloads a whole chapter / issue from a comic
        termination logic is defined in check_if_end()
        :return:
        """
        self.create_folder()
        self.get_current_page()

        self.chapter_urls = re.findall(self.pattern, self.current_page.text)

        for image_url in self.chapter_urls:
            self.image = requests.get(image_url)  # download image
            self.image.raise_for_status()
            self.save_page()
            self.site += 1

        os.chdir(self.cwd)
        return

    def get_next_page(self):
        pass

    def check_if_end(self):
        pass

    def image_navigator(self):
        pass


class TWDConverter(comic.Converter):

    def __init__(self, folder):
        self.cwd = os.path.join(os.getcwd(), 'The_Walking_Dead')
        self.name = str(folder) + '.pdf'
        self.folder = os.path.join(self.cwd, str(folder))
        os.chdir(self.cwd)


class TWDMake(comic.Make):

    def __init__(self):
        self.folder = 'The_Walking_Dead'
        self.path = os.path.join(os.getcwd(), self.folder)
        os.makedirs(self.path, exist_ok=True)
        os.chdir(self.path)

    def make_chapter(self, chapter):
        TWDScraper(chapter).download_chapter()
        TWDConverter(chapter).img_to_pdf()
        return
