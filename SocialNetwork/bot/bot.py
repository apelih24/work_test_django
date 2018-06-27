import json
import requests
from requests.auth import HTTPBasicAuth
from random import randint


data = {
    'users': 0,
    'posts': 0,
    'likes': 0
}
emails = (
    'valera@gmail.com',
    'vanya@gmail.com',
    'alex@gmail.com',
    'apelih24@gmail.com',
    'dima@gmail.com'
)
headers = {'content-type': 'application/json'}
number_of_posts = 0

with open('config.txt') as f:
    for line in f:
        line_data = line.strip().split('=')
        if line_data[0] == 'number_of_users':
            data['users'] = line_data[1]
        elif line_data[0] == 'max_posts_per_user':
            data['posts'] = line_data[1]
        elif line_data[0] == 'max_likes_per_user':
            data['likes'] = line_data[1]

for user in range(int(data['users'])):
    # Sign up users
    sign_in_data = {
        'username': emails[user].split('@')[0],
        'email': emails[user],
        'password': emails[user].split('@')[0]
    }
    r = requests.post(
        'http://127.0.0.1:8000/api/socialnetwork/signup/',
        data=json.dumps(sign_in_data),
        headers=headers
    )
    # print(r.status_code)

    # Log in users
    log_in_data = {
        'username': emails[user].split('@')[0],
        'password': emails[user].split('@')[0]
    }
    r = requests.post(
        'http://127.0.0.1:8000/api/socialnetwork/login/',
        data=json.dumps(log_in_data),
        headers=headers
    )
    # print(r.status_code)

    # Creating posts
    for post in range(randint(1, int(data['posts']))):
        post_data = {
            'post_text': emails[user].split('@')[0] + 'post #' + str(post + 1)
        }
        r = requests.post(
            'http://127.0.0.1:8000/api/socialnetwork/',
            data=json.dumps(post_data),
            headers=headers,
            auth=HTTPBasicAuth(log_in_data['username'], log_in_data['password'])
        )
        # print(r.status_code)
        number_of_posts += 1

# print()
# Like posts
for user in range(int(data['users'])):
    log_in_data = {
        'username': emails[user].split('@')[0],
        'password': emails[user].split('@')[0]
    }
    for like in range(int(data['likes'])):
        post = randint(1, number_of_posts)
        r = requests.post(
            'http://127.0.0.1:8000/api/socialnetwork/like/%i/' % post,
            auth=HTTPBasicAuth(log_in_data['username'], log_in_data['password'])
        )
        # print(r.status_code)
        # if r.status_code == 404:
        #     print(post)
        #     print(r.text)
