from flask import Flask, render_template, request, redirect, session
from utils.loader import load_questions
import config
import logging
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')  # 🔐 Use env var in production
app.debug = True

logging.basicConfig(level=logging.DEBUG)

# 🔹 Helper: Get all available question sets from /data
def get_available_sets():
    data_dir = "data"
    sets = [
        os.path.join(data_dir, file)
        for file in os.listdir(data_dir)
        if file.endswith(".json") and file.startswith("set")
    ]
    sets.sort(key=lambda f: int(''.join(filter(str.isdigit, os.path.basename(f))))
              if any(char.isdigit() for char in os.path.basename(f)) else 0)
    return sets

# 🔹 Jinja filter: Show just the filename
@app.template_filter('basename')
def basename_filter(path):
    return os.path.basename(path)

# 🔹 Home page: Show available sets
@app.route('/')
def index():
    available_sets = get_available_sets()
    return render_template('index.html', available_sets=available_sets)

# 🔹 Start quiz
@app.route('/start', methods=['POST'])
def start_quiz():
    set_name = request.form.get('set_name') or config.DEFAULT_QUESTION_SET
    session.clear()
    questions = load_questions(set_name)
    logging.debug(f"Loaded {len(questions)} questions from set '{set_name}'")

    if not questions:
        return "<h2>Error: No questions found for this set.</h2>"

    app.config['QUESTION_CACHE'] = questions
    session['index'] = 0
    session['score'] = 0
    session['answers'] = []
    return redirect('/quiz')

# 🔹 Quiz flow
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = app.config.get('QUESTION_CACHE', [])
    index = session.get('index', 0)

    if not questions:
        return redirect('/')

    if index >= len(questions):
        return redirect('/review')

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'next':
            session.pop('temp_feedback', None)
            session['index'] = index + 1
            return redirect('/quiz')

        selected = request.form.getlist('selected_options')
        if not selected:
            session['temp_feedback'] = {'error': 'No answer selected.'}
            return redirect('/quiz')

        question = questions[index]
        correct_list = [c.strip() for c in question.get('correct', '').split(',')]
        explanation = question.get('explanation', '')
        is_correct = set(selected) == set(correct_list)

        feedback = {
            'selected': selected,
            'correct': correct_list,
            'is_correct': is_correct,
            'explanation': explanation
        }

        if is_correct:
            session['score'] += 1

        session['answers'].append(selected)
        session['temp_feedback'] = feedback
        return redirect('/quiz')

    feedback = session.get('temp_feedback')
    question = questions[index]

    return render_template('quiz.html',
                           question=question,
                           feedback=feedback,
                           current_index=index,
                           total_questions=len(questions))

# 🔹 Review screen
@app.route('/review')
def review():
    questions = app.config.get('QUESTION_CACHE', [])
    answers = session.get('answers', [])
    score = session.get('score', 0)

    if not questions:
        return redirect('/')

    review_data = []
    incorrect = []

    for i, q in enumerate(questions):
        user_answer = answers[i] if i < len(answers) else []
        correct_answer = [c.strip() for c in q.get('correct', '').split(',')]
        is_correct = set(user_answer) == set(correct_answer)

        review_data.append({
            'id': q['id'],
            'question': q['question'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'explanation': q.get('explanation', '')
        })

        if not is_correct:
            incorrect.append(q)

    total = len(questions)
    percentage = (score / total) * 100 if total > 0 else 0
    status = "Pass" if percentage >= 70 else "Fail"

    # 🔁 Store incorrect questions for retry
    session['retry_questions'] = incorrect
    session['retry_index'] = 0
    session['retry_score'] = 0
    session['retry_answers'] = []

    return render_template('review.html',
                           review_data=review_data,
                           score=score,
                           total=total,
                           percentage=round(percentage, 2),
                           status=status)

# 🔁 Retry incorrect questions
@app.route('/retry')
def retry():
    retry_questions = session.get('retry_questions', [])
    if not retry_questions:
        return redirect('/')

    app.config['QUESTION_CACHE'] = retry_questions
    session['index'] = 0
    session['score'] = 0
    session['answers'] = []
    return redirect('/quiz')

# 🔄 Restart entire quiz
@app.route('/restart')
def restart():
    session.clear()
    return redirect('/')

# 🧹 Clear session manually
@app.route('/clear-session')
def clear_session():
    try:
        session.clear()
        return """
            <h2>✅ Session cleared successfully.</h2>
            <p>You can now restart the quiz.</p>
            <a href="/">Go to Home</a>
        """
    except Exception as e:
        return f"<h2>Error clearing session</h2><pre>{e}</pre>", 500

# ⚠️ Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    logging.exception("Unhandled exception:")
    return f"<h1>Internal Server Error</h1><pre>{e}</pre>", 500

if __name__ == '__main__':
    app.run(debug=True)
