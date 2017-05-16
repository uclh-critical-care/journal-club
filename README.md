# UCLH Critical Care Journal Club

The journal club is run from two trello boards.
A shared [board](https://trello.com/b/SrkK31HB) for all the trainees where articles are posted, and selected.
A [board for editing and publishing summaries](https://trello.com/b/jTuloSE3) from the journal club.

After a presentation, the presenter should save a 200-300 word commentary to the description part of the card. They will also be responsible for adding the following fields:

- DOI
- Pubmed ID
- Reviewer's first and last name (for credit on the blog)

The editorial team will then copy that card over to the board that works as a [blogging tool](https://trello.com/b/jTuloSE3). The commentary should be reviewed, and the links should be checked (and corrected if needed). When the article is ready to publish, then simply move the card from the 'Awaiting editorial review' list into the '!!!Ready to publish list'.

Lists prefixed with `!!!` (three exclamation marks) are managed by the Python script that converts the Trello card to a properly formatted Jekyll post. Moving cards from one list to another should trigger the actions described in the title the next time the `trello2jekyll.py` script runs.


- [ ] @TODO: (2017-05-15) add note about email to board settings
- [ ] @TODO: (2017-05-15) move the script and the blog onto a server where it can run regularly.

## Configuration


- To get the API key: https://trello.com/app-key
- To get the token: https://trello.com/1/authorize?scope=read&expiration=never&name=backup&key=REPLACE_WITH_YOUR_API_KEY&response_type=token
k


## Todos

Aim: Build a static blog from a trello board that works for the journal club

### Next

- [ ] @TODO: (2017-05-15) set-up as docker to manage dependencies
- [ ] @TODO: (2017-05-16) check for updates on published cards and republish these
- [ ] @TODO: (2017-05-16) formatting, smaller font for medline
- [ ] @TODO: (2017-05-16) add link to download presentation
- [ ] @TODO: (2017-05-16) fix editor link on blog
- [x] @TODO: (2017-05-16) fix about page
- [ ] @TODO: (2017-05-16) option to republish all in published column (e.g. where design changes)

## Todos

- [x] @TODO: (2017-05-12) connect to a trello for publishing
- [x] @TODO: (2017-05-12) download cards from the publish list
- [x] @TODO: (2017-05-13) add fields for reviewer and editor onto trello
- [x] @TODO: (2017-05-12) parse description
- [ ] @TODO: (2017-05-12) parse the card as a class
- [x] @TODO: (2017-05-12) pull the associated pubmed data
- [x] @TODO: (2017-05-13) prep the jekyll site
- [x] @TODO: (2017-05-12) create a markdown file for a jekyll post
- [x] @TODO: (2017-05-13) use jinja as the templating engine
- [x] @TODO: (2017-05-12) publish
- [x] @TODO: (2017-05-13) authors override in so-simple theme, set up authors.yaml for each editor
- [x] @TODO: (2017-05-13) add datascibc article to site
- [x] @TODO: (2017-05-15) use labels as tags
- [x] @TODO: (2017-05-15) use columns for publishing, after publishing move article
- [x] @TODO: (2017-05-15) place comment on trello with link after publishing
- [x] @TODO: (2017-05-15) delete old post if re-appears in to publish column
- [x] @TODO: (2017-05-15) rewrite into single script that you can run from the command line
- [x] @TODO: (2017-05-15) set up to run as CLI
