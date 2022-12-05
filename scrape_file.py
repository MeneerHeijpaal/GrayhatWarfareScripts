#!/usr/bin/env python3
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! WORKS with Premium or Enterprise Only !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

This script looks for files in different buckets.

Example:
$ python3 scrape_file.py "FBI SECRET FILES"

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

def scraper(string,key):
    encoded_string = urllib.parse.quote(string)
    try:
        r = requests.get('https://buckets.grayhatwarfare.com/api/v1/files/{}/0/100?access_token={}&full-path=1'.format(encoded_string,key))
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
        print(f'Your search for "{string}" found no results\nNo file has been written')
        exit(0)
    
    # If there are results, create a TXT File
    FileNameTXT = utils.create_file_name(encoded_string, 'txt')
    print(f'Your search for "{string}" found {res} results.\nThe output is saved in: {FileNameTXT}')
    with open(FileNameTXT, 'w') as writefile:
        for k in buckets['files']:
            writefile.write('{}\n'.format(urllib.parse.quote(k['url'], safe=':/')))

    # If there are results, create a JSON File
    """     FileNameJSON = utils.create_file_name(encoded_string, 'json')
    with open(FileNameJSON, 'w') as writefile:
        writefile.write('{"files": [\n')
        for k in buckets['files']:
            writefile.write('{"url": ')
            json.dump(k['url'], writefile, ensure_ascii=False, indent="")
            writefile.write('},\n')
        writefile.write(']\n}') """

def main(args):
    if len(sys.argv) !=2:
        print('Usage: %s <string to search for>' %(sys.argv[0]))
        print('Eg: %s "FBI SECRET FILES" ' %(sys.argv[0]))
        sys.exit(0)
    SearchString = sys.argv[1]
    scraper(SearchString,key)

if __name__ == "__main__":
    main(sys.argv)
#_EOF
