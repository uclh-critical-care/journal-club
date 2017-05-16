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
import argparse
import jinja2
import unicodedata
from datetime import datetime
from Bio import Entrez, Medline
from Bio.Entrez import efetch, read
from glob import glob

# Debugging hacks
# os.getcwd()
# os.chdir('src')


def read_yaml(file_name):
    '''read yaml from file'''
    with open(file_name, 'r') as f:
        d = yaml.load(f)
    return(d)

def dict_with_key_equal_to(l, k, v):
    ''' Filters a list of dictionaries,
    returns the dictionary with a key matching the value '''
    l = [i for i in l if i[k].lower() == v.lower()]
    # Check there's only 1 dictionary
    assert len(l) == 1
    return l[0]

# Instructions and prompts to enable the script to work as an app with Trello
# Connect to Trello


# Read all the cards from the 3 lists
    # !!!Ready to Publish (publish)
    # !!!Published (a destination list)
    # !!!Unpublish (i.e. remove blog post)
# Process cards

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

def get_card_plugin_data(CARD_ID, API, auth):
    '''Return plug-in data from card'''
    url = '{}cards/{}/pluginData{}'.format(API, CARD_ID, auth)
    try:
        _data = requests.get(url).json()
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.Timeout as e:
        # Time out
        print(e)
    except requests.exceptions.TooManyRedirects as e:
        # Bad URL
        print(e)
    return _data

def get_custom_fields(card_id, custom_field_dict, API, auth):
    ''' Given a card convert custom fields into dictionary by field name '''
    plugin_data = get_card_plugin_data(card_id, API, auth)
    plugin_data = dict(json.loads(plugin_data[0]['value']))['fields']
    custom_fields_clean = {custom_field_dict[k]:v for k,v in plugin_data.items()}
    return custom_fields_clean

def cards_from_list(list_name, cards, lists):
    '''Filter cards by name of list'''
    l = [i for i in lists if i['name'].lower() == list_name.lower()]
    assert len(l) == 1
    list_id = l[0]['id']
    c = [j for j in cards if j['idList'] == list_id]
    return c

def move_card_to_list(card_id, list_id, API, API_KEY, API_TOKEN):
    ''' Move card to list '''
    # URL for Put
    url = '{}cards/{}/idList'.format(API, card_id)
    params = {'key': API_KEY, 'token': API_TOKEN, 'value': list_id}
    r = requests.put(url, params=params)
    return r

def add_comment_to_card(card_id, text, API, API_KEY, API_TOKEN):
    ''' Add a comment to a card '''
    url = '{}cards/{}/actions/comments'.format(API, card_id)
    params = {'key': API_KEY, 'token': API_TOKEN, 'text': text}
    r = requests.post(url, params=params)
    return r


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

def gen_post_name(text):
    ''' Define post name as per jekyll YEAR-MONTH-DAY-text.MARKUP '''
    reverse_date = datetime.today().strftime('%Y-%m-%d')
    f = reverse_date + '-' + text + '.md'
    return f

# Format post data where needed
def list2string(l):
    '''Convert list of text to comma separated string with final "and" '''
    s = ', '.join(l[:-1]) + ', and ' + l[-1]
    return s

def sanitise_text(s, ascii=True):
    '''Convert to default unicode mapping etc'''
    # Remove leading and trailing white space
    s = s.strip()
    s = unicodedata.normalize('NFC', s)
    if ascii:
        # Encode then decode to force drop all non ascii characters
        s = s.encode('ascii', 'ignore').decode('ascii')
    return s

def text2tag(s):
    '''Convert string to lower case, replace white space with underscore'''
    legal_chars = '_abcdefghijklmnopqrstuvwxyz0123456789'
    remap_whitespace = {
        ord(' ') : '_',
        ord('\t') : '_',
        ord('\n') : '_',
        ord('\f') : '_',
        ord('\r') : None
    }
    s = s.translate(remap_whitespace)
    s = s.lower()
    s = [c for c in s if c in legal_chars]
    return ''.join(s)

