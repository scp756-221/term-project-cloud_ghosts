"""
Test the *_original_artist routines.

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import book


@pytest.fixture
def mserv(request, book_url, auth):
    return book.Book(book_url, auth)


@pytest.fixture
def novel(request):
    return ('George Orwell', '1984')


def test_simple_run(mserv, novel):
    genre = 'Fiction'
    trc, m_id = mserv.create(novel[0], novel[1], genre)
    assert trc == 200
    trc, author, title, gr = mserv.read(m_id)
    assert (trc == 200 and author == novel[0] and title == novel[1]
            and gr == genre)
    mserv.delete(m_id)
    # No status to check


@pytest.fixture
def novel_oa(request):
    return ('George Orwell', 'Animal Farm')


@pytest.fixture
def m_id_oa(request, mserv, novel_oa):
    trc, m_id = mserv.create(novel_oa[0], novel_oa[1])
    assert trc == 200
    yield m_id
    # Cleanup called after the test completes
    mserv.delete(m_id)


def test_full_cycle(mserv):
    # `mserv` is an instance of the `Music` class

    novel = ('F. Scott Fitzgerald', 'The Great Gatsby')
    genre = 'Tragedy'

    trc, m_id = mserv.create(novel[0], novel[1], genre)
    assert trc == 200

    trc, author, title, gr = mserv.read(m_id)
    assert (trc == 200 and author == novel[0] and title == novel[1]
            and gr == genre)

    # The last statement of the test
    mserv.delete(m_id)
