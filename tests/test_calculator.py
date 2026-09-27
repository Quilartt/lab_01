import pytest

from toolkit.calculator import calculate
from toolkit.errors import (
    DivisionByZero,
    EmptyExpression,
    InvalidNumber,
    MissingOperand,
    MissingOperator,
    TwoOperators,
    UnknownSymbol,
)

# ---------Позитивные----------------------------------------------

def test_positive_01():
    assert calculate("345 * 27") == pytest.approx(9315.0, rel=1e-8)


def test_positive_02():
    assert calculate("8642 / 123") == pytest.approx(8642 / 123, rel=1e-8)


def test_positive_03():
    assert calculate("1234.56 + 799.44") == pytest.approx(2034.0, rel=1e-8)


def test_positive_04():
    assert calculate("100 + 200 + 300 + 400") == pytest.approx(1000.0, rel=1e-8)


def test_positive_05():
    assert calculate("9999 - 123 * 7") == pytest.approx(9138.0, rel=1e-8)


def test_positive_06():
    assert calculate("1000 / 7") == pytest.approx(1000 / 7, rel=1e-8)


def test_positive_07():
    assert calculate("-12345 + 6789") == pytest.approx(-5556.0, rel=1e-8)


def test_positive_08():
    assert calculate("-9876 * -5432") == pytest.approx(53646432.0, rel=1e-8)


def test_positive_09():
    assert calculate("  12345   -   2345   ") == pytest.approx(10000.0, rel=1e-8)


def test_positive_10():
    assert calculate("+3.14 * 100") == pytest.approx(314.0, rel=1e-8)


def test_positive_11():
    assert calculate("111 * 222 * 333") == pytest.approx(8205786.0, rel=1e-8)


def test_positive_12():
    assert calculate("0.1 + 0.2 + 0.3") == pytest.approx(0.6, rel=1e-8)


def test_positive_13():
    assert calculate("1 + 2 * 3 - 4 / 2 + 10 * 10 - 100") == pytest.approx(5.0, rel=1e-8)


def test_positive_14():
    assert calculate("999 * 999") == pytest.approx(998001.0, rel=1e-8)


def test_positive_15():
    assert calculate("-1000 / -8 + 250") == pytest.approx(375.0, rel=1e-8)


# -----------Негативные--------------------------

def test_negative_01():
    with pytest.raises(EmptyExpression):
        calculate("")


def test_negative_02():
    with pytest.raises(EmptyExpression):
        calculate("   ")


def test_negative_03():
    with pytest.raises(EmptyExpression):
        calculate("+")


def test_negative_04():
    with pytest.raises(UnknownSymbol):
        calculate("2+a")


def test_negative_05():
    with pytest.raises(UnknownSymbol):
        calculate("2 & 3")


def test_negative_06():
    with pytest.raises(TwoOperators):
        calculate("2*/3")


def test_negative_07():
    with pytest.raises(TwoOperators):
        calculate("2 * * 3")


def test_negative_08():
    with pytest.raises(MissingOperand):
        calculate("2+")


def test_negative_09():
    with pytest.raises(MissingOperand):
        calculate("2 *")


def test_negative_10():
    with pytest.raises(MissingOperand):
        calculate("*")


def test_negative_11():
    with pytest.raises(MissingOperator):
        calculate("2 3")


def test_negative_12():
    with pytest.raises(DivisionByZero):
        calculate("1/0")


def test_negative_13():
    with pytest.raises(DivisionByZero):
        calculate("10/0")


def test_negative_14():
    with pytest.raises(InvalidNumber):
        calculate("2..5")


def test_negative_15():
    with pytest.raises(InvalidNumber):
        calculate("2 + 3.")