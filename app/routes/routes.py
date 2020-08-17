from aiohttp.web import Application

from views import AlarmClockHandler
from views import websocket_handler


def setup_routes(app: Application) -> None:
    """Создаем маршруты приложения."""

    app.router.add_route('*', r'/api/v1/alarm_clock', AlarmClockHandler)
    app.router.add_get('/ws', websocket_handler)
