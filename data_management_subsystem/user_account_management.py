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
            count = count[0]
            count = list(count)
            count = count[0]
            if count == 0:
                return False
            elif count == 1:
                return True
            else:
                raise AssertionError("Expected user count to be 1 but got " + str(count))
