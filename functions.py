from bs4 import BeautifulSoup
import requests
from random import choice
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import config


def find_order_page(page):
    '''Ищем на странице ключевые слова, связанные с покупкой'''
    order_words = config.ORDER_MARKERS
    for word in order_words:
        if page.find(word) != -1:
            return True
    return False


def check_link(link, url):
    if link.find(link, 0) == -1:
        return f'{url}{link}'


def get_all_links(page, url):
    '''Получаем все ссылки со страницы'''
    soup = BeautifulSoup(page, 'lxml')
    links = [check_link(link.get('href'), url) for link in soup.find_all('a')]
    return links


def write_log_file(url, message):
    '''Пишем лог ошибок при попытке подключиться'''
    fin = open(config.LOG_PATH, "a")
    fin.write(f'\n{url}; {message}')
    fin.close()


def write_result_file(url, message):
    '''Пишем результирующий файл'''
    fin = open(config.RESUTL_PATH, "a")
    fin.write(f'\n{url}; {message}')
    fin.close()

def random_headers():
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

def get_html(url):
    try:
        response = requests.get(url=url, headers=random_headers())
        print(f'{url}: {response}')
        write_log_file(url, {response})
        if response.status_code == 403:
            page_content = get_html_by_selenium(url)
            print('Попробовали селениумом')
            return page_content

        return response.text
    except Exception as ex:
        write_log_file(url, 'Не смогли подключиться')


def get_html_by_selenium(url):
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
        write_log_file(url, 'Не смогли подключиться')

    finally:
        driver.close()
        driver.quit()


def process_url(url):
    '''Обрабатываем страничку. Если на ней можно покупать, сохраняем. Если нет идем дальше'''
    if config.SELENIUM_MODE:
        page_source = get_html_by_selenium(url)
    else:
        page_source = get_html(url)

    if find_order_page(str(page_source)):
        write_result_file(url, 'Можно покупать')
    else:
        write_result_file(url, 'Не проверено')
        #print(f'{get_all_links(page_source, url)}')


def start_search(urls):
    '''Начинаем поиск отсюда'''
    start_time = time.time()
    for url in urls:
        print(f'Processing: {url}')
        process_url(url)

    print('Parsing is DONE!!!')
    print(f'Заняло {time.time() - start_time} секунд')
