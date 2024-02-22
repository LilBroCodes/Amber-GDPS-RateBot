import requests


def generate_sql_query(word):
    """
    Generate an SQL query string to search for rows where the "name" column is similar to the given word.

    Args:
    word (str): The word to search for similarity in the "name" column.

    Returns:
    str: The SQL query string.
    """
    # Construct the SQL query string
    query = f"""SELECT * FROM songs WHERE name LIKE '%{word}%' AND name REGEXP '{'[{}]'.join(word)}{{0,5}}'"""
    return query


def execute_query(session: requests.Session, query, login, password, url="https://amber.ps.fhgdps.com/sqlQuery.php"):
    """
    Execute a SQL query on a server using provided login credentials.

    Args:
    url (str): The URL of the PHP script.
    query (str): The SQL query to execute.
    login (str): The username for login authentication.
    password (str): The password for login authentication.

    Returns:
    dict: The result of the SQL query or an error message.
    """
    # Parameters to send in the POST request
    data = {
        'Query': query,
        'Login': login,
        'Pass': password
    }

    try:
        # Sending POST request to the PHP script
        response = session.post(url, data=data)

        # Checking if request was successful
        if response.status_code == 200:
            # Parsing response JSON
            result = response.json()
            if 'error' in result:
                return {"error": result['error']}
            else:
                return {"result": result}
        else:
            with open(f"error.html", "wb") as efile:
                efile.write(response.content)
            return {"error": "Failed to connect to the server"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
