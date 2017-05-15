# Created by Steve Harris
# Created on 2017-05-15
# Aim: Build a static blog from a trello board that works for the journal club

# GTD

## Todos

# - [x] @TODO: (2017-05-12) connect to a trello for publishing
# - [x] @TODO: (2017-05-12) download cards from the publish list
# - [x] @TODO: (2017-05-13) add fields for reviewer and editor onto trello
# - [x] @TODO: (2017-05-12) parse description
# - [ ] @TODO: (2017-05-12) parse the card as a class
# - [x] @TODO: (2017-05-12) pull the associated pubmed data
# - [x] @TODO: (2017-05-13) prep the jekyll site
# - [x] @TODO: (2017-05-12) create a markdown file for a jekyll post
# - [x] @TODO: (2017-05-13) use jinja as the templating engine
# - [ ] @TODO: (2017-05-12) publish
# - [x] @TODO: (2017-05-13) authors override in so-simple theme, set up authors.yaml for each editor
# - [x] @TODO: (2017-05-13) add datascibc article to site
# - [ ] @TODO: (2017-05-15) use labels as tags
# - [ ] @TODO: (2017-05-15) use columns for publishing, after publishing move article
# - [ ] @TODO: (2017-05-15) place comment on trello with link after publishing
# - [ ] @TODO: (2017-05-15) delete old post if re-appears in to publish column
# - [ ] @TODO: (2017-05-15) rewrite into single script that you can run from the command line

# - [ ] @TODO: (2017-05-15) set up to run as CLI
# - [ ] @TODO: (2017-05-15) set-up as docker to manage dependencies


# Load python modules as needed
import os
import sys
import json
import yaml
import requests
from datetime import datetime
from Bio import Entrez, Medline
from Bio.Entrez import efetch, read
import argparse

# Debugging hacks
# os.getcwd()
# os.chdir('src')


def read_yaml(file_name):
    '''read yaml from file'''
    with open(file_name, 'r') as f:
        d = yaml.load(f)
    return(d)

def get_trello_key(url='https://trello.com/app-key'):
    ''' Opens a web browser, calls Trello and after logging in displays key
    The user must save the key into private.yaml '''
    from webbrowser import open_new_tab
    open_new_tab(url)

def get_trello_token(app_name='trello2jekyll', trello_key=None, scope='write'):
    '''Get token for this app, default scope is read'''
    # Example URL
    # https://trello.com/1/connect?key=yourkey&name=your_board_name&expiration=never&response_type=token&scope=read,write

    from webbrowser import open_new_tab
    from yaml import load

    if trello_key is None:
        private_keys = read_yaml('private.yaml')
        trello_key = private_keys['trello-key']

    url_begin = 'https://trello.com/1/authorize?scope=read&expiration=never&name='
    url_end = '&key=' + trello_key + '&response_type=token'

    if scope == 'read':
        url_scope = '&scope=read'
    elif scope == 'write':
        url_scope = '&scope=read,write'

    url = url_begin + app_name + url_end + url_scope
    open_new_tab(url)

def all_boards(API, auth):
    '''Return a list of all boards'''
    boards_url = '{}members/me/boards{}'.format(API, auth)
    try:
        all_boards = requests.get(boards_url).json()
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.Timeout as e:
        # Time out
        print(e)
    except requests.exceptions.TooManyRedirects as e:
        # Bad URL
        print(e)
    return all_boards

def get_board(BOARD_ID):
    ''' Return a single board based on provided ID '''
    boards = all_boards(API, auth)
    try:
        the_board = [b for b in boards if b['id'] == BOARD_ID][0]
    except IndexError:
        print('!!! Board not found, check you have provided the right BOARD_ID')
    else:
        print('--- Publishing from board: ' + the_board['name'])
    return(the_board)


