import pytest

from src.backend.errors.user_facing_error import UserFacingError


def test_user_facing_error_is_exception() -> None:
    error = UserFacingError('test message')
    assert isinstance(error, Exception)
    assert str(error) == 'test message'


def test_user_facing_error_can_be_raised() -> None:
    with pytest.raises(UserFacingError):
        raise UserFacingError('something went wrong')


def test_user_facing_error_can_be_caught() -> None:
    try:
        raise UserFacingError('error')
    except UserFacingError as e:
        assert str(e) == 'error'
