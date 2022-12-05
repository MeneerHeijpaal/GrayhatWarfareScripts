#!/usr/bin/env python3
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! WORKS with Premium or Enterprise Only !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

This script looks for JPG's and PDF's in the supplied BucketID.

Example:
$ python3 get_img.py 1234

It is dependend on the following files, which are also in this repository:
- utils.py (for file-handling)
- settings.ini (for the API key)
"""

import configparser
import requests
import urllib.parse
import sys
import utils
import json

# Read Settings file
config = configparser.ConfigParser()
config.read('settings.ini')

# Read Key
key = config['API']['grayhat']

def scraper(bucket_id,key):
    try:
        r = requests.get('https://buckets.grayhatwarfare.com/api/v1/bucket/{}/files/0/100?access_token={}&keywords=jpg,pdf&full-path=1'.format(bucket_id,key))
    except requests.exceptions.Timeout:
        print("Time Out")
        # TODO
        # Maybe set up for a retry, or continue in a retry loop
    except requests.exceptions.TooManyRedirects:
        print("To many redirects")
        # TODO
        # Tell the user their URL was bad and try a different one
    except requests.exceptions.RequestException as e:
        print("Epic Fail")
        # Catastrophic error. bail.
        raise SystemExit(e)

    # Raise an error if the HTTP-request fails
    try: 
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code
        raise SystemExit(err)

    # Everything OK? Read the JSON data
    buckets = r.json()
    
    res = buckets['results']
    if int(res) == 0:
        print(f'Your search for "{format(bucket_id)}" found no results\nNo file has been written')
        exit(0)
    
    # If there are results, create a TXT File
    FileNameTXT = utils.create_file_name(bucket_id, 'txt')
    print(f'Your search for "{format(bucket_id)}" found {res} results.\nThe output is saved in: {FileNameTXT}')
    with open(FileNameTXT, 'w') as writefile:
        for k in buckets['files']:
            writefile.write('{}\n'.format(urllib.parse.quote(k['url'], safe=':/')))
    
def main(args):
    if len(sys.argv) !=2:
        print('Usage: %s <id of bucket>' %(sys.argv[0]))
        print('Eg: %s "7270" ' %(sys.argv[0]))
        sys.exit(0)
    SearchString = sys.argv[1]
    scraper(SearchString,key)

if __name__ == "__main__":
    main(sys.argv)
#_EOF
