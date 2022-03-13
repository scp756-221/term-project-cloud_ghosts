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
import reader


@pytest.fixture
def mserv(request, reader_url, auth):
    return reader.Reader(reader_url, auth)


@pytest.fixture
def myreader(request):
    return ('jiacheng_wu@sfu.ca', 'Jason', 'Wu')


def test_simple_run(mserv, myreader):
    trc, m_id = mserv.create(myreader[0], myreader[1], myreader[2])
    assert trc == 200
    trc, email, fname, lname, libaccountno, membershipexp = mserv.read(m_id)
    # trc, email, fname, lname = mserv.read(m_id)
    assert (trc == 200 and email == myreader[0] and fname == myreader[1]
            and lname == myreader[2] and isinstance(libaccountno, str)
            and isinstance(membershipexp, str))
    mserv.delete(m_id)
    # No status to check


@pytest.fixture
def reader_a(request):
    return ('sleepysalamander@sfu.ca',
            'Sleepy',
            'Salamander',
            'ABCEDEFG14232156',
            '2022-05-01')


@pytest.fixture
def m_id_oa(request, mserv, reader_a):
    trc, m_id = mserv.create(reader_a[0],
                             reader_a[1],
                             reader_a[2],
                             reader_a[3],
                             reader_a[4])
    assert trc == 200
    yield m_id
    # Cleanup called after the test completes
    mserv.delete(m_id)


def test_full_cycle(mserv):
    # `mserv` is an instance of the `Reader` class

    reader_b = ('conflictedcrab@sfu.ca',
                'Conflicted',
                'Crab',
                '999ABCEDEFG14232156',
                '2022-06-01')
    trc, m_id = mserv.create(reader_b[0],
                             reader_b[1],
                             reader_b[2],
                             reader_b[3],
                             reader_b[4])
    assert trc == 200

    # test read by other dev
    trc, email, fname, lname, libaccountno, membershipexp = mserv.read(m_id)
    # trc, email, fname, lname = mserv.read(m_id)
    assert (trc == 200 and email == reader_b[0] and fname == reader_b[1]
            and lname == reader_b[2] and libaccountno == reader_b[3]
            and membershipexp == reader_b[4])

    # The last statement of the test
    mserv.delete(m_id)
