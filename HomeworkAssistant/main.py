from flask import Flask, request, session, redirect, url_for, render_template
from modules.assignment_fetcher import fetch_relevant_assignments
from modules.description_summarizer import summarize_description

app = Flask(__name__)
app.secret_key = '0897TG789T*()&t7fOG*Y()_t'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_assignments', methods=['POST'])
def fetch_assignments():
    if not session['course_ids']:
        course_ids = request.form['course_ids']
    else:
        course_ids = session['course_ids']

    if not session['access_token']:
        access_token = request.form['access_token']
    else:
        access_token = session['access_token']

    if not session['groq_api_key']:
        groq_api_key = request.form['groq_api_key']
    else:
        groq_api_key = session['groq_api_key']


    buckets = request.form.getlist('buckets')  # Get the list of selected buckets


    # If buckets list is empty, add "upcoming" to it
    if not buckets:
        buckets.append('upcoming')

    session['course_ids'] = course_ids
    session['access_token'] = access_token
    session['groq_api_key'] = groq_api_key
    session['buckets'] = buckets

    assignments = fetch_relevant_assignments()
    return render_template('assignments.html', assignments=assignments, groq_api_key=groq_api_key, enumerate=enumerate, buckets=buckets)


@app.route('/assignment/<int:assignment_id>', methods=['GET'])
def assignment_detail(assignment_id):
    course_ids = session.get('course_ids')
    access_token = session.get('access_token')
    groq_api_key = session.get('groq_api_key')
    buckets = session.get('buckets')

    if not course_ids or not access_token:
        return redirect(url_for('index'))

    assignments = fetch_relevant_assignments()
    assignment = next((a for a in assignments if a['id'] == assignment_id), None)

    if assignment:
        summary = summarize_description(assignment['description'], groq_api_key)
        return render_template('assignment_detail.html', assignment=assignment, summary=summary, course_ids=course_ids,
                                   access_token=access_token, groq_api_key=groq_api_key, buckets=','.join(buckets))
    else:
        return "Assignment not found", 404


if __name__ == '__main__':
    app.run(debug=True)