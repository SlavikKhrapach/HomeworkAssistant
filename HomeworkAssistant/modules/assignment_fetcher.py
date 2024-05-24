# assignment_fetcher.py
import requests
from datetime import datetime
import pytz

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