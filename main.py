import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

token = os.environ['GIT_TOKEN']
user = os.environ['GIT_USER']

base_endpoint = 'https://gitlab.com/'
user_info_endpoint = base_endpoint + 'api/v4/users?username=' + user

headers = {'Authorization': 'Bearer ' + token}

def retrieve_user_id():
    x = requests.get(user_info_endpoint, headers=headers).json()
    return x[0]['id']

mr_endpoint = base_endpoint + 'api/v4/merge_requests?state=opened&scope=all&approver_ids[]=' + str(retrieve_user_id())

jsonResponse = requests.get(mr_endpoint, headers=headers).json()

for event in jsonResponse:
    print()
    print('Project: ' + event['references']['full'].split('!')[0])
    print('URL: ' + event['web_url'])
    print('Title: ' + event['title'])
    date_time_obj = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
    today = datetime.now(timezone.utc)
    print('Created at: ' + str((today - date_time_obj).days) + ' day(s) ago')
    print('From/To branch: ' + event['source_branch'] + ' --> ' + event['target_branch'])
    print('Author: ' + event['references']['full'].split('!')[0])
    print('Conflicts: ' + str(event['has_conflicts']))
    print('Opened Discussions: ' + str(not event['blocking_discussions_resolved']))