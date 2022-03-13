"""
Python  API for the bestseller service.
"""

# Standard library modules

# Installed packages
import requests


class BestSeller():
    """Python API for the bestseller service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the bestseller service. Often
        'http://cmpt756s2:30001/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the bestseller service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create_bestseller(self, title, copies, rating=None):
        """Create an author, book pair.

        Parameters
        ----------
        title: string
            The name of the book.
        copies: number
            The number of copies sold.
        rating: string or None
            The rating of the book.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by BestSeller.
            The string is the UUID of this book in the bestseller database.
        """
        payload = {'Title': title,
                   'Copies': copies}
        if rating is not None:
            payload['Rating'] = rating
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['book_id']

    def read_bestseller(self, b_id):
        """Read copies sold, rating of the book.

        Parameters
        ----------
        b_id: string
            The UUID of the book in the library database.

        Returns
        -------
        status, title, copies, rating

        status: number
            The HTTP status code returned by Music.
        title: If status is 200, the title of the song.
          If status is not 200, None.
        copies: If status is 200, the copies sold of the book.
          If status is not 200, None.
        rating: If status is 200 and the book has ratings
          If the status is not 200 or there is no rating, None.
        """
        r = requests.get(
            self._url + b_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None, None

        item = r.json()['Items'][0]
        Rating = (item['Rating'] if 'Rating' in item
                  else None)
        return r.status_code, item['Title'], item['Copies'], Rating

    def delete_bestseller(self, b_id):
        """Delete copies sold, rating of the book.

        Parameters
        ----------
        b_id: string
            The UUID of this book in the library database.

        Returns
        -------
        Does not return anything. The bestseller delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + b_id,
            headers={'Authorization': self._auth}
        )
