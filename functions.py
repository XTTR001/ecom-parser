from bs4 import BeautifulSoup
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


def get_all_links(page):
    '''Получаем все ссылки со страницы'''
    soup = BeautifulSoup(page, 'lxml')
    links = soup.find_all('a')
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


def get_html(url):
    '''Получаем контент страницы'''
    driver = webdriver.Chrome(
        ChromeDriverManager().install()
    )
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(1)
        return driver.page_source

    except Exception as _ex:
        write_log_file(url, _ex)

    finally:
        driver.close()
        driver.quit()


def process_url(url):
    '''Обрабатываем страничку. Если на ней можно покупать, сохраняем. Если нет идем дальше'''
    page_source = get_html(url)
    if find_order_page(str(page_source)):
        write_result_file(url, 'Можно покупать')
    else:
        write_result_file(url, 'Пока не знаю')
        # print(f'get_all_links(page_source)')


def start_search(urls):
    '''Начинаем поиск отсюда'''
    for url in urls:
        process_url(url)
