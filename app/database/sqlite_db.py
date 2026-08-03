import sqlite3
from app.config import settings



def sqlite_procedure(story,testcase_details):
    conn, cursor = create_connection()
    create_tables(cursor)
    insert_data(cursor,story,testcase_details)
    conn.commit()
    conn.close()
    #print("Data inserted successfully")

def create_connection():
    conn = sqlite3.connect('AiQA_DB.db')
    cursor = conn.cursor()
    #print("Connected to SQLite database")
    return conn,cursor

def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS story (
                    story_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    model_used TEXT NOT NULL,
                    status TEXT
                )''')
    #print("Table 'story' created successfully")
    cursor.execute('''CREATE TABLE IF NOT EXISTS testcase (
                    testcase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_id INTEGER,
                    title TEXT NOT NULL,
                    preconditions TEXT,
                    test_steps TEXT,
                    expected_result TEXT,
                    priority TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES story(story_id)
                 )''')

def insert_data(cursor, story,testcase_details):
    status = "Failed"
    if testcase_details:
        status="Success"
    story_id=insert_story(cursor,story, settings.AI_PROVIDER,status)
    for data in testcase_details:
        inser_testcase(cursor,story_id, data['title'], data['preconditions'], data['test_steps'], data['expected_result'], data['priority'])
    
 
def insert_story(cursor, story, model,success):
    cursor.execute(''' INSERT INTO story(
    title, model_used, status)
    VALUES (?,?,?)
    ''',(story,model,success))

    return cursor.lastrowid #

def inser_testcase(cursor,story_id, title, preconditions, test_steps, expected_result, priority):
    cursor.execute(''' INSERT INTO testcase(story_id, title, preconditions, test_steps, expected_result, priority)
                    VALUES(?,?,?,?,?,?)
                    ''',(story_id, title, preconditions, test_steps, expected_result, priority))
