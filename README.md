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
