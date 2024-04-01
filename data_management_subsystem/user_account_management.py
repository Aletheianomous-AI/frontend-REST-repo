import pyodbc

class UserAccountManagement():

        def user_exists(conn, userId):
            """Returns whether user exists in the database.
            
            PARAMETERS
            conn - The pyodbc connection object that is connected to SQL database
            userId - The userId to check if it exists.
            """
            query = """ SELECT COUNT(*)
            FROM dbo.Login
            WHERE UserID = '""" + str(userId) + """'
            """
            cursor = conn.cursor()
            cursor.execute(query)
            count = cursor.fetchall()
            print(count)
