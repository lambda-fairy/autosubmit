#!/usr/bin/env python3

from contextlib import contextmanager
import datetime
import json
import os
import random
import praw
import sys
import time


USER_AGENT = 'Automatic submitter script for /u/lfairy'

FILE = 'queue.json'

LIMIT = 5


def output(*args, **kwds):
    now = datetime.datetime.utcnow().replace(microsecond=0)
    print('[{}]'.format(now.isoformat()), *args, **kwds)
    sys.stdout.flush()


def no_pics_thursday():
    """
    Return True if it's No Pics Thursday today.

    NPT happens every second week on Thursday. All image posts are
    banned on that day.
    """

    return datetime.date.today().toordinal() % 14 == 4


class Queue:
    def __init__(self, r, data):
        self.r = r
        self.data = data

    @classmethod
    @contextmanager
    def from_file(cls, r, filename):
        with open(filename) as f:
            self = cls(r, json.load(f))
        yield self
        with open(filename+'.new', 'w') as f:
            json.dump(self.data, f)
        os.rename(filename+'.new', filename)

    def __bool__(self):
        return bool(self.data)

    def __len__(self):
        return len(self.data)

    def choose(self):
        """Pick a random link from the queue."""
        return random.choice(list(self.data.items()))

    def submit(self, url):
        """Submit a link chosen from the queue."""
        title = self.data[url]
        self.r.submit('mylittlepony', title, url=url, send_replies=True)

    def remove(self, url):
        """Remove a link from the queue."""
        del self.data[url]


def main():
    if no_pics_thursday():
        output("It's No-Pics Thursday today!")
        return

    r = praw.Reddit(user_agent=USER_AGENT)

    with Queue.from_file(r, FILE) as queue:
        if not queue:
            output('Nothing to post!')
            return

        output('Loaded {} entries; logging in'.format(len(queue)))
        r.login()

        count = 0
        first = True
        while queue and count < LIMIT:
            if first:
                first = False
            else:
                # One post every 16 minutes
                time.sleep(16 * 60)

            url, title = queue.choose()
            output('Submitting "{}" <{}>'.format(title, url))

            try:
                queue.submit(url)
            except praw.errors.AlreadySubmitted:
                queue.remove(url)
                output('Repost! Removing <{}>'.format(url))
            except praw.errors.RateLimitExceeded:
                output('ERROR: Too fast!')
            else:
                count += 1
                queue.remove(url)
                output('Posted <{}>'.format(url))

        output('Posted {} links; {} remaining'.format(count, len(queue)))


if __name__ == '__main__':
    main()
