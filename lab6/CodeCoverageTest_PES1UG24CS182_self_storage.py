import pytest

from self_storage import access_allowed, payment_status, rent_due


def test_rent_due_within_deposit_months():
    assert rent_due("small", 1, False, False) == 0


def test_rent_due_rejects_unknown_unit_size():
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("extra-large", 1, False, False)


def test_rent_due_rejects_negative_months():
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -1, False, False)


def test_rent_due_calculates_standard_rate():
    assert rent_due("small", 3, False, True) == 80


def test_rent_due_calculates_climate_rate():
    assert rent_due("medium", 4, True, False) == 240


def test_rent_due_calculates_long_term_rate():
    assert rent_due("large", 10, False, False) == 490


def test_access_allowed_for_regular_visitor():
    assert access_allowed(12, 1, False) is True


def test_access_denied_for_too_many_visitors():
    assert access_allowed(12, 3, False) is False


def test_payment_status_returns_current():
    assert payment_status(5, False, False) == "current"


def test_payment_status_returns_grace():
    assert payment_status(-10, False, False) == "grace"


def test_payment_status_returns_lien():
    assert payment_status(-11, False, False) == "lien"
