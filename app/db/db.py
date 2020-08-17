import asyncio
import datetime
import logging
import os
from typing import Dict, List, Set, Union

import sqlalchemy as sa
from aiopg.sa import create_engine
from aiopg.sa.connection import SAConnection
from aiopg.sa.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.ddl import CreateTable


log = logging.getLogger(__name__)

DATABASE = {
    'drivername': 'postgres',
    'host': os.getenv('PG_HOST', 'localhost'),
    'port': os.getenv('PG_PORT', '5434'),
    'username': os.getenv('POSTGRES_USER', 'ptest'),
    'password': os.getenv('POSTGRES_PASSWORD', 'ptest'),
    'database': os.getenv('POSTGRES_DB', 'ptest'),
}

ALARM_TABLE_NAME = 'alarm_clock'

dsn = str(URL(**DATABASE))

metadata = sa.MetaData()

alarm_clock_table = sa.Table(
    ALARM_TABLE_NAME , metadata, #  заменить на другую
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('description', sa.String(255), nullable=False),
    sa.Column('time_alarm', sa.DateTime, nullable=False),
)


async def create_table(engine: Engine):
    async with engine.acquire() as conn:
        #await conn.execute(CreateTable(alarm_clock_table))
        await conn.execute(f'''CREATE TABLE IF NOT EXISTS {ALARM_TABLE_NAME} (
               id serial PRIMARY KEY,
               description varchar(255) NOT NULL,
               time_alarm timestamp without time zone NOT NULL)''')


async def init_db(app) -> None:
    engine = await create_engine(dsn)
    await create_table(engine)
    app['db'] = engine
    log.info('Connected to database')


async def close_pg(app) -> None:
    app['db'].close()
    await app['db'].wait_closed()


async def create_alarm(conn: SAConnection, data) -> None:
    log.info('Create alarm %s', data.get('time_alarm'))
    stmt = alarm_clock_table.insert().values(**data)
    await conn.execute(stmt)


async def get_alarms(conn: SAConnection, *, ws: bool=False) -> List[Union[Set, Dict]]:
    now = datetime.datetime.now
    query = alarm_clock_table.select().where(alarm_clock_table.c.time_alarm >= now())
    records = await conn.execute(query)
    if ws:
        return [(row.description, row.time_alarm) async for row in records]
    return [{'description': row.description, 'alarm_time': str(row.time_alarm)} async for row in records]
