import asyncio
import logging

import uvloop
from aiohttp import web

from db import close_pg
from db import init_db
from routes import setup_routes

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
log = logging.getLogger(__name__)


async def init_app() -> web.Application:
    app = web.Application()
    setup_routes(app)
    await init_db(app)
    app.on_shutdown.append(close_pg)
    return app


def main() -> None:
    app = init_app()
    log.info('Start app')
    web.run_app(app, host='0.0.0.0', port='8080')
    log.info('Stop app')


if __name__ == "__main__":
    main()
