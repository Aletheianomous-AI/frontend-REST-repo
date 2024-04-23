from pytz import timezone
from ConnectionFailureException import ConnectionFailureException
from RecordNotFoundException import RecordNotFoundException
from NonExistentUserException import NonExistentUserException
from user_account_management import UserAccountManagement

import os
import time
import pyodbc
import pandas as pd


class ChatData():
    
    def upload_citations(self, response_chat_id, citations_list):
        """This function uploads citations related to this response_chat_id.

            PARAMETERS
            response_chat_id - The chat id that the citation(s) belongs to.
            citations_list - A list of citations to upload.
        """

        citation_url = ""


        for citation in citations_list:
            citation_url = citation
            citation_url = citation.replace("'", "''")
            cursor = self.conn.cursor()
            citation_list_append_qry = """
                DECLARE @CitationID int;
                IF EXISTS (SELECT * FROM dbo.Citation WHERE Link = ?)
                        BEGIN
                            SELECT @CitationID = Citation_ID
                            FROM dbo.Citation WHERE Link = ?;
                        END
                ELSE 
                        BEGIN
                            SELECT @CitationID = (MAX(Citation_ID) + 1)
                            FROM dbo.Citation;
                       
                            INSERT INTO dbo.Citation (Citation_ID, Link)
                            VALUES (@CitationID, ?);
                        END
            """
            cursor.execute(citation_list_append_qry, citation_url, citation_url, citation_url)

            del cursor

    def connect(self):
        self.con_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.db_name};UID={self.uname};PWD={self.passwrd}'
    
        connection_successful: bool = False
        con_attempts: int = 0
    
        
        while (connection_successful == False) and (con_attempts < 5):
            try:    
                self.conn = pyodbc.connect(self.con_str)
                
            except Exception as e:
                print(e)
                if con_attempts >=5:
                    raise ConnectionFailureException("Sorry, your message could not be sent.")
                else:
                    delay_time = [1,5,10,30,60]
                    time.sleep(delay_time[con_attempts])
            con_attempts+=1

    def close_conn(self):
        self.conn.close()
        self.conn = None
    
    def __init__(self, userId):
    
        self.server = os.environ.get('ALETHEIANOMOUS_AI_SERVER')
        self.db_name = os.environ.get('ALETHEIANOMOUS_AI_DB_NAME')
        self.uname = os.environ.get('ALETHEIANOMOUS_AI_UNAME')
        self.passwrd = os.environ.get('ALETHEIANOMOUS_AI_PASSWRD')
        self.conn = None
        self.connect()
    
        self.userId = userId
        if UserAccountManagement.user_exists(self.conn, userId):
            self.userId = userId
        else:
            raise NonExistentUserException(userId)

    def get_chat_by_cid(self, chat_id):
        """Returns the chat history by chat id.
        PARAMETER
        chat_id - The chat ID to return.
        """


        query = """
            SELECT *
            FROM dbo.Chat_History
            WHERE Chat_ID = ? 
            ORDER BY Chat_ID DESC
        """
        cursor = self.conn.cursor()
        cursor.execute(query, chat_id)
        row = cursor.fetchone()
        del cursor
        if row is not None:
            return row
        else:
            return RecordNotFoundException("No records with chat_id " + chat_id + " found in the database.")
        
            
    
        
    
    
    def log_chat(self, chat_data, timestamp, is_from_bot):
        """Uploads the chat data to the SQL database.
    
            PARAMETERS:
            chat_data - The chat to upload.
            timestamp - The data which the chat is generated.
            is_from_bot - If true, the chat is from the AI chatbot. 
            Otherwise, the chat is from the AI.
        """
       
        chat_data = chat_data.replace("'", "''")

        timestamp = timestamp.astimezone(timezone('America/New_York'))
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        if is_from_bot:
            is_from_bot_int: int = 1
        else:
            is_from_bot_int: int = 0

        # CREATE SQL QUERY THAT UPLOADS CHAT DATA.
        upload_query = ("""
            DECLARE @ChatID int;
    		SELECT @ChatID = (MAX(Chat_ID) + 1)
            FROM dbo.Chat_History;
            INSERT INTO dbo.Chat_History (Chat_ID, Chat_Content, Belongs_To_Bot, Time_Of_Output)
            VALUES (@ChatID, '""" + chat_data + """', """ + str(is_from_bot_int) + """, '""" + timestamp+ """');
            INSERT INTO dbo.Chat_User (Chat_ID, UserID) VALUES (@ChatID, """ + str(self.userId) + """);
        """
        )
        self.conn.autocommit = False
        cursor = self.conn.cursor()
        cursor.execute(upload_query)
        self.conn.commit()
        self.conn.autocommit = True
        del cursor

        cursor = self.conn.cursor()
        chat_id_qry = ("""
            SELECT MAX(Chat_ID) FROM dbo.Chat_History;
        """
        )
        cursor.execute(chat_id_qry)
        chat_id = cursor.fetchall()
        chat_id = chat_id[0][0]
        return chat_id
    
    def return_chat_history(self):

        fetching_query = """
            SELECT *
            FROM dbo.Chat_History AS ch
            INNER JOIN dbo.Chat_User AS cu
                ON (cu.Chat_ID = ch.Chat_ID)
            WHERE cu.UserId = """ + str(self.userId) + """
            ORDER BY cu.Chat_ID DESC
        """
        

        cursor = self.conn.cursor()
        cursor.execute(fetching_query)
        row = cursor.fetchone()
        chat_hist = [row]
        while row is not None:
            row = cursor.fetchone()
            chat_hist.append(row)
        return chat_hist
