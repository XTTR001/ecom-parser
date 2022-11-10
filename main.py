from config import DATA_PATH, LOG_PATH, RESUTL_PATH, ORDER_MARKERS
from web_parser import WebParser


def main():
    web_parser = WebParser(DATA_PATH, LOG_PATH, RESUTL_PATH, ORDER_MARKERS)
    web_parser.start_search()

if __name__ == '__main__':
    main()
