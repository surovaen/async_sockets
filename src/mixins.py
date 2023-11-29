from asyncio import StreamReader

import aiofiles

from config import Config as settings


class FileWorkerMixin:
    """Класс-миксин работы с файловыми данными."""

    async def _read_file(self, filepath: str) -> bytes:
        """Метод чтения файла."""

        async with aiofiles.open(filepath, 'rb') as file:
            return await file.read()

    async def _write_file(self, filepath: str, data: bytes):
        """Метод записи файла."""

        async with aiofiles.open(filepath, 'wb') as file:
            await file.write(data)

    async def _read_bytes(self, reader: StreamReader) -> bytes:
        """Метод чтения данных файла из ридера."""

        data = b''

        while (chunk := await reader.read(settings.SIZE)) != b'':
            data += chunk

        return data
