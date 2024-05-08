import requests

def rest_queue_list(user='guest', password='guest', host='localhost', port=15672, virtual_host=None):
    url = 'http://%s:%s/api/bindings/%s' % (host, port, virtual_host or '')
    response = requests.get(url, auth=(user, password))
    exchange = [q['source'] for q in response.json() if q["source"]]
    queues = [q['routing_key'] for q in response.json() if q["source"]]

    print("CHAT DISCOVERY (QUEUES)")
    for tupla in zip(exchange, queues):
        print("EXCHANGE: ", tupla[0], " QUEUE: ", tupla[1])
rest_queue_list()
