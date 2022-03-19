"""
Test the *_bestseller routines.

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import bestseller


@pytest.fixture
def mserv(request, bestseller_url, auth):
    return bestseller.BestSeller(bestseller_url, auth)


@pytest.fixture
def bestselling(request):
    return ('The Alchemist', '1000', '5')


def test_best_run(mserv, bestselling):
    trc, b_id = mserv.create_bestseller(bestselling[0], bestselling[1],
                                        bestselling[2])
    assert trc == 200
    assert isinstance(b_id, str)
    trc, title, copies, rating = mserv.read_bestseller(b_id)
    assert (trc == 200 and title == bestselling[0] and copies == bestselling[1]
            and rating == bestselling[2])
    mserv.delete_bestseller(b_id)
    # No status to check


@pytest.fixture
def bestseller_a(request):
    # Recorded 1967
    return ('Suspense', '2000')


@pytest.fixture
def m_id_oa(request, mserv, bestseller_a):
    trc, b_id = mserv.create(bestseller_a[0], bestseller_a[1])
    assert trc == 200
    yield b_id
    # Cleanup called after the test completes
    mserv.delete_bestseller(b_id)
