from flask import Flask, request, render_template
import requests
from datetime import datetime
import pytz
from groq import Groq

app = Flask(__name__)

def fetch_relevant_assignments(course_ids, access_token, buckets):
    headers = {'Authorization': f'Bearer {access_token}'}
    assignments = []
    pacific_tz = pytz.timezone('US/Pacific')

    for course_id in course_ids.split(','):
        for bucket in buckets:
            url = f'https://egator.greenriver.edu/api/v1/courses/{course_id.strip()}/assignments?bucket={bucket}'
            while url:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                assignments.extend(response.json())
                url = response.links.get('next', {}).get('url')

    # Convert due dates to local time and remove duplicates
    unique_assignments = {}
    for assignment in assignments:
        due_at = assignment.get('due_at')
        if due_at:
            utc_due_date = datetime.strptime(due_at, '%Y-%m-%dT%H:%M:%SZ')
            local_due_date = utc_due_date.replace(tzinfo=pytz.utc).astimezone(pacific_tz)
            assignment['due_at'] = local_due_date.strftime('%Y-%m-%d %I:%M %p')
        unique_assignments[assignment['id']] = assignment

    return list(unique_assignments.values())

def summarize_description(description, groq_api_key):
    client = Groq(api_key=groq_api_key)
    message_history = [{
        "role": "system",
        "content": """As an assignment summarizing machine, your task is to generate clear and concise summaries of assignments in HTML format. If the information is not provided in the assignment just return No Information Provided, and do nothing. That's normal, you don't have to explain anything. If there is information about an assignment, write the summary. These summaries will be integrated into a web page, so it's crucial to follow the provided guidelines for consistency and readability.

Instructions:

Summary: Provide a brief overview of the assignment's objectives and requirements. This should give readers a clear understanding of what the assignment entails.

Example: 
<h2>Assignment Summary</h2>
<p>Create a web application that allows users to track their daily fitness activities and analyze their progress over time.</p>

Steps: If the task in provided and clear, include this section in the summary. Outline the steps required to complete the assignment in a clear and sequential manner. Use an ordered list (<ol>) to present the steps. If the information is not provided, don't include and don't mention the steps.

Example if the tasks provided:

<h2>Steps:</h2>
<ol>
    <li>Design the user interface using HTML and CSS.</li>
    <li>Implement backend functionality using Python and Flask.</li>
    <li>Integrate a database to store user data.</li>
    <li>Test the application for functionality and usability.</li>
</ol>

Tools Needed: If the task in provided and clear, include this section in the summary. List any specific tools, software, or materials required to complete the assignment. This may include programming languages, development environments, or libraries. Use an unordered list (<ul>) to present the tools. If the information is not provided, don't include and don't mention the tools.

Example if the tasks provided:

<h2>Tools you will need:</h2>
<ul>
    <li>Text editor (e.g., Visual Studio Code, Sublime Text)</li>
    <li>Python programming language</li>
    <li>Flask framework</li>
    <li>SQLite database</li>
</ul>
Link Handling: If the assignment directions are provided in a link, include the link and indicate that the detailed instructions are available there. Do not invent assignment information if it is not provided. The links should open in a new tab, but don't mention it, do it seamlessly. This section does not need a header. If there are additional files provided, mention them and include the links to them.

Example: "See directions at Course Resources (kellerflint.github.io)"

Formatting Guidelines:

Avoid explicitly mentioning HTML formatting; focus on implementing it seamlessly.
Stick strictly to HTML without using Markdown or other markup languages.
Ensure all output is properly structured for integration into a web page.
If the assignment task is not provided, don't mention the steps and tools. Just output No Information Provided.
"""
    }, {"role": "user", "content": description}]

    chat_completion = client.chat.completions.create(
        messages=message_history,
        model="llama3-8b-8192"
    )

    return chat_completion.choices[0].message.content


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch_assignments', methods=['POST'])
def fetch_assignments():
    course_ids = request.form['course_ids']
    access_token = request.form['access_token']
    groq_api_key = request.form['groq_api_key']
    buckets = request.form.getlist('buckets')  # Get the list of selected buckets

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
