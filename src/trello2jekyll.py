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
from datetime import datetime
from Bio import Entrez, Medline
from Bio.Entrez import efetch, read
import argparse

# Debugging hacks
# os.getcwd()
# os.chdir('src')

def get_trello_key(url='https://trello.com/app-key'):
    ''' Opens a web browser, calls Trello and after logging in displays key
    The user must save the key into private.yaml '''
    from webbrowser import open_new_tab
    open_new_tab(url)

# Load configuration data
def get_trello_token(app_name='trello2jekyll', trello_key=None, scope='write'):
    '''Get token for this app, default scope is read'''
    # Example URL
    # https://trello.com/1/connect?key=yourkey&name=your_board_name&expiration=never&response_type=token&scope=read,write

    from webbrowser import open_new_tab
    from yaml import load

    if trello_key is None:
        with open('private.yaml', 'r') as f:
            private_keys = yaml.load(f)
            trello_key = private_keys['trello-key']

    url_begin = 'https://trello.com/1/authorize?scope=read&expiration=never&name='
    url_end = '&key=' + trello_key + '&response_type=token'

    if scope == 'read':
        url_scope = '&scope=read'
    elif scope == 'write':
        url_scope = '&scope=read,write'

    url = url_begin + app_name + url_end + url_scope
    open_new_tab(url)

    return 0

get_trello_token()

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
    print(args)

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


    print('Publishing tasks completed!')

if __name__ == '__main__':
    cli()
