#!/usr/bin/env python3
""
This script looks for buckets which contain a certain phrase.                                                                                                                                                                                                   
It prints the output in a file and on screen.
The filename is generated and contains the phrase.

Example:
$ python3 scrape_bucket.py "FBI SECRET FILES" 

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
        r = requests.get('https://buckets.grayhatwarfare.com/api/v1/buckets/0/100?access_token={}&keywords={}'.format(key,encoded_string))
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
    
    res = buckets['buckets_count']
    if int(res) == 0:
        print(f'Your search for "{string}" found no results\nNo file has been written')
        exit(0)

    FileNameTXT = utils.create_file_name(encoded_string, 'txt')
    print(f'Your search for "{string}" found {res} result(s).')
    with open(FileNameTXT, 'w') as writefile:
      for k in buckets['buckets']:
        writefile.write("Found bucket: {} with id: {}\n".format(k['bucket'], k['id']))
        print('Found bucket: "{}"  with id: "{}"\n'.format(k['bucket'],format(k['id'])))

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
