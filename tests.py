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
          'email': False})
put('http://localhost:5000/api/v2/users/11',
    json={'id': 2,
          'surname': 'Jackson',
          'name': 'Mikael',
          'age': 23,
          'position': 'capitan',
          'speciality': 'engineer',
          'address': 'street'})
