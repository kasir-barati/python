import random
import pytest


def sum(a: int, b: int) -> int:
    return a + b


class DummyNumber:
    def get_number(self) -> int:
        return random.randint(1, 100)


@pytest.fixture
def dummy_number() -> DummyNumber:
    return DummyNumber()


@pytest.mark.parametrize("a,b", [(5, 6)])
def test_sum_with_dummy_number1(dummy_number: DummyNumber, a: int, b: int) -> None:
    dummy_value = dummy_number.get_number()

    result = sum(a + dummy_value, b)

    assert isinstance(result, int)


@pytest.mark.parametrize("a,b", [(3, 4)])
def test_sum_with_dummy_number2(a: int, b: int, dummy_number: DummyNumber) -> None:
    dummy_value = dummy_number.get_number()

    result = sum(a + dummy_value, b)

    assert isinstance(result, int)
