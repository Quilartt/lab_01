from .errors import AbsoluteZero, IncompatibleUnits, InvalidValue, UnknownUnit
import math

LENGTH = {"km": 1000, "m": 1, "cm": 0.01, "mm": 0.001}

MASS = {"g": 1, "kg": 1000}

TEMP = {"c", "f", "k"}


def convert_from_c(value: float, to_unit: str) -> float:
    """Переводит температуру из градусов Цельсия в указанную единицу."""

    if value + 273.15 < 0:
        raise AbsoluteZero("Температура ниже абсолютного нуля")
    elif to_unit == "k":
        result = value + 273.15
    elif to_unit == "f":
        result = value * 9 / 5 + 32
    else:
        result = value
    return result


def convert(value: str, from_unit: str, to_unit: str) -> float:
    """Конвертирует из одной величины в другую"""

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    if not math.isfinite(value):
        raise InvalidValue(f"Недопустимое значение: {value}")
    else:
        value = float(value)
    
    # Валидация входных единиц измерения
    known = set(LENGTH) | set(MASS) | set(TEMP)
    if from_unit not in known:
        raise UnknownUnit(f"Недопустимая единица измерения: {from_unit}")
    if to_unit not in known:
        raise UnknownUnit(f"Недопустимая единица измерения: {to_unit}")

    # Конвертер длин
    if from_unit in LENGTH:
        if to_unit in LENGTH:
            result = LENGTH[from_unit] / LENGTH[to_unit] * value
        else: 
            raise IncompatibleUnits(f"Невозможен перевод из {from_unit} в {to_unit}")

    # Конвертер масс
    elif from_unit in MASS:
        if to_unit in MASS:
            result = MASS[from_unit] / MASS[to_unit] * value
        else: 
            raise IncompatibleUnits(f"Невозможен перевод из {from_unit} в {to_unit}")

    # Конвертер температур
    elif from_unit in TEMP:
        if to_unit not in TEMP:
            raise IncompatibleUnits(f"Невозможен перевод из {from_unit} в {to_unit}")
        else:
            if from_unit == "c":
                result = convert_from_c(value, to_unit)
            elif from_unit == "k":
                temp_c = value - 273.15
                result = convert_from_c(temp_c, to_unit)
            elif from_unit == "f":
                temp_c = (value - 32) * 5 / 9
                result = convert_from_c(temp_c, to_unit)
    return result








