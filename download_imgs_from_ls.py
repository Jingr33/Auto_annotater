"""Script for downloading images from LabelStudio projects."""

import base64
import os

import requests

API_KEY = ''  # your API Key
PROJECT_ID = ''  # id (from URL) of your LabelStudio project
BASE_URL = ''  # LAbelStudio API endpoint for download

headers = {'Authorization': f'Token {API_KEY}'}  # API header
API_URL = f'{BASE_URL}/api/projects/{PROJECT_ID}/tasks?completed=false'  # API url address

PAGE = 1
all_tasks = []
while True:  # while loop due to paging
    # download images from LabelStudio
    response = requests.get(API_URL, headers=headers, params={'page': PAGE}, timeout=10)
    tasks = response.json()

    # break if there are no other images
    if response.status_code != 200:
        break

    # select only unannotated tasks
    unannotated_tasks = [task for task in tasks if not task.get('annotations')]
    all_tasks.extend(unannotated_tasks)
    PAGE += 1

print('Staženo!')
print(f'Počet neoanotovaných obrázků {len(all_tasks)}')

# save each task as jpg file
for task in all_tasks:
    image_data = task['data']['image'].split(',')[-1]
    image_bytes = base64.b64decode(image_data)

    with open(os.path.join('for_annotation', f'{task["id"]}.jpg'), 'wb') as f:
        f.write(image_bytes)

print('Uloženo!')
