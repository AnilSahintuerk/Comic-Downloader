from abc import abstractmethod
import requests
import os
import img2pdf
import shutil
import abc


class Scraper(abc.ABC):
    site = 1
    chapter = ''
    termination = []
    image = None
    current_page = ''
    page_url = ''
    main_url = ''
    flag = 0
    cwd = os.getcwd()

    def download_chapter(self):
        """
        downloads a whole chapter / issue from a comic
        termination logic is defined in check_if_end()
        :return:
        """
        self.create_folder()

        while self.flag != -1:
            self.download_page()

        os.chdir(self.cwd)
        return

    def download_page(self):
        """
        downloads the image on the page which is returned by the image_navigator()
        :return:
        """
        self.get_current_page()
        self.check_if_end()

        if self.flag == -1:
            return

        self.image_navigator()
        self.save_page()
        self.get_next_page()
        return

    def get_current_page(self):
        self.current_page = requests.get(self.page_url)
        return

    @abstractmethod
    def get_next_page(self):
        """
        updates to the next following page

        Variations for implementation:
        1. BS4 Object that clicks on 'next' button
        2. Manipulate the String

        Errors:
        PageDoesNotExist
        """
        pass

    @abstractmethod
    def image_navigator(self):
        """
        navigates us to the html object in the current_page
        """
        pass

    def save_page(self):
        """
        Save the image html object in a folder
        :return:
        """

        filename = str(self.site)
        with open(filename, 'wb') as image_file:
            for chunk in self.image.iter_content(100000):
                image_file.write(chunk)
            return

    @abstractmethod
    def check_if_end(self):
        """
        defines the termination rules and sets them in the termination list

        checks if the termination rules get violated
        :return:
        -1: terminate the downloading process
        0: continue
        """
        pass

    def create_folder(self):
        os.makedirs(str(self.chapter), exist_ok=True)
        path = os.path.join(os.getcwd(), str(self.chapter))
        os.chdir(path)
        return


"""----- END OF SCRAPER -----"""


class Converter(abc.ABC):
    cwd = ''
    folder = ''
    name = ''
    images = []

    def img_to_pdf(self):
        self.get_images()

        with open(self.name, "wb") as pdf:
            pdf.write(img2pdf.convert(self.images))

        shutil.rmtree(self.folder)

    def get_images(self):
        self.images = []
        folder = os.listdir(self.folder)

        for i in range(1, len(folder) + 1):
            self.images.append(os.path.join(self.folder, str(i)))

        return


"""----- END OF CONVERTER -----"""


class Make(abc.ABC):
    path = ''
    folder = ''

    @abc.abstractmethod
    def make_chapter(self, chapter):
        """
        calls the concrete implementation of the scraper and converter

        after calling folder of images get converted as the pdf of images
        :param chapter:
        :return:
        """
        pass

    def make_chapters(self, begin, end):
        for i in range(begin, end + 2):
            self.make_chapter(i)
        return


"""----- END OF MAKE -----"""
