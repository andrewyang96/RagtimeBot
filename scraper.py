# From http://www.kunstderfuge.com/ragtime.htm

from bs4 import BeautifulSoup
import os
import requests
import shutil

URL = 'http://www.kunstderfuge.com/ragtime.htm'
AWS_URL_FORMAT = 'http://kunstderfuge.mid.s3.amazonaws.com/{0}'

if not os.path.exists('midis'):
    os.mkdir('midis')

soup = BeautifulSoup(requests.get(URL).content, 'html.parser')
tags = soup.findAll('a')
for tag in tags:
    link = tag.get('href')
    if link is not None and '.mid' in link:
        print 'Downloading', link
        path = link.split('=')[-1]
        filename = path.replace('/', '_')
        url = AWS_URL_FORMAT.format(path)
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            outfile = os.path.join('midis', filename)
            with open(outfile, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            print 'Cannot find', url
