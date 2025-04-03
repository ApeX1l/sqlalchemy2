from requests import get, delete, post

print(post('http://localhost:5000/api/v2/jobs', json={}).json())  # отправляется пустая форма json

print(post('http://localhost:5000/api/v2/jobs',  # пропущен один параметр - work_size
           json={'team_leader': 'example',
                 'job': 'example',
                 'collaborators': '0',
                 'start_date': 'now',
                 'end_date': 'never',
                 'is_finished': False}).json())

print(post('http://localhost:5000/api/v2/jobs',  # пропущено два параметра - work_size, end_date
           json={'team_leader': 'example',
                 'job': 'example',
                 'collaborators': '0',
                 'start_date': 'now',
                 'is_finished': False}).json())

print(post('http://localhost:5000/api/v2/jobs',  # успешное добавление работы в базу данных
           json={'team_leader': 'example',
                 'job': 'example',
                 'work_size': 0,
                 'collaborators': '0',
                 'start_date': 'now',
                 'end_date': 'never',
                 'is_finished': False}).json())

print(delete('http://localhost:5000/api/v2/jobs/medium').json())  # некорректный id работы
print(delete('http://localhost:5000/api/v2/jobs/3').json())  # нет работы с id 3
print(delete('http://localhost:5000/api/v2/jobs/7').json())

print(get('http://localhost:5000/api/v2/jobs/9999').json())  # некорректный id пользователя
print(get('http://localhost:5000/api/v2/jobs/last').json())  # некорректный id пользователя
print(get('http://localhost:5000/api/v2/jobs/5').json())
print(get('http://localhost:5000/api/v2/jobs').json())
# ---------------------------------------------------------------------------------------------
print(post('http://localhost:5000/api/v2/users',
           json={}).json())  # отправляется пустая форма json

print(post('http://localhost:5000/api/v2/users',
           json={'surname': 'test',  # пропущен параметр name
                 'age': '99',
                 'position': 'test',
                 'speciality': 'test',
                 'address': 'test',
                 'email': 'test@email.com',
                 'city_from': 'test',
                 'hashed_password': 'test'}).json())

print(post('http://localhost:5000/api/v2/users/9',
           json={'surname': 'test',  # указан неверный адрес
                 'age': '99',
                 'position': 'test',
                 'speciality': 'test',
                 'address': 'test',
                 'email': 'test@email.com',
                 'city_from': 'test',
                 'hashed_password': 'test'}).json())

print(post('http://localhost:5000/api/v2/users',
           json={'surname': 'test',  # успешное добавление пользователя в базу данных
                 'name': 'test',
                 'age': '99',
                 'position': 'test',
                 'speciality': 'test',
                 'address': 'test',
                 'email': 'test@email.com',
                 'city_from': 'test',
                 'hashed_password': 'test'}).json())

print(delete('http://localhost:5000/api/v2/users/second').json())  # некорректный id работы
print(delete('http://localhost:5000/api/v2/users/19').json())  # нет работы с id 19
print(delete('http://localhost:5000/api/v2/users/6').json())

print(get('http://localhost:5000/api/v2/users/100').json())  # некорректный id пользователя
print(get('http://localhost:5000/api/v2/users/first').json())  # некорректный id пользователя
print(get('http://localhost:5000/api/v2/users/5').json())
print(get('http://localhost:5000/api/v2/users').json())
