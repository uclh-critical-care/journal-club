Aim: Build a static blog from a trello board that works for the journal club

# GTD

## Todos

- [x] @TODO: (2017-05-12) connect to a trello for publishing
- [x] @TODO: (2017-05-12) download cards from the publish list
- [ ] @TODO: (2017-05-13) add fields for reviewer and editor onto trello
- [ ] @TODO: (2017-05-12) parse description
- [ ] @TODO: (2017-05-12) parse the card as a class
- [x] @TODO: (2017-05-12) pull the associated pubmed data
- [x] @TODO: (2017-05-13) prep the jekyll site
- [x] @TODO: (2017-05-12) create a markdown file for a jekyll post
- [x] @TODO: (2017-05-13) use jinja as the templating engine
- [ ] @TODO: (2017-05-12) publish
- [ ] @TODO: (2017-05-13) authors override in so-simple theme, set up authors.yaml for each editor
- [ ] @TODO: (2017-05-13) add datascibc article to site
- [ ] @TODO: (2017-05-15) use labels as tags
- [ ] @TODO: (2017-05-15) use columns for publishing, after publishing move article
- [ ] @TODO: (2017-05-15) place comment on trello with link after publishing
- [ ] @TODO: (2017-05-15) delete old post if re-appears in to publish column

## Breadcrumbs

- [x] @CRUMB: (2017-05-13) sanitise text read for blog data.normalize, str.replace then prepare dictionary for post
- [ ] @CRUMB: (2017-05-13) combine card and pubmed data into yaml dump


Let's use hydrogen/jupyter to test this out
Interactive version with a jupyter notebook per task


# Log

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
