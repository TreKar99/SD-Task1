#!/usr/bin/env python3


import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

private_chats = {
    'Germán': '198.124.23.14',
    'Montse': '198.125.12.12',
    'Pedro': '129.43.123.21'
}

group_chats = {
    'local': 'localhost',
    'otro': '192.168.12.0',
    'no': '198.128.12.2'
}


def list_chat(r, hash_name):
    key_value_pairs = r.hgetall(hash_name)
    list_of_pairs = []

    for key, value in key_value_pairs.items():
        key = key.decode('utf-8') if isinstance(key, bytes) else key
        value = value.decode('utf-8') if isinstance(value, bytes) else value

        list_of_pairs.append((key, value))

    print(f"Key-Value Pairs from '{hash_name}':")
    for key, value in list_of_pairs:
        print(f"  - {key}: {value}")


def list_chats():

    try:

        r = redis.StrictRedis(host=redis_host, port=redis_port,
                              password=redis_password, decode_responses=True)

        # Add key-value pairs to the Redis hash
        for key, value in private_chats.items():
            r.hset('private_chats', key, value)

        # Add key-value pairs to the Redis hash
        for key, value in group_chats.items():
            r.hset('group_chats', key, value)

        # Retrieve the value associated with key 'name'
        # name = r.hget('group_chats', 'local')
        # print(name)

        list_chat(r, 'private_chats')
        list_chat(r, 'group_chats')

    except Exception as e:
        print(e)


if __name__ == '__main__':
    list_chats()
