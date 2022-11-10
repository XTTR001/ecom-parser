

class Website:

    def __init__(self, url):
        self.url = self.check_url(url)

    def check_url(self, url):
        if url.find('https://www.', 0) == -1:
            return self.form_url(url)
        return url

    def form_url(self, url):
        return f'https://www.{url}'

    def set_status(self, status):
        self.status = status
