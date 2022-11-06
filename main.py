import functions
import data_process
import config


def main():
    functions.start_search(data_process.get_urls(config.DATA_PATH))


if __name__ == '__main__':
    main()
