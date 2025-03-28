from requests import put, get, post

print(post('http://localhost:5000/api/jobs',  # успешное добавление работы в базу данных
           json={'team_leader': 'example',
                 'job': 'example',
                 'work_size': 0,
                 'collaborators': '0',
                 'start_date': 'now',
                 'end_date': 'never',
                 'is_finished': False}).json())
print(get('http://localhost:5000/api/jobs').json())

print(put('http://localhost:5000/api/jobs/7',
          json={'team_leader': 'example_put',
                'job': 'example_put',
                'work_size': 10,
                'collaborators': 0,
                'start_date': 'never',
                'end_date': 'never',
                'is_finished': False}).json())
print(get('http://localhost:5000/api/jobs').json())
