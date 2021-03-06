"""
Create the Book and reader tables

This is intended to be used within a continuous integration test.
As such, it presumes that it is creating the tables in a local
DynamoDB instance.

It may work with the full AWS DynamoDB service but it has
not been tested on that.
"""

# Standard libraries

# Installed packages
import boto3

# Local modules


# Function definitions
def create_tables(url, region, access_key_id, secret_access_key, book, reader,
                  bestseller):
    """ Create the book and reader tables in DynamoDB.

    Parameters
    ----------
    url: string
        The URL of the DynamoDB service.  This could be the actual AWS
        service or a local copy of DynamodDB. Local copies are typically
        at 'http://dynamodb-local:8000'.
    region: string
        The region to connect to. This is significant for the AWS
        service but could be any AWS region for a local copy.
        Example: 'us-west-2'.
    access_key_id: string
        The access key ID to authorize calls to DynamodDB.  Local
        DynamoDB copies will accept any value, while the actual AWS
        service requires a valid ID.
    secret_access_key: string
        The secret access key value associated with the key ID. Local
        DynamodDB copies will accept any value, while the actual AWS
        service requires the secret key associated with the key ID.
    music: string
        Name of the music table.
    reader: string
        Name of the reader table.
    """
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=url,
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key)
    """
    ProvisionedThroughput is meaningless for local DynamoDB instances but
    required by the API.

    These create_table() calls are asynchronous and so will run in parallel.
    """
    mt = dynamodb.create_table(
        TableName=book,
        AttributeDefinitions=[{
            "AttributeName": "book_id", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "book_id", "KeyType": "HASH"}],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    )
    ut = dynamodb.create_table(
        TableName=reader,
        AttributeDefinitions=[{
            "AttributeName": "reader_id", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "reader_id", "KeyType": "HASH"}],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    )
    bt = dynamodb.create_table(
        TableName=bestseller,
        AttributeDefinitions=[{
            "AttributeName": "bestseller_id", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "bestseller_id", "KeyType": "HASH"}],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    )
    """
    The order in which we wait for the tables is irrelevant.  We can only
    proceed after both exist.
    """
    mt.wait_until_exists()
    ut.wait_until_exists()
    bt.wait_until_exists()
