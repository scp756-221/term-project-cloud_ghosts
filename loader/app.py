"""
SFU CMPT 756
Loader for sample database
"""

# Standard library modules
import csv
import os
import time

# Installed packages
import requests

# The application

loader_token = os.getenv('SVC_LOADER_TOKEN')

# Enough time for Envoy proxy to initialize
# This is only needed if the loader is run with
# Istio injection.  `cluster/loader-tpl.yaml`
# sets that value.
INITIAL_WAIT_SEC = 1

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
}


def build_auth():
    """Return a loader Authorization header in Basic format"""
    global loader_token
    return requests.auth.HTTPBasicAuth('svc-loader', loader_token)

def create_book(author, genre, title, uuid):
    """
    Create a book.
    If a record already exists with the same fname, lname, and email,
    the old UUID is replaced with this one.
    """
    url = db['name'] + '/load'
    response = requests.post(
        url,
        auth=build_auth(),
        json={"objtype": "book",
              "Author": author,
              "BookTitle": title,
              "Genre": genre,
              "uuid": uuid})
    return (response.json())

def create_reader(email, fname, lname, libaccountno, membershipexp, uuid):
    """
    Create a reader.
    If a record already exists with the same fname, lname, and email,
    the old UUID is replaced with this one.
    """
    url = db['name'] + '/load'
    response = requests.post(
        url,
        auth=build_auth(),
        json={"objtype": "reader",
              "lname": lname,
              "email": email,
              "fname": fname,
              "libaccountno": libaccountno,
              "membershipexp": membershipexp,
              "uuid": uuid})
    return (response.json())


def create_bestseller(title, copies, rating, uuid):
    """
    Create a best seller.
    If a record already exists with the same artist and title,
    the old UUID is replaced with this one.
    """
    url = db['name'] + '/load'
    response = requests.post(
        url,
        auth=build_auth(),
        json={"objtype": "bestseller",
              "Title": title,
              "Copies": copies,
              "Rating": rating,
              "uuid": uuid})
    return (response.json())


def check_resp(resp, key):
    if 'http_status_code' in resp:
        return None
    else:
        return resp[key]


if __name__ == '__main__':
    # Give Istio proxy time to initialize
    time.sleep(INITIAL_WAIT_SEC)

    resource_dir = '/data'

    with open('{}/book/book.csv'.format(resource_dir), 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for fn, ln, email, uuid in rdr:
            resp = create_book(fn.strip(),
                               ln.strip(),
                               email.strip(),
                               uuid.strip())
            resp = check_resp(resp, 'book_id')
            if resp is None or resp != uuid:
                print('Error creating book {} {} ({}), {}'.format(fn,
                                                                  ln,
                                                                  email,
                                                                  uuid))

    with open('{}/reader/reader.csv'.format(resource_dir), 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for email, fname, lname, libaccountno, membershipexp, uuid in rdr:
            resp = create_reader(email.strip(),
                               fname.strip(),
                               lname.strip(),
                               libaccountno.strip(),
                               membershipexp.strip(),
                               uuid.strip())
            resp = check_resp(resp, 'reader_id')
            if resp is None or resp != uuid:
                print('Error creating reader {} {} ({}), {}'.format(email,
                                                                    fname,
                                                                    lname,
                                                                    uuid))
                                                                  
    with open('{}/bestseller/bestseller.csv'.format(resource_dir), 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for title, copies, rating, uuid in rdr:
            resp = create_bestseller(title.strip(),
                               copies.strip(),
                               rating.strip(),
                               uuid.strip())
            resp = check_resp(resp, 'bestseller_id')
            if resp is None or resp != uuid:
                print('Error creating best seller {} {}, {} {}'.format(title,
                                                                       copies,
                                                                       title,
                                                                       uuid))
