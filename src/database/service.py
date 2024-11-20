import logging

import pyodbc, struct

from azure.identity import DefaultAzureCredential

from faker import Faker

from .utils import table_exists, create_table, insert_record


logger = logging.getLogger(__name__)


class Database:

    def __init__(self, server_name: str, database_name: str, credential: DefaultAzureCredential) -> None:
        
        access_token = credential.get_token('https://database.windows.net/.default').token

        self.conn = get_connection(server_name=server_name, database_name=database_name, access_token=access_token)


    def setup(self) -> None:
        """
        Set up the database by creating the table and inserting fake records.
        """
        logger.debug("Setting up the database.")

        # create a cursor object to execute SQL queries
        cursor = self.conn.cursor()

        if table_exists(cursor):
            logger.debug("Table already exists.")
            # skip if table already exists
            return

        logger.debug("Creating table.")
        create_table(cursor)

        # Create Faker object
        fake = Faker()

        logger.debug("Generating and inserting records.")
        # Generate and insert 1,000 fake records
        for i in range(1000):
            insert_record(cursor, i, fake)

        # Commit the changes and close the connection
        self.conn.commit()

        logger.debug("Database setup completed.")


    def query(self, query: str) -> [pyodbc.Row]:
        """
        Query the database with the given SQL query.
        """
        cursor = self.conn.cursor()
        try:
            logger.debug("Querying database with: {}.".format(query))
            cursor.execute(query)
            result = cursor.fetchall()
            logger.debug("Successfully queried database: {}.".format(result))
        except Exception as ex:
            logger.error("Error querying database: {}.".format(ex))
            return "No Result Found"
        finally:
            cursor.close()

        return result


def pyodbc_attrs(access_token: str) -> dict:
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    token_bytes = bytes(access_token, 'utf-8')
    exp_token = b''
    for i in token_bytes:
        exp_token += bytes({i}) + bytes(1)
    return {SQL_COPT_SS_ACCESS_TOKEN: struct.pack("=i", len(exp_token)) + exp_token}


def get_connection(server_name: str, database_name: str, access_token: str):

    connection_string_template = 'DRIVER={driver_name};SERVER=tcp:{server_name}.database.windows.net,1433;DATABASE={database_name}'

    connection_string = connection_string_template.format(driver_name='ODBC Driver 18 for SQL Server', server_name=server_name, database_name=database_name)

    return pyodbc.connect(connection_string, attrs_before=pyodbc_attrs(access_token))