def read_medline(pmid, email):
    '''Read a pubmed record identified by its PMID as Medline text'''
    # Must register email for Bio.Entrez to work
    Entrez.email = email
    try:
        handle = Entrez.efetch(db='pubmed', id=pmid, retmode='text', rettype='medline')
    except Exception as e:
        print('!!! Unable to retrieve PubMed record: {}'.format(e))
    records = Medline.parse(handle)
    record = next(records)
    # Now check you only got one record as per http://stackoverflow.com/a/7460986
    assert sum(1 for x in records) == 0
    handle.close()
    return record

def format_reference(record):
    ''' Takes Medline record and returns BMJ style formatted reference '''

    # Check all keys present
    assert len([i
        for i in ['AU', 'TI', 'TA', 'DP', 'VI', 'PG', 'LID']
        if i not in record.keys()]
        ) == 0

    s = list2string(record['AU'][:3]) + ', et al. '
    s = s + record['TI']
    s = s + ' _' + record['TA'] + '_'
    s = s + ' **' + str.split(record['DP'])[0] + '**;'
    s = s + '' + record['VI'] + ';'
    s = s + '' + record['PG'] + '. '
    s = s + 'https://doi.org/' + str.split(record['LID'])[0] + ''
    return s

def make_post(template_file, data):
    ''' Create a Jekyll formatted blog post using provided data and template '''
    templateLoader = jinja2.FileSystemLoader(searchpath='.')
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template( TEMPLATE_FILE )
    outputText = template.render( data )
    return outputText

