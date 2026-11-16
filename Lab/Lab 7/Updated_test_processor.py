import pytest
from hypothesis import given, strategies as st

from processor import calculate_total, normalize_text, parse_int_list


@given(st.text())
def test_normalize_text_handles_valid_strings(value):
    if not value.strip():
        with pytest.raises(ValueError):
            normalize_text(value)
    else:
        result = normalize_text(value)
        assert isinstance(result, str)
        assert result == " ".join(value.split())


@given(st.one_of(st.none(), st.integers(), st.booleans(), st.lists(st.text())))
def test_normalize_text_rejects_non_strings(value):
    with pytest.raises(TypeError):
        normalize_text(value)


@given(
    st.one_of(
        st.integers(),
        st.text(),
        st.lists(
            st.one_of(
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.text(),
                st.booleans(),
                st.none(),
            )
        ),
        st.tuples(st.integers(), st.text()),
    )
)
def test_parse_int_list_is_safe(value):
    try:
        result = parse_int_list(value)
    except (TypeError, ValueError):
        pass
    else:
        assert isinstance(result, list)
        assert all(isinstance(item, int) for item in result)


@given(st.sampled_from([float("nan"), float("inf"), float("-inf")]))
def test_parse_int_list_rejects_non_finite_floats(value):
    with pytest.raises(ValueError):
        parse_int_list([value])


@given(
    st.lists(
        st.one_of(
            st.integers(min_value=0, max_value=1000),
            st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False),
        ),
        min_size=0,
        max_size=10,
    ),
    st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
)
def test_calculate_total_works_for_valid_inputs(prices, tax_rate):
    result = calculate_total(prices, tax_rate)
    assert isinstance(result, float)
    assert result >= 0


@given(st.sampled_from([float("nan"), float("inf"), float("-inf")]))
def test_calculate_total_rejects_non_finite_tax_rates(value):
    with pytest.raises(ValueError):
        calculate_total([10], value)


@given(st.sampled_from([float("nan"), float("inf"), float("-inf")]))
def test_calculate_total_rejects_non_finite_prices(value):
    with pytest.raises(ValueError):
        calculate_total([value], 0.1)


def test_calculate_total_rejects_overflowing_totals():
    with pytest.raises(ValueError):
        calculate_total([1e308, 1e308], 0)


@given(st.one_of(st.none(), st.text(), st.integers(), st.booleans()))
def test_calculate_total_rejects_invalid_prices_argument(value):
    with pytest.raises(TypeError):
        calculate_total(value, 0.1)


@given(st.one_of(st.none(), st.text(), st.booleans()))
def test_calculate_total_rejects_invalid_tax_type(value):
    with pytest.raises(TypeError):
        calculate_total([10, 20], value)


@given(st.floats(min_value=-5, max_value=5, allow_nan=False, allow_infinity=False))
def test_calculate_total_rejects_out_of_range_tax_rate(value):
    if value < 0 or value > 1:
        with pytest.raises(ValueError):
            calculate_total([10, 20], value)


@given(st.floats(max_value=-1e-10, allow_nan=False, allow_infinity=False))
def test_calculate_total_rejects_negative_prices(value):
    with pytest.raises(ValueError):
        calculate_total([value], 0.1)
