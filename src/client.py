import argparse
import asyncio
from asyncio import StreamReader, StreamWriter
from pathlib import Path

from loguru import logger

from config import Config as settings
from enums import LogMessage, RequestType
from mixins import FileWorkerMixin


class FileClient(FileWorkerMixin):
    """Класс клиента отправки/получения файлов."""

    HOST: str = settings.APP_HOST
    PORT: int = settings.APP_PORT

    def __init__(self, filepath: str = None):
        """Инициализация параметров."""

        self.file = filepath
        self._reader = None
        self._writer = None
        self.request = None

    @property
    def reader(self) -> StreamReader:
        """Проперти reader клиента."""

        return self._reader

    @reader.setter
    def reader(self, value: StreamReader):
        """Сеттер reader клиента."""

        self._reader = value

    @property
    def writer(self) -> StreamWriter:
        """Проперти writer клиента."""

        return self._writer

    @writer.setter
    def writer(self, value: StreamWriter):
        """Сеттер writer клиента."""

        self._writer = value

    async def send_request(self,):
        """Метод отправки запроса на сервер."""

        self.reader, self.writer = await asyncio.open_connection(
            host=self.HOST,
            port=self.PORT,
        )

        if self.file:
            logger.info(
                LogMessage.SEND_FILE_CLIENT.value.format(
                    file=self.file,
                ),
            )

            self.request = message = RequestType.POST.value
            message = (message + '\n').encode() + await self._add_file()

            self.writer.write(message)
            await self.writer.drain()

            self.writer.close()
            await self.writer.wait_closed()

        else:
            logger.info(
                LogMessage.GET_FILE_REQUEST.value,
            )

            self.request = message = RequestType.GET.value
            message = (message + '\n').encode()

            self.writer.write(message)
            await self.writer.drain()

    async def _add_file(self) -> bytes:
        """Метод добавления данных отправляемого файла."""

        filedata = await self._read_file(self.file)
        filename = Path(self.file).name
        message = (filename + '\n').encode() + filedata

        return message

    async def get_file(self):
        """Метод получения файла с сервера по запросу."""

        response = await self.reader.readline()
        response = response.rstrip(b'\n').decode()

        if response == LogMessage.NOT_FOUND.value:
            logger.info(
                LogMessage.NOT_FOUND.value,
            )
        else:
            filepath = '{dir}/{filename}'.format(
                dir=settings.CLIENT_DIR,
                filename=response,
            )

            filedata = await self._read_bytes(self.reader)

            logger.info(
                LogMessage.SAVE_FILE_CLIENT.value.format(
                    file=filepath,
                ),
            )

            await self._write_file(filepath, filedata)

        self.writer.close()
        await self.writer.wait_closed()


async def main(file=None):
    """Функция запуска клиента."""

    file_client = FileClient(file)
    await file_client.send_request()

    if file_client.request == RequestType.GET.value:
        await file_client.get_file()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Запрос на файловый сервер')
    parser.add_argument('-f', '--file', type=str, default=None, help='Файл')
    args = parser.parse_args()

    try:
        logger.info(
            LogMessage.START_CLIENT.value,
        )
        asyncio.run(main(args.file))
    except KeyboardInterrupt:
        logger.info(
            LogMessage.STOP_CLIENT.value,
        )
    except Exception as e:
        logger.error(
            LogMessage.ERROR_CLIENT.value.format(
                exc=e,
            ),
        )
