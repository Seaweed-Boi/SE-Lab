import pytest

from self_storage import access_allowed, payment_status, rent_due


@pytest.mark.parametrize(
    ("unit_size", "months", "is_climate", "is_member", "expected"),
    [
        ("small", 1, False, False, 0),
        ("small", 3, False, True, 80),
        ("medium", 4, True, False, 240),
        ("large", 10, False, False, 490),
        ("large", 10, True, True, 735),
    ],
)
def test_rent_due_branches(
    unit_size, months, is_climate, is_member, expected
):
    assert rent_due(unit_size, months, is_climate, is_member) == expected


def test_rent_due_rejects_unknown_unit_size():
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("extra-large", 1, False, False)


def test_rent_due_rejects_negative_months():
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -1, False, False)


@pytest.mark.parametrize(
    ("hour", "visitors", "is_owner", "expected"),
    [
        (12, 4, True, True),
        (12, 5, True, False),
        (6, 2, False, True),
        (22, 2, False, True),
        (12, 3, False, False),
        (5, 1, False, False),
        (23, 1, False, False),
    ],
)
def test_access_allowed_branches(hour, visitors, is_owner, expected):
    assert access_allowed(hour, visitors, is_owner) is expected


@pytest.mark.parametrize(
    ("days_to_due", "is_autopay", "has_prior_late", "expected"),
    [
        (0, True, False, "current"),
        (-1, True, False, "grace"),
        (-16, True, False, "lien"),
        (5, False, False, "current"),
        (-10, False, False, "grace"),
        (-11, False, False, "lien"),
        (15, False, True, "current"),
        (0, False, True, "grace"),
        (-1, False, True, "lien"),
    ],
)
def test_payment_status_branches(
    days_to_due, is_autopay, has_prior_late, expected
):
    assert payment_status(days_to_due, is_autopay, has_prior_late) == expected
