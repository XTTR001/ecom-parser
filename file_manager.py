

class FileManager:
    ''' Класс, который обрабатывает файлы для последующей передачи в парсинг
        или для записи в файл
    '''

    def __init__(self, input_data_file, log_file, result_file):
        self.input_data_file = input_data_file
        self.log_file = log_file
        self.result_file = result_file

    def read_file_to_list(self, file):
        try:
            file1 = open(file, "r")
            lines = [line.strip() for line in file1.readlines()]
            file1.close
        except Exception as _ex:
            return _ex
        return lines

    def get_file_strings(self):
        return [file_string for file_string in self.read_file_to_list(self.input_data_file)]

    def write_log_file(self, url, message):
        '''Пишем лог ошибок при попытке подключиться'''
        fin = open(self.log_file, "a")
        fin.write(f'\n{url}; {message}')
        fin.close()

    def write_result_file(self, url, message):
        '''Пишем результирующий файл'''
        fin = open(self.result_file, "a")
        fin.write(f'\n{url}; {message}')
        fin.close()
