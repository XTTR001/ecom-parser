from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import data_process
import time


def find_order_page(page):
    '''Ищем на странице ключевые слова, связанные с покупкой'''
    order_words = ['basket','cart','корзина', 'checkout', 'продукты', 'products']
    for word in order_words:
        if page.find(word) != -1:
            return True
    return False

def get_all_links(page):
    '''Получаем все ссылки со страницы'''
    soup = BeautifulSoup(page, 'lxml')
    links = soup.find_all('a')
    return links


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
        fin = open("/Users/romanenko/Documents/Python Проекты/Parser Интернет магазины/result/result.txt", "a")
        fin.write(f'\n{url}; {_ex}')
        fin.close()

        print('Наша ошибка',_ex)

    finally:
        driver.close()
        driver.quit()


def process_url(url):
    '''Обрабатываем страничку. Если на ней можно покупать, сохраняем. Если нет идем дальше'''
    page_source = get_html(url)
    if find_order_page(str(page_source)):
        fin = open("/Users/romanenko/Documents/Python Проекты/Parser Интернет магазины/result/result.txt", "a")
        fin.write(f'\n{url}; можно покупать')
        fin.close()
    else:
        fin = open("/Users/romanenko/Documents/Python Проекты/Parser Интернет магазины/result/result.txt", "a")
        fin.write(f'\n{url}; пока не выяснил')
        fin.close()
        #print(f'get_all_links(page_source)')

def start_search(urls):
    '''Начинаем поиск отсюда'''
    for url in urls:
        process_url(url)

def main():
    start_search(data_process.get_urls())



if __name__ == '__main__':
    main()
