# JoeyTracker

REST API, hosted on Heroku, to track the Tufts Joey

`index.js` is used by Google Cloud Function through DialogFlow, to send a request to `app.py`

`app.py` responds with _unique_ `JSON` format to DialogFlow

TODO:

- write a better API that sends more proper responses
- `index.js` parses output from HTTP request-promise better
- `index.js` logic flow is better
- API logic flow is better
