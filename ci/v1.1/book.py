"""
Python  API for the book service.
"""

# Standard library modules

# Installed packages
import requests


class Book():
    """Python API for the book service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the book service. Often
        'http://cmpt756s2:30001/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the book service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, author, title, genre=None):
        """Create an author, book pair.

        Parameters
        ----------
        author: string
            The author of the book.
        title: string
            The name of the book.
        genre: string or None
            The genre of the book.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Music.
            The string is the UUID of this song in the music database.
        """
        payload = {'Author': author,
                   'BookTitle': title}
        if genre is not None:
            payload['Genre'] = genre
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['book_id']

    def read(self, b_id):
        """Read an author, book pair.

        Parameters
        ----------
        b_id: string
            The UUID of this book in the library database.

        Returns
        -------
        status, author, title, genre

        status: number
            The HTTP status code returned by Music.
        author: If status is 200, the artist performing the song.
          If status is not 200, None.
        title: If status is 200, the title of the song.
          If status is not 200, None.
        genre: If status is 200 and the song has an
          original artist field, the artist's name.
          If the status is not 200 or there is no original artist
          field, None.
        """
        r = requests.get(
            self._url + b_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None, None

        item = r.json()['Items'][0]
        Genre = (item['Genre'] if 'Genre' in item
                 else None)
        return r.status_code, item['Author'], item['BookTitle'], Genre

    def delete(self, b_id):
        """Delete an author, book pair.

        Parameters
        ----------
        b_id: string
            The UUID of this book in the library database.

        Returns
        -------
        Does not return anything. The book delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + b_id,
            headers={'Authorization': self._auth}
        )
