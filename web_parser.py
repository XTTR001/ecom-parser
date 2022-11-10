from bs4 import BeautifulSoup
import requests
from random import choice
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from file_manager import FileManager
from website import Website


class WebParser:

    def __init__(self, input_data_file, log_file, result_file, order_markers, selenium_mode=False):

        self.selenium_mode = selenium_mode
        self.file_manager = FileManager(input_data_file, log_file, result_file)
        self.websites = [Website(url)
                         for url in self.file_manager.get_file_strings()]
        self.order_markers = order_markers

    def start_search(self):
        '''Начинаем поиск отсюда'''
        start_time = time.time()
        for website in self.websites:
            print(f'Processing: {website.url}')
            self.process_url(website.url)

        print('Parsing is DONE!!!')
        print(f'Заняло {time.time() - start_time} секунд')

    def process_url(self, url):
        '''Обрабатываем страничку. Если на ней можно покупать, сохраняем. Если нет идем дальше'''
        if self.selenium_mode:
            page_source = self.get_html_by_selenium(url)
        else:
            page_source = self.get_html(url)

        if self.find_order_page(str(page_source)):
            self.file_manager.write_result_file(url, 'Можно покупать')
        else:
            self.file_manager.write_result_file(url, 'Можно покупать')

    def get_html(self, url):
        try:
            response = requests.get(url=url, headers=self.get_headers())
            print(f'{url}: {response}')
            self.file_manager.write_log_file(url, {response})

            if response.status_code == 403:
                page_content = self.get_html_by_selenium(url)
                print('Попробовали селениумом')
                return page_content

            return response.text

        except Exception as ex:
            self.file_manager.write_log_file(url, 'Не смогли подключиться')

    def get_headers(self):
        HEADERS = {
            "User-Agent": choice(config.DESKTOP_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }

        return HEADERS

    def get_html_by_selenium(self, url):
        '''Возвращаем контент страницы, использя Selenium'''
        driver = webdriver.Chrome(
            ChromeDriverManager().install()
        )
        driver.maximize_window()

        try:
            driver.get(url=url)
            time.sleep(1)
            return driver.page_source

        except Exception as _ex:
            self.file_manager.write_log_file(url, 'Не смогли подключиться')

        finally:
            driver.close()
            driver.quit()


    def find_order_page(self, page):
        '''Ищем на странице ключевые слова, связанные с покупкой'''
        order_words = self.order_markers
        for word in order_words:
            if page.find(word) != -1:
                return True
        return False
