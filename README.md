# autosubmit

1.  Set up pyvenv

        $ pyvenv-3.4 --without-pip env
        $ source env/bin/activate.fish
        $ curl https://bootstrap.pypa.io/get-pip.py | python3.4
        $ deactivate
        $ source env/bin/activate.fish

2.  Install dependencies

        $ pip3 install -r requirements.txt

3.  Hook up OAuth

        $ cat > praw.ini
        [reddit]
        domain: www.reddit.com
        oauth_client_id: ...
        oauth_client_secret: ...
        oauth_redirect_uri: ...
        ^D

        $ ./login.py

4. Add cron job

        $ sudo vi /etc/crontab

5. Party
