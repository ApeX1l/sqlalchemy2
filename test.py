from requests import post, get

print(post('http://localhost:5000/api/jobs', json={}).json())  # отправляется пустая форма json

print(post('http://localhost:5000/api/jobs',  # пропущен один параметр - work_size
           json={'team_leader': 'example',
                 'job': 'example',
                 'collaborators': '0',
                 'start_date': 'now',
                 'end_date': 'never',
                 'is_finished': False}).json())

print(post('http://localhost:5000/api/jobs',  # пропущено два параметра - work_size, end_date
           json={'team_leader': 'example',
                 'job': 'example',
                 'collaborators': '0',
                 'start_date': 'now',
                 'is_finished': False}).json())

print(post('http://localhost:5000/api/jobs',  # успешное добавление работы в базу данных
           json={'team_leader': 'example',
                 'job': 'example',
                 'work_size': 0,
                 'collaborators': '0',
                 'start_date': 'now',
                 'end_date': 'never',
                 'is_finished': False}).json())

print(get('http://localhost:5000/api/jobs').json())
