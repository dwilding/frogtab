# This script checks whether the server responds correctly to API calls

import requests

def success_body(response):
    assert response.status_code == 200
    data = response.json()
    assert 'success' in data
    assert data['success']
    return data

def failure_only(response):
    assert response.status_code == 200
    data = response.json()
    assert data.keys() == {'success'}
    assert not data['success']

# Register a user
PGP_PUBLIC_KEY = '''-----BEGIN PGP PUBLIC KEY BLOCK-----

xjMEZQKv7RYJKwYBBAHaRw8BAQdAQ4PrjRAjxXcDCAyXk9e8uzxh7PgeOqyl
vGPa56HXD5bNNjxrZXkrNzc3MTM0MDAtZDcxOS00NDZjLWE4ZjQtNjc1OTRk
ZjM2ZGE2QGZyb2d0YWIuY29tPsKMBBAWCgA+BYJlAq/tBAsJBwgJkB4XttlV
8mCPAxUICgQWAAIBAhkBApsDAh4BFiEEuvokTQ+6AFAHgFolHhe22VXyYI8A
AC07AQCMShgJhMBB0t40zqGRaVwWplk/dKJlzC0kbfqGx7n0hQEAvmJr+0A0
L0N8hGfsDL5jHEkAZekREDpzfn97nhgBiwLOOARlAq/tEgorBgEEAZdVAQUB
AQdAojdSTm+t3RP/jO4/cci0tvzKu7TkJP3JATqRBbGrFhQDAQgHwngEGBYI
ACoFgmUCr+0JkB4XttlV8mCPApsMFiEEuvokTQ+6AFAHgFolHhe22VXyYI8A
AL1iAP4j+D3FhEk6D1YGeMu3S0SdLJiTB6i7yGXVOkUt69U6nQEAjKznIHnT
533fpczRbqny4ViRgCXRZ3Jk5GRQXYhh9wE=
=Ot5x
-----END PGP PUBLIC KEY BLOCK-----
'''
ENCRYPTED_COMMENT = '''-----BEGIN PGP MESSAGE-----

wV4D3yKzBdYhqlwSAQdAs+3HSkt/V7rIMaRSqHAXR/7MRz/bpN5LtpzwpC0T
tXcwBFsyWa6vC/PRSInH5gRtvGt2rf1qJsJLxvFc9GwqVQLQewKMYGxUYNhF
23z/Xy1g0kYBNd4mozNFkyODXM3bR/1hp8gDRAQsY1Gn6gKXk8R0wYNYwC5Y
nQ63YgNib+ELXl44Hu8tEjYY65R3sBk8lCv67eY6UQKP
=9WlR
-----END PGP MESSAGE-----
'''
registration_data = success_body(requests.post('https://frogtab.com/post-create-user', json={
    'pgp_public_key': PGP_PUBLIC_KEY,
    'comment': ENCRYPTED_COMMENT
}))
assert 'user' in registration_data
assert 'user_id' in registration_data['user']
user_id = registration_data['user']['user_id']
assert 'api_key' in registration_data['user']
api_key = registration_data['user']['api_key']

# Lookup the user's public key
user_data = success_body(requests.get(f"https://frogtab.com/open/get-user?user_id={user_id}"))
assert 'user' in user_data
assert 'user_id' in user_data['user']
assert user_data['user']['user_id'] == user_id
assert 'pgp_public_key' in user_data['user']
assert user_data['user']['pgp_public_key'] == PGP_PUBLIC_KEY

# Send a message to the user
ENCRYPTED_MESSAGE_1 = '''-----BEGIN PGP MESSAGE-----

wV4DMgVFzGEeJ8ESAQdAGHDeMR7jibhWOOb2epDsSBfnnvoEnfBl71uYESao
lE4wR9HO4Ofh0jb9K2I5WAdCDNHsIgljayh5RcmzHkTr10KTx6p8ISGzFnTT
aGPnkRKd0joBEfrQpCBBgk5dk5EUagkFhpeX5H87j0aBgl58J7sJrIbVEZrZ
9M1rMcz6Q0uZ8ofoZ7xMio8ou2Bm
=wMdo
-----END PGP MESSAGE-----
'''
success_body(requests.post('https://frogtab.com/open/post-add-message', json={
    'user_id': user_id,
    'message': ENCRYPTED_MESSAGE_1
}))

# Send another message to the user
ENCRYPTED_MESSAGE_2 = '''-----BEGIN PGP MESSAGE-----

wV4DMgVFzGEeJ8ESAQdAc9bX6vREt3HHgGDIu2su4JBK3XZHYsya0tt4oAE4
rAEwA+LIIQNX92xrPO19E/Qj43Jly+EXoXJWzJK2PKi61Vuoff++9T27+6et
as8Pa3Bs0joBMRfP12XTSJVxP86E43KBvuumh1/GesM/Lm/D2N47UnIlDdwr
/BmlwtY6FQuwNyfRuqmGVYRQ7wEo
=HIoH
-----END PGP MESSAGE-----
'''
success_body(requests.post('https://frogtab.com/open/post-add-message', json={
    'user_id': user_id,
    'message': ENCRYPTED_MESSAGE_2
}))

# Fail to check the user's messages if no API key is provided
failure_only(requests.post('https://frogtab.com/post-remove-messages', json={
    'user_id': user_id
}))

# Fail to check the user's messages if the wrong API key is provided
failure_only(requests.post('https://frogtab.com/post-remove-messages', json={
    'user_id': user_id,
    'api_key': '0123456789abcdef'
}))

# Check the user's messages
message_data = success_body(requests.post('https://frogtab.com/post-remove-messages', json={
    'user_id': user_id,
    'api_key': api_key
}))
assert 'messages' in message_data
assert isinstance(message_data['messages'], list)
assert len(message_data['messages']) == 2
assert message_data['messages'][0] == ENCRYPTED_MESSAGE_1
assert message_data['messages'][1] == ENCRYPTED_MESSAGE_2

# Now there are no messages on the server
message_data_none = success_body(requests.post('https://frogtab.com/post-remove-messages', json={
    'user_id': user_id,
    'api_key': api_key
}))
assert 'messages' in message_data_none
assert isinstance(message_data_none['messages'], list)
assert len(message_data_none['messages']) == 0

# Fail to remove the user if no API key is provided
failure_only(requests.post('https://frogtab.com/post-remove-user', json={
    'user_id': user_id
}))

# Fail to remove the user if the wrong API key is provided
failure_only(requests.post('https://frogtab.com/post-remove-user', json={
    'user_id': user_id,
    'api_key': '0123456789abcdef'
}))

# Remove the user
success_body(requests.post('https://frogtab.com/post-remove-user', json={
    'user_id': user_id,
    'api_key': api_key
}))

# Fail to lookup the user's public key
failure_only(requests.get(f"https://frogtab.com/open/get-user?user_id={user_id}"))

# Fail to send a message to the user
failure_only(requests.post('https://frogtab.com/open/post-add-message', json={
    'user_id': user_id,
    'message': ENCRYPTED_MESSAGE_1
}))

# Fail to check the user's messages
failure_only(requests.post('https://frogtab.com/post-remove-messages', json={
    'user_id': user_id,
    'api_key': api_key
}))

# Fail to remove the user
failure_only(requests.post('https://frogtab.com/post-remove-user', json={
    'user_id': user_id,
    'api_key': api_key
}))