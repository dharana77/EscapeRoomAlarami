import pytest
from main import is_date_in_twice


@pytest.mark.parametrize("next_date", 29)
@pytest.mark.parametrize("table_text_twice_dates", [26, 27, 28, 29, 30, 31, 1, 2, 3])
def test_is_date_in_twice(next_date: int, table_text_twice_dates: list):
    result = is_date_in_twice(next_date=next_date, table_text_twice_dates=table_text_twice_dates)
    assert result
