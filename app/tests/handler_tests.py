import aiohttp
import pytest

from app import init_app


@pytest.fixture
async def client(test_client):
    """Создаем фикстуру клиента."""
    app = await init_app()
    return await test_client(app)


async def test_get_handler(client):
    response = await client.get('/api/v1/alarm_clock')
    assert response.status == 200


@pytest.mark.parametrize(
    'parameters',
    (
        # data, status
        ({"description": "qwe", "time_alarm": "2021-11-17 15:45"}, 200),
        ({"description": "", "time_alarm": "2021-11-17 15:45"}, 500),
        ({"description": "qwe", "time_alarm": "2021-17-17  15:45"}, 500),
    )
)
async def test_get_handler(client, parameters):
    data, status = parameters
    response = await client.post('api/v1/alarm_clock', json=data)
    assert response.status == status


async def test_ws_handler(client):
    """Проверка работает ли ws."""
    res = await client.ws_connect('/ws')
    data = await res.receive_str()
    assert data == 'ws connect'
