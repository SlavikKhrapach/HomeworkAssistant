from flask import Flask, request, render_template
import requests

from modules.assignment_fetcher import fetch_relevant_assignments
from modules.description_summarizer import summarize_description

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch_assignments', methods=['POST'])
def fetch_assignments():
    course_ids = request.form['course_ids']
    access_token = request.form['access_token']
    groq_api_key = request.form['groq_api_key']
    buckets = request.form.getlist('buckets')  # Get the list of selected buckets
    print("Bucket:" + str(buckets))

    # If buckets list is empty, add "upcoming" to it
    if not buckets:
        buckets.append('upcoming')

    assignments = fetch_relevant_assignments(course_ids, access_token, buckets)
    return render_template('assignments.html', assignments=assignments, groq_api_key=groq_api_key, enumerate=enumerate, buckets=buckets)


@app.route('/assignment/<int:assignment_id>', methods=['GET'])
def assignment_detail(assignment_id):
    course_ids = request.args.get('course_ids')
    access_token = request.args.get('access_token')
    groq_api_key = request.args.get('groq_api_key')
    print("groq_api_key:" + groq_api_key)
    buckets = request.args.getlist('buckets')

    assignments = fetch_relevant_assignments(course_ids, access_token, buckets)
    assignment = next((a for a in assignments if a['id'] == assignment_id), None)

    if assignment:
        summary = summarize_description(assignment['description'], groq_api_key)
        return render_template('assignment_detail.html', assignment=assignment, summary=summary, course_ids=course_ids,
                               access_token=access_token, groq_api_key=groq_api_key, buckets=','.join(buckets))
    else:
        return "Assignment not found", 404


if __name__ == '__main__':
    app.run(debug=True)