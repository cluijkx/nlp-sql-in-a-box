import pyodbc
import struct

from azure.identity import AzureCliCredential

driver_name = 'ODBC Driver 18 for SQL Server'
server_name = 'sql-NAHACKATHON-fluts'
database_name = 'sqldb-NAHACKATHON-fluts'

connection_string = f"Driver={driver_name};Server=tcp:{server_name}.database.windows.net,1433;Database={database_name}"


def pyodbc_attrs(access_token: str) -> dict:
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    token_bytes = bytes(access_token, 'utf-8')
    exp_token = b''
    for i in token_bytes:
        exp_token += bytes({i}) + bytes(1)
    return {SQL_COPT_SS_ACCESS_TOKEN: struct.pack("=i", len(exp_token)) + exp_token}


def get_records():
    credential = AzureCliCredential()
    access_token = credential.get_token('https://database.windows.net/.default').token
    conn = pyodbc.connect(connection_string, attrs_before=pyodbc_attrs(access_token))
    cursor = conn.cursor()
    query_string = "SELECT * FROM [dbo].[ExplorationProduction]"
    cursor.execute(query_string)
    return cursor.fetchall()


if __name__ == "__main__":
    records = get_records()
    for record in records:
        print(record)