def get_from_board(item, board_id, API, auth):
    '''Return a list of cards, lists, plugins etc from a board'''
    try:
        assert item in ['cards', 'lists', 'pluginData']
    except AssertionError as e:
        print(e)
        print('!!! ' + item + ' not recognised')
        sys.exit(1)
    url = '{}boards/{}/{}{}'.format(API, board_id, item, auth)

    try:
        _items = requests.get(url).json()
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.Timeout as e:
        # Time out
        print(e)
    except requests.exceptions.TooManyRedirects as e:
        # Bad URL
        print(e)
    return _items

def cards_from_list(list_name, cards, lists):
    '''Filter cards by name of list'''
    l = [i for i in lists if i['name'].lower() == list_name.lower()]
    assert len(l) == 1
    list_id = l[0]['id']
    c = [j for j in cards if j['idList'] == list_id]
    return c


# Instructions and prompts to enable the script to work as an app with Trello
# Connect to Trello


# Read all the cards from the 3 lists
    # !!!Ready to Publish (publish)
    # !!!Published (a destination list)
    # !!!Unpublish (i.e. remove blog post)
# Process cards

# Unpublish blog post
# move file into _unpublished folder with timestamp in filename
# move card to !!!Ready to publish list
# Insert notes about this into comments of card

# Publish blog post
# Download and check card data
# Connect to pubmed and extract pubmed info
# Assemble data into dictionary and clean text
# Make file using jinja template, save into _posts/articles
# move card into !!!Published list
# add comment regarding above into card

def cli():
    ''' Command line interface for running script '''

    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Publish from Trello to Jekyll'
    )

    # destination folders for blog
    parser.add_argument('-d',
                        metavar='DEST',
                        default = '../_posts/articles',
                        help='Article destination folder')

    # board to read
    parser.add_argument('-b',
                        metavar='BOARD',
                        default = 'Journal club - blog',
                        help='Name of Trello board')

    # Help user get to API key
    parser.add_argument('--trello_key',
                        action='store_true',
                        help='Open default webbrowser and display API key')

    # Help user get to token for reading and writing
    parser.add_argument('--trello_token',
                        action='store_true',
                        help='Open default webbrowser and display API token')

    args = parser.parse_args()
    article_dir = args.d

    if args.trello_key is True:
        get_trello_key()
        print('--- Save your key in private.yaml')
        print('--- Scroll down the page, and save your OAuth token in private.yaml')
        sys.exit(0)

    if args.trello_token is True:
        get_trello_token()
        print('--- Save your token in private.yaml')
        sys.exit(0)

    if os.path.exists(article_dir) is False:
        print('Folder', article_dir, 'not found')
        sys.exit(1)

    return args


if __name__ == '__main__':
    args = cli()

    # Load configuration data
    # =======================
    # API for trello
    API = 'https://api.trello.com/1/'
    # Read the API keys from the environment variables
    CONFIG_PRIVATE = 'private.yaml'

    # Keys
    private_keys = read_yaml(CONFIG_PRIVATE)

    API_KEY = private_keys['trello-key']
    API_TOKEN = private_keys['trello-token']
    auth = '?key={}&token={}'.format(API_KEY, API_TOKEN)

    # Board to publish
    BOARD_ID = private_keys['board2publish']

    print('--- Configuration OK')

    # Load boards, cards, lists, plugins
    the_board = get_board(BOARD_ID)
    pluginData = get_from_board('pluginData', BOARD_ID, API, auth)
    lists = get_from_board('lists', BOARD_ID, API, auth)
    cards = get_from_board('cards', BOARD_ID, API, auth)

    try:
        cards2publish = cards_from_list('!!!Ready to publish', cards=cards, lists=lists)
        print('--- Found {} cards to publish'.format(len(cards2publish)))
    except:
        print('!!! Problem finding Ready to publish list')

    try:
        cards2unpublish = cards_from_list('!!!Unpublish', cards=cards, lists=lists)
        print('--- Found {} cards to UNpublish'.format(len(cards2unpublish)))
    except:
        print('!!! Problem finding Unpublish list')





    print('--- End of script: all tasks complete')
