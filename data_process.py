#TODO отрефакторить
def read_data_file(file):
    file1 = open(file, "r")
    lines = [line.strip() for line in file1.readlines()]
    file1.close
    return lines

def form_url(string):
    return f'https://www.{string}'

def get_urls(file):
    return [form_url(url) for url in read_data_file(file)]
