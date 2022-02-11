from typing import Any


def to_bool(value: Any) -> bool:
    if not isinstance(value, str):
        return bool(value)
    if value:
        if value == "0" or value[0] == "F" or value[0] == "f":
            return False
        return True
    return False