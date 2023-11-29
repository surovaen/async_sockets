import asyncio
from asyncio import StreamReader, StreamWriter
from pathlib import Path
import random

from loguru import logger

from config import Config as settings
from enums import LogMessage, RequestType
from mixins import FileWorkerMixin


class FileServer(FileWorkerMixin):
    """Класс сервера получения/отправки файла."""

    HOST: str = settings.APP_HOST
    PORT: int = settings.APP_PORT

    async def start(self):
        """Метод запуска сервера."""

        server = await asyncio.start_server(
            client_connected_cb=self.file_callback,
            host=self.HOST,
            port=self.PORT,
        )

        async with server:
            logger.info(
                LogMessage.START_SERVER.value,
            )
            await server.serve_forever()

    async def file_callback(self, reader: StreamReader, writer: StreamWriter):
        """Метод обработки запроса клиента."""

        request = await reader.readline()
        request = request.rstrip(b'\n').decode()
        logger.info(
            LogMessage.GET_REQUEST.value.format(
                req=request,
            ),
        )

        if request == RequestType.GET.value:
            await self._send_file(writer)

        elif request == RequestType.POST.value:
            await self._save_file(reader)

        else:
            logger.error(
                LogMessage.WRONG_REQUEST.value.format(
                    req=request,
                ),
            )

            writer.close()
            await writer.wait_closed()

    async def _send_file(self, writer: StreamWriter):
        """Метод отправки рандомного файла в ответ на запрос клиента 'GET'."""

        media_list = [path for path in Path(settings.SERVER_DIR).iterdir()]

        if not media_list:
            message = f'{LogMessage.NOT_FOUND.value}\n'.encode()
            logger.info(
                LogMessage.NOT_FOUND.value,
            )

        else:
            filepath = random.choice(media_list)
            file_reader = await self._read_file(filepath)
            filename = (filepath.name + '\n').encode()
            message = filename + file_reader

            logger.info(
                LogMessage.SEND_FILE_SERVER.value.format(
                    file=filepath.name,
                ),
            )

        writer.write(message)
        await writer.drain()

        writer.close()
        await writer.wait_closed()

    async def _save_file(self, reader: StreamReader):
        """Метод сохранения полученного от клиента файла."""

        filename = await reader.readline()
        filename = filename.rstrip(b'\n').decode()
        filepath = '{dir}/{filename}'.format(
            dir=settings.SERVER_DIR,
            filename=filename,
        )

        filedata = await self._read_bytes(reader)

        logger.info(
            LogMessage.SAVE_FILE_SERVER.value.format(
                file=filepath,
            ),
        )

        await self._write_file(filepath, filedata)


if __name__ == '__main__':
    file_server = FileServer()

    try:
        asyncio.run(file_server.start())
    except KeyboardInterrupt:
        logger.info(
            LogMessage.STOP_SERVER.value,
        )
    except Exception as e:
        logger.error(
            LogMessage.ERROR_SERVER.value.format(
                exc=e,
            ),
        )
