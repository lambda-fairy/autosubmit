#!/usr/bin/env python3

import praw

r = praw.Reddit('autosubmit login <https://github.com/lfairy/autosubmit>')
url = r.get_authorize_url('ducks', ['submit', 'identity'], True)

print('Go to this URL:')
print()
print('\t{}'.format(url))
print()

code = input('Click "authorize", then paste the code here: ')
access_information = r.get_access_information(code)

print('Thanks! Now add this line to your praw.ini:')
print()
print('\toauth_refresh_token: {}'.format(access_information['refresh_token']))
print()
