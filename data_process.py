websites = [
   'perekrestok.ru',
   'mvideo.ru',
   'dixy.ru',
   'metro-cc.ru',
   'auchan.ru',
   'ozon.ru'
]

def form_url(string):
    return f'https://www.{string}'

def get_urls():
    return [form_url(url) for url in websites]
