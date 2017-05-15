import os
import yaml
from datetime import datetime
import jinja2

def gen_post_name(title):
    ''' Define post name as per jekyll YEAR-MONTH-DAY-title.MARKUP '''
    reverse_date = datetime.today().strftime('%Y-%m-%d')
    # First five words of the title
    ti = str.split(title)[:5]
    f = reverse_date + '-' + '-'.join(ti) + '.md'
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
    import unicodedata
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


if os.getcwd() != '/Users/steve/projects/cc-Journal Club/site/src':
    os.chdir('/Users/steve/projects/cc-Journal Club/site/src')

# Open dictionary
with open('data-test.yml', 'r') as f:
    post = yaml.load(f)

post['authors_all'] = list2string(post['authors'])
post['post_date'] = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
post['jekyll_tags'] = []
post['journal']
post['jekyll_tags'].append(text2tag(post['journal']))
post['jekyll_tags'].append(text2tag(post['reviewer']))
# post['jekyll_tags'].append('eggs')
post['jekyll_tags']

# Make an excerpt from the pubmed abstract (will go link list)
if 'excerpt' not in post.keys():
    excerpt = str.split(post['abstract'])[:30]
    post['excerpt'] = ' '.join(excerpt)

# Make a header paragraph
s = list2string(post['authors'][:3]) + ', et al. '
s = s + post['title']
s = s + ' _' + post['journal'] + '_'
s = s + ' **' + str.split(post['date'])[0] + '**;'
s = s + '' + post['volume'] + ';'
s = s + '' + post['pages'] + '. '
s = s + '' + post['doi'] + ''

post['reference'] = s


# 1.	Schaller SJ, Anstey M, Blobner M, Edrich T, Grabitz SD, Gradwohl-Matis I, et al. Early, goal-directed mobilisation in the surgical intensive care unit: a randomised controlled trial. The Lancet. 2016;388: 1377–1388. doi:10.1016/S0140-6736(16)31637-3

# Sanitise
for k,v in post.items():
    if type(v) == str:
        post[k] = sanitise_text(v)



templateLoader = jinja2.FileSystemLoader(searchpath='.')
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "article-template.jinja"
template = templateEnv.get_template( TEMPLATE_FILE )
outputText = template.render( post )

# print(outputText)

file_name = gen_post_name(post['title'])
p = os.path.join('../site/_posts/articles', file_name)
with open(p, 'wt') as f:
    f.write(outputText)
