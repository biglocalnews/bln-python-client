#!/usr/bin/env python3
from pprint import pprint
from time import sleep
import argparse
import json
import pickle
import sys

from seleniumwire import webdriver


def scrape(url, wait_secs):
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(wait_secs)
    posts = [
        r for r in driver.requests
        if r.method == 'POST' and r.headers.get('origin') ==
        'https://app.powerbigov.us' and 'queries' in json.loads(r.body)
    ]
    return [{
        'queries': json.loads(p.body)['queries'],
        'results': json.loads(p.response.body)['results']
    } for p in posts]


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog=argv[0],
        description='Microsoft Power BI Scraper',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('url')
    parser.add_argument('-w',
                        '--wait_secs',
                        help='number of seconds to wait for responses',
                        default=10)
    return parser.parse_args(argv[1:])


if __name__ == '__main__':
    args = parse_args(sys.argv)
    res = scrape(args.url, args.wait_secs)
    with open('res.pkl', 'wb') as f:
        pickle.dump(res, f)
