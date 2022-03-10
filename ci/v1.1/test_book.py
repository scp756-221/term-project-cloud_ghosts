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
def song(request):
    # Recorded 1956
    return ('Elvis Presley', 'Hound Dog')


def test_simple_run(mserv, song):
    # Original recording, 1952
    orig_artist = 'Big Mama Thornton'
    trc, m_id = mserv.create(song[0], song[1], orig_artist)
    assert trc == 200
    trc, artist, title, oa = mserv.read(m_id)
    assert (trc == 200 and artist == song[0] and title == song[1]
            and oa == orig_artist)
    mserv.delete(m_id)
    # No status to check


@pytest.fixture
def song_oa(request):
    # Recorded 1967
    return ('Aretha Franklin', 'Respect')


@pytest.fixture
def m_id_oa(request, mserv, song_oa):
    trc, m_id = mserv.create(song_oa[0], song_oa[1])
    assert trc == 200
    yield m_id
    # Cleanup called after the test completes
    mserv.delete(m_id)


def test_full_cycle(mserv):
    # `mserv` is an instance of the `Music` class

    # Performance at 2010 Vancouver Winter Olympics
    song = ('k. d. lang', 'Hallelujah')
    # Soundtrack of first Shrek film (2001)
    orig_artist = 'Rufus Wainwright'

    # Create a music record and save its id in the variable `m_id`
    # ... Fill in the test ...

    # function by other_dev to create the song with orig_artist
    trc, m_id = mserv.create(song[0], song[1], orig_artist)
    assert trc == 200

    # test read by other dev
    trc, artist, title, oa = mserv.read(m_id)
    assert (trc == 200 and artist == song[0] and title == song[1]
            and oa == orig_artist)

    # The last statement of the test
    mserv.delete(m_id)
