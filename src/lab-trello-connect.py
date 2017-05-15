# Aim connect to a trello board
# Docs at https://developers.trello.com/get-started/start-building
# Application key
# hacked from trell-full-backup


import sys
import os
import re
import datetime
import requests
import json
import yaml

# just to ensure in right place
os.getcwd()
os.chdir('/Users/steve/projects/cc-Journal Club/site/src')
os.getcwd()


# Do not download files over 100 MB by default
ATTACHMENT_BYTE_LIMIT = 100000000
ATTACHMENT_REQUEST_TIMEOUT = 30  # 30 seconds
FILE_NAME_MAX_LENGTH = 100
FILTERS = ['open', 'all']

# API for trello
API = 'https://api.trello.com/1/'

# Read the API keys from the environment variables
CONFIG_PRIVATE = 'private.yaml'


def read_yaml(file_name):
    '''read yaml from file'''
    with open(file_name, 'r') as f:
        d = yaml.load(f)
    return(d)

def backup_board(board, args):
    ''' Backup the board '''
    board_details = requests.get(''.join((
        '{}boards/{}{}&'.format(API, board["id"], auth),
        'actions=all&actions_limit=1000&',
        'cards={}&'.format(FILTERS[args.archived_cards]),
        'card_attachments=true&',
        'labels=all&',
        'lists={}&'.format(FILTERS[args.archived_lists]),
        'members=all&',
        'member_fields=all&',
        'checklists=all&',
        'fields=all'
    ))).json()


def get_trello_token(app_name, trello_app_key):
    '''Get token for this app'''
    # Example URL
    # https://trello.com/1/authorize?scope=read&expiration=never&name=cc-journalclub&key=REPLACE_WITH_YOUR_API_KEY&response_type=token
    # then use this function as below
    # run this and then copy paste result into browser, then save key into private.yaml
    # print(get_trello_token('uclh-journalclub', trello_app_key))
    url_begin = 'https://trello.com/1/authorize?scope=read&expiration=never&name='
    url_end = '&key=' + trello_app_key + '&response_type=token'
    url = url_begin + app_name + url_end
    print(url)



dict_private = read_yaml(CONFIG_PRIVATE)
API_KEY = dict_private['trello-app-key']
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
