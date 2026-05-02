from flask import Flask, render_template, request, session, redirect, url_for
import os
from random import shuffle
import db_scripts

app = Flask(__name__, template_folder=os.getcwd(), static_folder=os.getcwd())
app.secret_key = 'super_secret_key'

def get_questions_for_quiz(quiz_id):
    db_scripts.open()
    db_scripts.cursor.execute(
        "SELECT question_id FROM quiz_content WHERE quiz_id = ?", (quiz_id,))
    ids = [row[0] for row in db_scripts.cursor.fetchall()]
    db_scripts.close()
    return ids

def check_answer(q_id, user_answer):
    db_scripts.open()
    db_scripts.cursor.execute(
        "SELECT correct_answer FROM question WHERE id = ?", (q_id,))
    correct = db_scripts.cursor.fetchone()[0]
    db_scripts.close()
    return correct == user_answer

def question_form(q_id):
    db_scripts.open()
    db_scripts.cursor.execute(
        "SELECT question_text, answer1, answer2, answer3, answer4 FROM question WHERE id = ?", (q_id,))
    row = db_scripts.cursor.fetchone()
    db_scripts.close()
    text = row[0]
    answers = list(row[1:])
    shuffle(answers)
    return render_template('test.html', q_id=q_id, question_text=text, answers=answers)

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        if quiz_id:
            quiz_id = int(quiz_id)
            questions = get_questions_for_quiz(quiz_id)
            if not questions:
                return "В викторине нет вопросов"
            session['quiz_id'] = quiz_id
            session['questions'] = questions
            session['current_index'] = 0
            session['total'] = 0
            session['answers'] = 0
            return redirect(url_for('test'))
    return render_template('start.html')

@app.route('/test')
def test():
    if 'questions' not in session or 'current_index' not in session:
        return redirect(url_for('start'))
    idx = session['current_index']
    questions = session['questions']
    if idx >= len(questions):
        return redirect(url_for('result'))
    q_id = questions[idx]
    return question_form(q_id)

@app.route('/save_answer', methods=['POST'])
def save_answers():
    if 'questions' not in session:
        return redirect(url_for('start'))
    user_ans = request.form.get('ans_text')
    q_id = int(request.form.get('q_id'))
    is_correct = check_answer(q_id, user_ans)
    session['total'] = session.get('total', 0) + 1
    if is_correct:
        session['answers'] = session.get('answers', 0) + 1
    session['current_index'] += 1
    return redirect(url_for('test'))

@app.route('/result')
def result():
    total = session.get('total', 0)
    correct = session.get('answers', 0)
    return render_template('result.html', total=total, correct=correct)

if __name__ == '__main__':
    app.run(host=("0.0.0.0"))