import enum


class RequestType(enum.Enum):
    """Перечисление типов запросов."""

    GET = 'GET'
    POST = 'POST'


class LogMessage(enum.Enum):
    """Перечисление сообщений логгера."""

    START_SERVER = 'Сервер запущен'
    START_CLIENT = 'Клиент запущен'
    STOP_SERVER = 'Сервер остановлен пользователем'
    STOP_CLIENT = 'Клиент остановлен пользователем'
    ERROR_SERVER = 'Ошибка в работе сервера: {exc}'
    ERROR_CLIENT = 'Ошибка в работе клиента: {exc}'
    GET_REQUEST = 'Получен запрос от клиента: {req}'
    WRONG_REQUEST = 'Получен неверный запрос от клиента: {req}'
    NOT_FOUND = 'На сервере отсутствуют файлы, попробуйте повторить запрос позже'
    SEND_FILE_SERVER = 'Отправка файла "{file}" клиенту'
    SAVE_FILE_SERVER = 'Сохранение файла "{file}" от клиента'
    SEND_FILE_CLIENT = 'Отправка файла "{file}" на сервер'
    SAVE_FILE_CLIENT = 'Сохранение файла "{file}" с сервера'
    GET_FILE_REQUEST = 'Запрос файла с сервера'
