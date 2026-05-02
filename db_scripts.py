import sqlite3

db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    open()
    do('DROP TABLE IF EXISTS quiz_content')
    do('DROP TABLE IF EXISTS question')
    do('DROP TABLE IF EXISTS quiz')
    close()

def create():
    open()

    do('''CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT)''')

    do('''CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT,
            answer1 TEXT,
            answer2 TEXT,
            answer3 TEXT,
            answer4 TEXT,
            correct_answer TEXT)''')

    do('''CREATE TABLE IF NOT EXISTS quiz_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER,
            question_id INTEGER,
            FOREIGN KEY (quiz_id) REFERENCES quiz(id),
            FOREIGN KEY (question_id) REFERENCES question(id))''')


    cursor.execute("SELECT id FROM quiz")
    if not cursor.fetchall():
        do("INSERT INTO quiz (name) VALUES ('Столицы')")

        do("INSERT INTO question (question_text, answer1, answer2, answer3, answer4, correct_answer) VALUES ('Столица России?', 'Москва', 'Питер', 'Казань', 'Сочи', 'Москва')")
        do("INSERT INTO question (question_text, answer1, answer2, answer3, answer4, correct_answer) VALUES ('Столица Франции?', 'Лондон', 'Берлин', 'Париж', 'Мадрид', 'Париж')")
        do("INSERT INTO question (question_text, answer1, answer2, answer3, answer4, correct_answer) VALUES ('Столица Японии?', 'Пекин', 'Сеул', 'Токио', 'Бангкок', 'Токио')")

        do("INSERT INTO quiz_content (quiz_id, question_id) VALUES (1,1), (1,2), (1,3)")
    conn.commit()
    close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    show_tables()

if __name__ == "__main__":
    main()