# Command line interaction
# ========================

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
    # Need to register an email with Entrez else won't run
    ENTREZ_EMAIL = 'm@steveharris.me'
    # API for trello
    API = 'https://api.trello.com/1/'
    # Read the API keys from the environment variables
    CONFIG_PRIVATE = 'private.yaml'
    # JINJA template file for article
    TEMPLATE_FILE = "article-template.jinja"
    # Article destination directory
    ARTICLE_PATH = args.d
    UNPUBLISH_PATH = '../_unpublished'
    # Permalink stem http://uclh-critical-care.github.io/journal-club/articles/
    URL_SITE = 'http://uclh-critical-care.github.io/journal-club'

    # Keys (stored locally, make sure in .gitignore to avoid inadvertent publication)
    # Extract private configuration keys from local YAML file
    private_keys = read_yaml(CONFIG_PRIVATE)
    API_KEY = private_keys['trello-key']
    API_TOKEN = private_keys['trello-token']
    auth = '?key={}&token={}'.format(API_KEY, API_TOKEN)

    # Board to publish
    BOARD_ID = private_keys['board2publish']

    print('--- Configuration OK')

    # Load boards, cards, lists, plugins
    the_board = get_board(BOARD_ID)
    lists = get_from_board('lists', BOARD_ID, API, auth)
    cards = get_from_board('cards', BOARD_ID, API, auth)

    # Named lists
    list_unpublish = dict_with_key_equal_to(lists, 'name', '!!!Unpublish')
    list_ready2publish = dict_with_key_equal_to(lists, 'name', '!!!Ready to publish')
    list_published = dict_with_key_equal_to(lists, 'name', '!!!Published')

    # Get plug in data from board and create dictionary for custom fields
    pluginData = get_from_board('pluginData', BOARD_ID, API, auth)
    custom_fields = dict(json.loads(pluginData[0]['value']))['fields']
    custom_field_dict = {i['id']: i['n'] for i in custom_fields}

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


    for card in cards2unpublish:
        # - [ ] @TODO: (2017-05-16) move corresponding blog post to archive
        # ARTICLE_PATH = '../_posts/articles'
        # os.listdir(ARTICLE_PATH)
        try:
            post_path = glob('{}/*{}*.md'.format(ARTICLE_PATH, card['shortLink']))
            assert len(post_path) == 1
            post_path = post_path[0]
        except AssertionError as e:
            print(
                '!!! Found {} files, expecting 1 when trying to unpublish {}'.format(
                len(post_path), card['name'][:40]))
            print(e)

        try:
            to_path = os.path.join(UNPUBLISH_PATH, os.path.basename(post_path))
            os.rename(post_path, to_path)
        except Exception as e:
            print('!!! Problem moving file from {} to {}'.format(post_path, UNPUBLISH_PATH))


        move_card_to_list(card['id'], list_ready2publish['id'], API, API_KEY, API_TOKEN)
        reverse_timestamp = datetime.today().strftime('%Y-%m-%d %H:%S')
        comment = '''Card unpublished at {} \nFile moved from {} to {}'''.format(
            reverse_timestamp, post_path, UNPUBLISH_PATH)
        add_comment_to_card(card['id'], comment, API, API_KEY, API_TOKEN)
        print('--- Unpublishing card {}: {} ...'.format(card['shortLink'], card['name'][:40]))

    for card in cards2publish:

        # card = cards2publish[0]
        # Load and format custom fields
        card['custom_fields'] = get_custom_fields(
            card['id'],
            custom_field_dict,
            API, auth)

        # Get PubMed data and construct a dictionary from card + pubmed
        pmid = card['custom_fields']['PubMed ID']
        record = read_medline(pmid, email=ENTREZ_EMAIL)
        print('--- Found PubMed data for PMID {}'.format(pmid))
        # Check no duplicate keys then merge data
        assert len([i for i in card.keys() if i in record.keys()]) == 0

        # Add formatted citation into data
        data = {**card, **record}
        data['citation'] = format_reference(record)

        # Add formatted author list into data
        data['authors_all'] = list2string(record['AU'])
        data['post_date'] = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')

        # Add tags into data
        data['jekyll_tags'] = []
        data['jekyll_tags'].append(text2tag(record['TA']))
        data['jekyll_tags'].append(text2tag(card['custom_fields']['Reviewer']))
        # Use card labels as tags too
        card_labels = [l['name'] for l in card['labels']]
        data['jekyll_tags'].extend(card_labels)

        # Add pubmed URL
        data['pubmed_url'] = 'https://www.ncbi.nlm.nih.gov/pubmed/?term={}'.format(pmid)

        # Add tweet (doubles a slug) or use first 30 words of abstract
        tweet = card['custom_fields']['Tweet']
        if len(tweet) == 0:
            slug = str.split(data['AB'])[:30]
            data['slug'] = ' '.join(slug)
        else:
            data['slug'] = tweet[:140]
        data['slug'] = data['slug'] + ' (Reviewed by {})'.format(card['custom_fields']['Reviewer'])

        # Santise all text
        for k,v in data.items():
            if type(v) == str:
                data[k] = sanitise_text(v)

        # Pass data to blog post making function
        # - [ ] @TODO: (2017-05-16) construct post and save
        try:
            article_text = make_post(TEMPLATE_FILE, data)
        except Exception:
            print('!!! Failed to generate blog post from article template')

        # article_text
        # Generate a file name for the blog post using shortLink as unique ID
        post_name = gen_post_name(data['shortLink'])
        # ARTICLE_PATH = '../_posts/articles'
        post_path = os.path.join(ARTICLE_PATH, post_name)
        post_url = URL_SITE + '/articles/' + data['shortLink']

        # Save text to file
        try:
            with open(post_path, 'wt') as f:
                f.write(article_text)
        except OSError as e:
                print('!!! Error writing post to file: {}'.format(e))



        # Move card to list, and post link to blog post in comments
        move_card_to_list(card['id'], list_published['id'], API, API_KEY, API_TOKEN)
        reverse_timestamp = datetime.today().strftime('%Y-%m-%d %H:%S')
        # - [ ] @TODO: (2017-05-16) add permalink to blog post in comments
        comment = '''Card published at {}
        File path: {}
        URL: {}
        '''.format(
            reverse_timestamp,
            post_path,
            post_url
            )
        add_comment_to_card(card['id'], comment, API, API_KEY, API_TOKEN)
        print('--- Publishing card {}: {} ...'.format(card['shortLink'], card['name'][:40]))





    print("--- End of script: Don't forget to push your changes to github")
