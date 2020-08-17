import asyncio
import copy
import datetime
from json import JSONDecodeError

from aiohttp.web import Response, View, WebSocketResponse, json_response
from aiopg.sa.engine import Engine

from db import create_alarm, get_alarms
from utils import alarm_clock_schema, validate_data


class AlarmClockHandler(View):
    """Хэндлер для создания и вывода всех будильников."""

    async def get(self) -> Response:
        db: Engine = self.request.app['db']
        async with db.acquire() as conn:
            alarms = await get_alarms(conn)
        return json_response(alarms)

    async def post(self) -> Response:
        try:
            request_json = await self.request.json()
        except JSONDecodeError:
            return json_response({'status': 'bad request'}, status=400)
        data = validate_data(request_json, alarm_clock_schema)
        db: Engine = self.request.app['db']
        async with db.acquire() as conn:
            await create_alarm(conn, data)
        return Response()


async def websocket_handler(request):
    """Websocket хэнждлер, для сигнализирования сработанного будильника."""
    ws = WebSocketResponse()
    await ws.prepare(request)
    now = datetime.datetime.now()
    await ws.send_str('ws connect')
    await ws.send_str(f'Now: {now}')
    db: Engine = request.app['db']
    async with db.acquire() as conn:
        alarm_clocks = await get_alarms(conn, ws=True)
    #  TODO логику можно вынести в отдельный сервис что бы не грязнить хэндлер.
    while alarm_clocks:
        intems = copy.deepcopy(alarm_clocks)
        now = datetime.datetime.now()
        for enum, (description, date) in enumerate(intems):
            #  >= потому что, если случится race condition
            #  мы убрали все будильники которые были до текущего времени.
            if now >= date:
                await ws.send_str(f'{description}, {date}')
                del alarm_clocks[enum]
                break
        await asyncio.sleep(20)
