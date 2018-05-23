import argparse
import configparser
import requests
import time


def print_ordinal():
    print("name:{}| messages count:".format(" " * 25))
    for id, name in get_friends().items():
        print('{:<30}|{:>15}'.format(name, get_dialog_count(id)))


def print_sorted_by_id():
    print("it may take some time")
    result = []
    for id, name in get_friends().items():
        result.append((name, get_dialog_count(id)))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    print("name:{}| messages count:".format(" " * 25))
    for name, count in result:
        print('{:<30}|{:>15}'.format(name, count))


def get_friends():
    payload = {'fields': 'name',
               'order': 'name',
               'access_token': token,
               'v': '5.76'}
    result = dict()
    for friend in make_request("friends.get", payload)['items']:
        result[friend['id']] = friend['first_name'] + ' ' + friend['last_name']
    return result


def get_dialog_count(id):
    payload = {'user_id': id,
               'count': '0',
               'access_token': token,
               'v': '5.76'}
    return make_request("messages.getHistory", payload)["count"]


def make_request(method, payload):
    response = requests.get("https://api.vk.com/method/{}".format(method), payload).json()
    if 'error' in response:
        time.sleep(0.5)
        return make_request(method, payload)
    else:
        return response['response']


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        token = config['ACCESS_INFO']['token']
    except:
        print("could not retrieve token")
        exit(0)
    parser = argparse.ArgumentParser(description="сообщет количество сообщений с друзьями")
    parser.add_argument('--sorted', '-s', action='store_true', help='отсортировать друзей по количеству сообщений')
    args = parser.parse_args()
    if args.sorted:
        print_sorted_by_id()
    else:
        print_ordinal()
