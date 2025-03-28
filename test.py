from requests import get, delete

print(delete('http://localhost:5000/api/jobs/999').json())
print(delete('http://localhost:5000/api/jobs/7').json())
print(get('http://localhost:5000/api/jobs').json())
