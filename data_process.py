#TODO отрефакторить
def read_data_file():
    file1 = open('/Users/romanenko/Documents/Python Проекты/Parser Интернет магазины/source/dataTest.txt', "r")
    lines = file1.readlines()
    lines = [line.strip() for line in lines]
    file1.close
    return lines

def form_url(string):
    return f'https://www.{string}'

def get_urls():
    return [form_url(url) for url in read_data_file()]
