import httpx
import logging
import asyncio
from typing import Any, Dict, Optional

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class HotelAPI:
    """
    Класс для взаимодействия с API 1C-Hotel.

    Параметры:
    - base_url (str): Базовый URL API.
    - api_key (str): API-ключ для авторизации в сервисе.
    """

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    async def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None,
                            attempts: int = 3) -> Optional[Dict[str, Any]]:
        """
        Базовый метод для выполнения запросов к API.

        Параметры:
        - endpoint (str): Путь к API-методу.
        - method (str): HTTP-метод (GET, POST, PUT и т.д.).
        - data (Optional[Dict[str, Any]]): Тело запроса (для POST/PUT).
        - attempts (int): Количество попыток выполнения запроса.

        Возвращает:
        - Optional[Dict[str, Any]]: Ответ от API в формате словаря или None при неудаче.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        for attempt in range(attempts):
            try:
                logger.debug(f"Попытка {attempt + 1} запроса к {url}")
                async with httpx.AsyncClient() as client:
                    if method.upper() == "GET":
                        response = await client.get(url, headers=headers)
                    else:
                        response = await client.post(url, headers=headers, json=data)

                    response.raise_for_status()
                    logger.debug(f"Ответ получен: {response.json()}")
                    return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Ошибка HTTP статуса: {e}")
            except Exception as e:
                logger.error(f"Ошибка во время запроса: {e}")

        logger.error(f"Не удалось выполнить запрос после {attempts} попыток")
        return None

    async def get_room_availability(self) -> Optional[Dict[str, Any]]:
        """
        Получение информации о наличии свободных/занятых номеров.

        Возвращает:
        - Optional[Dict[str, Any]]: Информация о номерах в формате словаря или None при неудаче.
        """
        logger.debug("Получение информации о наличии номеров")
        return await self._make_request("/rooms/availability")

    async def get_room_info(self, room_id: str) -> Optional[Dict[str, Any]]:
        """
        Получение информации о конкретном номере.

        Параметры:
        - room_id (str): Идентификатор номера.

        Возвращает:
        - Optional[Dict[str, Any]]: Информация о номере в формате словаря или None при неудаче.
        """
        logger.debug(f"Получение информации о номере: {room_id}")
        return await self._make_request(f"/rooms/{room_id}")

    async def book_room(self, room_id: str, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Бронирование номера за пользователем.

        Параметры:
        - room_id (str): Идентификатор номера.
        - user_data (Dict[str, Any]): Информация о пользователе (имя, контактные данные и т.д.).

        Возвращает:
        - Optional[Dict[str, Any]]: Подтверждение бронирования или None при неудаче.
        """
        logger.debug(f"Бронирование номера: {room_id} для пользователя {user_data.get('name')}")
        return await self._make_request(f"/rooms/{room_id}/book", method="POST", data=user_data)


# Асинхронная функция для выполнения запросов к API
async def main():
    # Инициализация API-клиента
    api = HotelAPI(base_url="http://192.168.0.50:8181/hotel-test/api", api_key="eAqYAR9dveWUwSYJ2yfWX6E3DhCkYTumoS+oxCPD02g=")

    # Получение информации о наличии номеров
    availability = await api.get_room_availability()
    print("Доступные номера:", availability)

    # Получение информации о конкретном номере
    room_info = await api.get_room_info("101")
    print("Информация о номере 101:", room_info)

    # Бронирование номера
    booking = await api.book_room("101", {"name": "Иван Иванов", "email": "ivan@example.com"})
    print("Результат бронирования:", booking)


# Запуск асинхронной программы
if __name__ == "__main__":
    asyncio.run(main())
