"""Scrape ragtime sheet music."""

from bs4 import BeautifulSoup
import os
import requests
import shutil

if not os.path.exists('sheet_music'):
    os.mkdir('sheet_music')

URL_FORMAT = 'http://www.ragsrag.com/pr/{0}'
soup = BeautifulSoup(
    requests.get(URL_FORMAT.format('pr.html')).content, 'html.parser')
tags = soup.findAll('a')
for tag in tags:
    path = tag.get('href')
    if path is not None and '.pdf' in path:
        print 'Downloading', path
        r = requests.get(URL_FORMAT.format(path), stream=True)
        if r.status_code == 200:
            outfile = os.path.join('sheet_music', path)
            with open(outfile, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            print 'Cannot find', path
