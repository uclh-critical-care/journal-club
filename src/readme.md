Aim: Build a static blog from a trello board that works for the journal club

# GTD

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

### Next

- [ ] @TODO: (2017-05-15) set-up as docker to manage dependencies
- [ ] @TODO: (2017-05-16) check for updates on published cards and republish these
- [ ] @TODO: (2017-05-16) formatting, smaller font for medline
- [ ] @TODO: (2017-05-16) add link to download presentation
- [ ] @TODO: (2017-05-16) fix editor link on blog
- [x] @TODO: (2017-05-16) fix about page
- [ ] @TODO: (2017-05-16) option to republish all in published column (e.g. where design changes)

## Breadcrumbs


# Notes

Rewrite with try/except blocks
Think about unit tests
Think about class structure

# Log

## 2017-05-15
Up and runnning
Moving code into blog

## 2017-05-13
Setting up a blog
https://mmistakes.github.io/so-simple-theme/theme-setup/#installation
Configure the `_config.yml` file
Switch of the




### get the blog working locally
brew install ruby
switch to a new terminal window (to force mac os to use the new ruby)
gem install bundler



## 2017-05-12
`pip install trello`
but trello api doesn't work, ?python2 issue with urllib
instead try py-trello, seems to be more recently updated
`pip install py-trello`
done
so can access board and pull in cards

install biopython and use Entrez submodule

blog theme
https://heiswayi.nrird.com/thinkspace/

Much credit to https://github.com/jtpio/trello-full-backup
Used this as inspiration for building script and getting my hands dirty with the Trello API
