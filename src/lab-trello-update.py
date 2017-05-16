# Aim connect to a trello board
# Docs at https://developers.trello.com/get-started/start-building
# Application key
# hacked from trell0-full-backup


import sys
import os
import datetime
import requests
import json
import yaml

# just to ensure in right place
os.getcwd()
os.chdir('/Users/steve/projects/cc-Journal Club/site/src')
os.getcwd()


# API for trello
API = 'https://api.trello.com/1/'

# Read the API keys from the environment variables
CONFIG_PRIVATE = 'private.yaml'

def read_yaml(file_name):
    '''read yaml from file'''
    with open(file_name, 'r') as f:
        d = yaml.load(f)
    return(d)

def get_trello_token(app_name, trello_app_key, scope='read'):
    '''Get token for this app, default scope is read'''
    # Example URL
    # https://trello.com/1/authorize?scope=read&expiration=never&name=cc-journalclub&key=REPLACE_WITH_YOUR_API_KEY&response_type=token
    # then use this function as below
    # run this and then copy paste result into browser, then save key into private.yaml
    # print(get_trello_token('uclh-journalclub', trello_app_key))
    # https://trello.com/1/connect?key=yourkey&name=your_board_name&expiration=never&response_type=token&scope=read,write
    url_begin = 'https://trello.com/1/authorize?scope=read&expiration=never&name='
    url_end = '&key=' + trello_app_key + '&response_type=token'
    if scope == 'read':
        url_scope = '&scope=read'
    elif scope == 'write':
        url_scope = '&scope=read,write'
    url = url_begin + app_name + url_end + url_scope
    print(url)



dict_private = read_yaml(CONFIG_PRIVATE)
API_KEY = dict_private['trello-app-key']
# print(get_trello_token('uclh-journalclub', API_KEY, scope='write'))
API_TOKEN = dict_private['trello-app-token']
BOARD_ID = dict_private['jclub-summary-board-id']

auth = '?key={}&token={}'.format(API_KEY, API_TOKEN)

boards_url = '{}members/me/boards{}'.format(API, auth)

def all_cards(board_id, API=API, auth=auth):
    '''Return a list of cards on a board'''
    url = '{}boards/{}/cards{}'.format(API, board_id, auth)
    return url

def all_lists(board_id, API=API, auth=auth):
    '''Return a list of lists on a board'''
    url = '{}boards/{}/lists{}'.format(API, board_id, auth)
    return url

lists_url =all_lists(BOARD_ID)
cards_url =all_cards(BOARD_ID)

def all_plugins(board_id, API=API, auth=auth):
    '''Return plug-in data from board'''
    url = '{}boards/{}/pluginData{}'.format(API, board_id, auth)
    return url

plugins_url = all_plugins(BOARD_ID )
these_plugins = requests.get(plugins_url).json()
these_plugins


all_boards = requests.get(boards_url).json()
these_lists = requests.get(lists_url).json()
lists_dict = {l['name']:l['id'] for l in these_lists}
these_cards = requests.get(cards_url).json()

# Select a list
def cards_from_list(list_name, cards=these_cards, lists=these_lists):
    '''Filter cards by name of list'''
    l = [i for i in lists if i['name'].lower() == list_name]
    assert len(l) == 1
    list_id = l[0]['id']
    c = [j for j in cards if j['idList'] == list_id]
    return c


cards = cards_from_list('test')
card_data = cards[0]
CARD_ID = card_data['id']

# Get card plugin data
def card_plugin_url(card_id, API=API, auth=auth):
    '''Return plug-in data from card'''
    url = '{}cards/{}/pluginData{}'.format(API, card_id, auth)
    return url

this_plugin_url = card_plugin_url(CARD_ID)
card_plugin_data = requests.get(this_plugin_url).json()
card_plugin_data
custom_field_data = json.loads(card_plugin_data[0]['value'])['fields']

# Now label up plugin data as keyvalue pairs for fields
# the dict is stored as a string so convert using json module
# this assumes only one custom field
json.loads(these_plugins[0]['value'])['fields']
custom_fields = dict(json.loads(these_plugins[0]['value']))['fields']
# lookup dictionary for field names
custom_field_dict = {i['id']: i['n'] for i in custom_fields}
custom_field_dict

# now relabel
custom_fields_clean = {custom_field_dict[k]:v for k,v in custom_field_data.items()}
card_data['custom_fields'] = custom_fields_clean

card_data
with open('card-test.yml', 'wt') as f:
    yaml.dump(card_data, f, default_flow_style=False)

# Now try writing to card
# POST /1/cards/[card id or shortlink]/actions/comments
'{}cards/{}/pluginData{}'.format(API, CARD_ID, auth)
comments_url = '{}cards/{}/actions/comments'.format(API, CARD_ID)
# curl -D -X POST -F "file=@[path/to/file]" https://api.trello.com/1/cards/[cardId]/attachments?key=[yourKey]&token=[yourToken]
payload = 'Hello world 2017-05-15t17:22'
params = {'key': API_KEY, 'token': API_TOKEN, 'text': payload}
# files = {'file': open(file_path, 'rb')}
# url = ATTACHMENTS_URL % card_id
r = requests.post(comments_url, params=params)
# r.url
r.status_code
# r
r.text


# Now try moving the card to a new list
these_lists
move2list_url = '{}cards/{}/idList'.format(API, CARD_ID)
payload = lists_dict['Published']
payload
params = {'key': API_KEY, 'token': API_TOKEN, 'value': payload}
r = requests.put(move2list_url, params=params)
r.url
r.status_code
