from functools import lru_cache

import pytest

from pyaoc.y_2025.d_02 import IDRange, find_invalid_p2


@pytest.mark.parametrize(
    "idr_str, expected_singleton",
    [
        ("12341234-12341234", 12341234),  # 1234 × 2
        ("123123123-123123123", 123123123),  # 123 × 3
        ("1212121212-1212121212", 1212121212),  # 12 × 5
        ("1111111-1111111", 1111111),  # 1 × 7
    ],
)
def test_find_invalid_p2_simple(idr_str, expected_singleton):
    idr = IDRange.from_string(idr_str)
    result = find_invalid_p2(idr)
    assert result == {expected_singleton}


@pytest.mark.parametrize(
    "idr_str, expected",
    [
        # All 2-digit “aa” patterns
        ("10-99", {11, 22, 33, 44, 55, 66, 77, 88, 99}),
        # Range clipped to middle (only 22 and 33 fall into the interval)
        ("12-34", {22, 33}),
        # Single value, not a repetition of any shorter pattern
        ("10-10", set()),
        # Single exact repeated pattern of 2 digits
        ("1212-1212", {1212}),
        # 4-digit range containing both 2×2-digit and 4×1-digit patterns
        # 1010, 1111, 1212, ..., 1919 that lie in [1000, 2000]
        ("1000-2000", {1010, 1111, 1212, 1313, 1414, 1515, 1616, 1717, 1818, 1919}),
        # Mixed 2-/3-digit range: hits 99 (9×2) and 111 (1×3)
        ("90-150", {99, 111}),
    ],
)
def test_find_invalid_p2_expected_sets(idr_str, expected):
    idr = IDRange.from_string(idr_str)
    result = find_invalid_p2(idr)
    assert result == expected


@lru_cache
def _is_repeated_pattern(n: int) -> bool:
    s = str(n)
    length = len(s)
    for chunk_len in range(1, length // 2 + 1):
        if length % chunk_len != 0:
            continue
        repeats = length // chunk_len
        if repeats < 2:
            continue
        chunk = s[:chunk_len]
        if chunk * repeats == s:
            return True
    return False


@pytest.mark.parametrize(
    "idr_str",
    [
        "10-99",
        "1000-2000",
        "1212-1212",
        "12341234-12341234",
        "123123123-123123123",
        "1212121212-1212121212",
        "1111111-1111111",
        "90-150",
        f"{10**3}-{10**4}",
    ],
)
def test_find_invalid_p2_all_repeated(idr_str):
    idr = IDRange.from_string(idr_str)
    result = find_invalid_p2(idr)
    assert len(result) > 0, "Expected at least one invalid ID"
    for value in result:
        assert _is_repeated_pattern(value), f"{value} is not a repeated pattern"


@pytest.mark.parametrize(
    "idr_str",
    [
        "10-10",
        "15-15",  # single 2-digit non-repetition
        "1234-1234",  # single 4-digit non-repetition
        "1203-1203",  # mixed digits, not a repetition
    ],
)
def test_find_invalid_p2_empty_when_no_invalids(idr_str):
    idr = IDRange.from_string(idr_str)
    assert find_invalid_p2(idr) == set()


@lru_cache
def raw_repeated_generator(chunk: str, repeats: int) -> int:
    return int(chunk * repeats)


def test_find_invalid_p2_on_large_range():
    min_n, max_n = 10**5, 10**6
    idr = IDRange.from_string(f"{min_n}-{max_n}")
    result = find_invalid_p2(idr)

    assert all(n in range(min_n, max_n + 1) for n in result), "Some invalid IDs are out of range"

    raw = set()
    for n in range(min_n, max_n + 1):
        if _is_repeated_pattern(n):
            raw.add(n)
    assert result == raw, "Mismatch between computed and raw repeated patterns"
