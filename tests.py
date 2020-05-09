from requests import get, delete, put

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(get('http://localhost:5000/api/v2/users/999').json())
print(get('http://localhost:5000/api/v2/users/q').json())

print(delete('http://localhost:5000/api/v2/users/3').json())
print(delete('http://localhost:5000/api/v2/users/100').json())

put('http://localhost:5000/api/v2/users/11',
    json={'id': 2,
          'surname': 'Jackson',
          'name': 'Mikael',
          'age': 23,
          'position': 'capitan',
          'speciality': 'engineer',
          'address': 'street',
          'email': 'hello@mail.ru'})
put('http://localhost:5000//api/v2/users/3',
    json={'id': 2,
          'surname': 'Jackson',
          'name': 'Mikael',
          'age': 23,
          'position': 'capitan',
          'speciality': 'engineer',
          'address': 'street',
          'email': 'hello@mail.ru'})
put('http://localhost:5000/api/v2/users/11',
    json={'id': 2,
          'surname': 'Jackson',
          'name': 'Mikael',
          'age': 23,
          'position': 'capitan',
          'speciality': 'engineer',
          'address': 'street'})

print(get('http://localhost:5000/api/v2/jobs').json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs/999').json())
print(get('http://localhost:5000/api/v2/jobs/q').json())

print(delete('http://localhost:5000/api/v2/jobs/3').json())
print(delete('http://localhost:5000/api/v2/jobs/100').json())

put('http://localhost:5000/api/v2/jobs/11',
    json={'id': 2,
          'team_leader': 4,
          'job': 'work',
          'work_size': 23,
          'collaborators': '[1, 2, 3]',
          'start_date': '2020-03-24 17:19',
          'end_date': '2020-03-23 17:30',
          'is_finished': False})
put('http://localhost:5000//api/v2/jobs/3',
    json={'id': 2,
          'team_leader': 4,
          'job': 'work',
          'work_size': 23,
          'collaborators': '[1, 2, 3]',
          'start_date': '2020-03-24 17:19',
          'end_date': '2020-03-23 17:30',
          'is_finished': False})
put('http://localhost:5000/api/v2/jobs/11',
    json={'id': 2,
          'team_leader': 4,
          'job': 'work',
          'work_size': 23,
          'collaborators': '[1, 2, 3]',
          'start_date': '2020-03-24 17:19',
          'end_date': '2020-03-23 17:30'})
