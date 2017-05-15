# Open dictionary
with open('card-test.yml', 'r') as f:
    card = yaml.load(f)

from Bio import Entrez, Medline
from Bio.Entrez import efetch, read
from yaml import load, dump

# Must register email for Bio.Entrez to work
Entrez.email = 'm@steveharris.me'

def read_medline(pmid):
    '''Read a pubmed record identified by its PMID as Medline text'''
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='text', rettype='medline')
    records = Medline.parse(handle)
    record = next(records)
    # Now check you only got one record as per http://stackoverflow.com/a/7460986
    assert sum(1 for x in records) == 0
    handle.close()
    return record


pmid = card['custom_fields']['PubMed ID']
record = read_medline(pmid)
# help(record) # Inspect tags

post = {}
post['title'] = record['TI']
post['journal'] = record['TA']
post['journal_full'] = record['JT']
post['abstract'] = record['AB']
post['authors'] = record['AU']
post['date'] = record['DP']
post['pages'] = record['PG']
post['volume'] = record['VI']
post['doi'] = card['custom_fields']['DOI']
post['pmid'] = card['custom_fields']['PubMed ID']
post['editor'] = card['custom_fields']['Editor']
post['reviewer'] = card['custom_fields']['Reviewer']
post['review'] = card['desc']
post['url_trello'] = card['shortUrl']
post['shortlink_trello'] = card['shortLink']
post['labels'] = [i['name'] for i in card['labels']]

# Now write all these data out
# Suggest convert into python dictionary, then write out as JSON?

post
# open file for writing in text mode (NB default is text)
with open('data-test.yml', 'wt') as f:
    yaml.dump(post, f, default_flow_style=False)
