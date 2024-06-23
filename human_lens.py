import requests
import json
import time
import os


def resolve_with_human_lens(api_key, task_data):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    base_url = "http://127.0.0.1:8000"
    
    url = base_url +'/task/create/'

    image_path = task_data.pop('image', None)

    files = {}
    task_id = None
    form_data = {
        'details': task_data['details'],
        'options': json.dumps(task_data['options'])
    }


    if image_path:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image_name = os.path.basename(image_path)

        files['image'] =  (image_name, image_data)
    

    response = requests.post(url, data=form_data, files=files, headers=headers)
    if response.status_code == 201:
        print('Task created successfully')
        task = response.json()
        task_id = task['id']
    else:
        print('Error creating task:', response.status_code, response.text)
        return None
    
    if task_id:
        return check_task_result(task_id, api_key)
    


def check_task_result(task_id, api_key):
    base_url = "http://127.0.0.1:8000"
    url = f'{base_url}/task/get_result/{task_id}/'  # Replace with your actual result checking API endpoint
    start_time = time.time()  # Get the start time

    headers = {
        'Authorization': f'Bearer {api_key}'
    }


    while time.time() - start_time < 60:
        response = requests.get(url, headers=headers)  # Make the GET request

        if response.status_code == 200:
            # Task completed successfully
            result = response.json()
            end_time = time.time()  # Get the end time
            elapsed_time = end_time - start_time  # Calculate elapsed time in seconds
            print(f'Task Completed: {result["tag"]}, Time Taken: {elapsed_time:.2f} seconds')
            return result["tag"], elapsed_time
            break
        elif response.status_code == 400:
            # Task not completed yet, retry after some time
            # print('Task not completed yet, retrying in 5 seconds...')
            time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            # Handle error
            print(f'Error checking task result: {response.status_code} - {response.text}')
            break
    
    return None