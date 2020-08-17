from typing import Any, Dict

from cerberus import Validator

from .errors import ValidateError


def validate_data(data: Dict[Any, Any], schema: Dict[Any, Any], **kwargs) -> Dict[Any, Any]:
    validator = Validator(schema, **kwargs)
    if not validator.validate(data):
        raise ValidateError(f'Validate data error: {validator.errors}')
    return validator.document
