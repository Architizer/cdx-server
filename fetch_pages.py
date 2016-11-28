import gzip
import json
import requests
import argparse

parser = argparse.ArgumentParser(prog='fetch_pages.py')
parser.add_argument('--index', default='CC-MAIN-2016-44', help='domains help')
parser.add_argument('domains', nargs='+', help='domains help')
parser.print_help()

args = parser.parse_args()

if __name__ == "__main__":
    for domain in args.domains:
        try:
            from cStringIO import StringIO
        except:
            from StringIO import StringIO

        resp = requests.get('http://localhost:8888/{}-index?url={}/*&output=json'.format(args.index, domain))
        pages = [json.loads(x) for x in resp.content.strip().split('\n')]

        for page in pages:
            print page

            offset, length = int(page['offset']), int(page['length'])
            offset_end = offset + length - 1
            prefix = 'https://s3.amazonaws.com/commoncrawl/'
            resp = requests.get(prefix + page['filename'], headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})

            raw_data = StringIO(resp.content)
            f = gzip.GzipFile(fileobj=raw_data)

            data = f.read()
            warc, header, response = data.strip().split('\r\n\r\n', 2)

            print 'WARC headers'
            print '---'
            print warc
            print '---'
            print 'HTTP headers'
            print '---'
            print header
            print '---'
            print 'HTTP response'
            print '---'
            print response
