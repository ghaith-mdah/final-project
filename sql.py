import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table Actions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Actions (
        idActions INTEGER PRIMARY KEY AUTOINCREMENT,
        idProgress INTEGER,
        ProgressName TEXT,
        Image BLOB,
        LW TEXT,
        Feedback TEXT
    )
''')

# Create table Progress
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Progress (
        idProgress INTEGER PRIMARY KEY AUTOINCREMENT,
        UserId INTEGER,
        ProgressName TEXT,
        Language TEXT,
        Level TEXT,
        LorW TEXT,
        Counter INTEGER DEFAULT 0
    )
''')

# Create table Themes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Themes (
        Theme TINYINT PRIMARY KEY
    )
''')
cursor.execute('''
    INSERT INTO Themes (Theme)
    SELECT '0'
    WHERE NOT EXISTS (SELECT 1 FROM Themes);
''')

# Create table Users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        idUsers INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT,
        Password TEXT,
        Mail TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Quiz (
        quizid INTEGER PRIMARY KEY AUTOINCREMENT,
        progressid INTEGER,
        level TEXT,
        GroupNum INTEGER,
        Grade INTEGER DEFAULT -1,
        Date DATE DEFAULT '2000-01-01' 
    )
''')
               

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ActionInQuiz (
        idAction INTEGER PRIMARY KEY AUTOINCREMENT,
        quizid INTEGER,
        progressid INTEGER,
        Image BLOB,
        LW TEXT,
        FeedBack TEXT 
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
