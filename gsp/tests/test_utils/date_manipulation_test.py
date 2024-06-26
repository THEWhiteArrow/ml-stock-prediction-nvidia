import datetime
import pytest
from gsp.utils.date_utils import get_nth_previous_working_date


@pytest.mark.dev
def test_get_nth_previous_working_date_correctly_returns_within_the_same_week():
    # --- SETUP ---
    monday = datetime.date(year=2024, month=4, day=29)
    thursday = monday + datetime.timedelta(days=3)
    friday = monday + datetime.timedelta(days=4)

    # --- ASSERT ---
    assert get_nth_previous_working_date(3, thursday) == monday
    assert get_nth_previous_working_date(4, friday) == monday


@pytest.mark.dev
def test_get_nth_previous_working_date_correctly_returns_across_weeks():
    # --- SETUP ---
    thursday_week_18 = datetime.date(year=2024, month=5, day=2)
    thursday_week_ealier = thursday_week_18 - datetime.timedelta(days=7)

    friday_week_18 = datetime.date(year=2024, month=5, day=3)
    friday_week_ealier = friday_week_18 - datetime.timedelta(days=7)

    # --- ASSERT ---
    assert get_nth_previous_working_date(5, thursday_week_18) == thursday_week_ealier
    assert get_nth_previous_working_date(5, friday_week_18) == friday_week_ealier
    assert get_nth_previous_working_date(6, friday_week_18) == thursday_week_ealier


@pytest.mark.dev
def test_get_nth_previous_working_date_can_get_nth_future_working_date_within_the_same_week():
    # --- SETUP ---
    tuesday = datetime.date(year=2024, month=4, day=29)
    thursday = tuesday + datetime.timedelta(days=2)
    friday = tuesday + datetime.timedelta(days=3)

    # --- ASSERT ---
    assert get_nth_previous_working_date(-2, tuesday) == thursday
    assert get_nth_previous_working_date(-3, tuesday) == friday


@pytest.mark.dev
def test_get_nth_previous_working_date_can_get_nth_future_working_date_across_weeks_v2():
    current_week = [datetime.date(year=2024, month=5, day=13 + i) for i in range(7)]
    next_week = [datetime.date(year=2024, month=5, day=20 + i) for i in range(7)]

    assert get_nth_previous_working_date(-1, current_week[4]) == next_week[0]
    assert get_nth_previous_working_date(-2, current_week[4]) == next_week[1]
    assert get_nth_previous_working_date(-5, current_week[4]) == next_week[4]

    assert get_nth_previous_working_date(-1, current_week[5]) == next_week[0]
    assert get_nth_previous_working_date(-2, current_week[5]) == next_week[1]
    assert get_nth_previous_working_date(-5, current_week[5]) == next_week[4]

    assert get_nth_previous_working_date(-1, current_week[0]) == current_week[1]
    assert get_nth_previous_working_date(-2, current_week[0]) == current_week[2]
    assert get_nth_previous_working_date(-5, current_week[0]) == next_week[0]

    assert get_nth_previous_working_date(-1, current_week[2]) == current_week[3]
    assert get_nth_previous_working_date(-2, current_week[2]) == current_week[4]
    assert get_nth_previous_working_date(-3, current_week[2]) == next_week[0]


def test_date_to_isoformat_will_provide_prefix_zeros():
    # --- SETUP ---
    date = datetime.date(year=2024, month=5, day=2)

    # --- ASSERT ---
    assert date.isoformat() == "2024-05-02"


@pytest.mark.parametrize(
    "date_iso, step, expected_iso",
    [
        ("2024-02-20", -10, "2024-03-05"),
        ("2024-03-05", 10, "2024-02-20"),
    ],
)
def test_get_nth_previous_working_date_with_leap_years(date_iso: str, step: int, expected_iso: str):
    # --- SETUP ---
    date = datetime.datetime.fromisoformat(date_iso).date()
    expected = datetime.datetime.fromisoformat(expected_iso).date()

    # --- ASSERT ---
    assert get_nth_previous_working_date(step, date) == expected


def test_get_nth_previous_working_date_with_value_0():
    # --- SETUP ---
    friday = datetime.date(year=2024, month=5, day=24)
    thursday = friday - datetime.timedelta(days=1)
    saturaday = friday + datetime.timedelta(days=1)
    sunday = friday + datetime.timedelta(days=2)

    assert get_nth_previous_working_date(0, thursday) == thursday
    assert get_nth_previous_working_date(0, friday) == friday
    assert get_nth_previous_working_date(0, saturaday) == friday
    assert get_nth_previous_working_date(0, sunday) == friday
