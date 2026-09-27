import pytest

from toolkit.converter import convert
from toolkit.errors import (
    AbsoluteZero,
    IncompatibleUnits,
    UnknownUnit,
)

# -----Позитивные-------------------------------

def test_positive_01():
    assert convert("3456", "mm", "m") == pytest.approx(3.456, rel=1e-8)


def test_positive_02():
    assert convert("12345", "cm", "km") == pytest.approx(0.12345, rel=1e-8)


def test_positive_03():
    assert convert("0.007", "km", "mm") == pytest.approx(7000.0, rel=1e-8)


def test_positive_04():
    assert convert("12.34", "m", "cm") == pytest.approx(1234.0, rel=1e-8)


def test_positive_05():
    assert convert("2.5", "kg", "g") == pytest.approx(2500.0, rel=1e-8)


def test_positive_06():
    assert convert("3456", "g", "kg") == pytest.approx(3.456, rel=1e-8)


def test_positive_07():
    assert convert("100", "c", "f") == pytest.approx(212.0, rel=1e-8)


def test_positive_08():
    assert convert("27", "c", "k") == pytest.approx(300.15, rel=1e-8)


def test_positive_09():
    assert convert("98.6", "f", "c") == pytest.approx(37.0, rel=1e-8)


def test_positive_10():
    assert convert("1000", "MM", "M") == pytest.approx(1.0, rel=1e-8)



# -------Негативные------------------------------------

def test_negative_01():
    with pytest.raises(AbsoluteZero):
        convert("-274", "c", "k")


def test_negative_02():
    with pytest.raises(AbsoluteZero):
        convert("-460", "f", "c")


def test_negative_03():
    with pytest.raises(AbsoluteZero):
        convert("-1", "k", "c")


def test_negative_04():
    with pytest.raises(IncompatibleUnits):
        convert("1000", "kg", "m")


def test_negative_05():
    with pytest.raises(IncompatibleUnits):
        convert("1", "m", "c")


def test_negative_06():
    with pytest.raises(IncompatibleUnits):
        convert("500", "mm", "g")


def test_negative_07():
    with pytest.raises(IncompatibleUnits):
        convert("100", "k", "m")


def test_negative_08():
    with pytest.raises(UnknownUnit):
        convert("1", "foo", "m")


def test_negative_09():
    with pytest.raises(UnknownUnit):
        convert("1", "m", "bar")


def test_negative_10():
    with pytest.raises(UnknownUnit):
        convert("1", "mile", "km")
