import datetime


def validate_date_time(field: str, value: str, error):
    format = '%Y-%m-%d %H:%M'
    try:
        datetime.datetime.strptime(value, format)
    except ValueError:
        error(field, f'Incorrect format datetime,use: {format}')


alarm_clock_schema = {
    'time_alarm': {
        'type': 'string',
        'required': True,
        'empty': False,
        'validator': validate_date_time
    },
    'description': {
        'type': 'string',
        'required': True,
        'empty': False,
    }
}
