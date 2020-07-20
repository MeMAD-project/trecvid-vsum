# Script for extracting Episodes data from the Eastenders fandom wiki
# Files "eastenders.collection.xml" and "eastenders.episodeDescriptions.xml" should be provided 
# (both downloadable from the challenge website)

# dependencies: Beautiful Soup (pip install bs4)

import time
import pickle 
import datetime
import requests
import urllib.request
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import xml.etree.ElementTree as xml

strptime = datetime.datetime.strptime

# mapping episode numbers to files
episodes_numbers = list(map(str, range(175, 185+1)))
videos_data      = xml.parse('eastenders.collection.xml').getroot().findall("./VideoFile")

episodes_filenames = {v.find('filename').text: v.find('id').text 
                      for v in videos_data
                      if v.find('id').text in episodes_numbers}

print('Episodes numbers:')
pprint(episodes_filenames)


episodes_urls            = {}
episodes_dates           = {}
episodes_descriptions    = {}
episodes_web_description = {}
episodes_characters      = {}


filepath = 'eastenders.episodeDescriptions.xml'
episodes = xml.parse(filepath).getroot().findall("./episode")

for episode in episodes:
    episode_url      = episode.find("./episodeUrl").text
    episode_date     = episode.find("./episodeDate").text
    episode_filename = episode.find("./episodeFile").text
    episode_description     = episode.find("./episodeDescription").text
    episode_web_description = episode.find("./episodeWebDescription").text
    episode_characters      = episode.find("./episodeCharacters").text
    
    if episode_filename in episodes_filenames:
        episodes_urls[episode_filename]            = episode_url
        episodes_dates[episode_filename]           = episode_date
        episodes_descriptions[episode_filename]    = episode_description
        episodes_web_description[episode_filename] = episode_web_description
        episodes_characters[episode_filename]      = episode_characters.split('; ')

        
filepath = 'eastenders.episodeDescriptions.xml'
episodes = xml.parse(filepath).getroot().findall("./episode")

print('Episodes dates:')
pprint(episodes_dates)

# Scraping episode data (dates for prev and next episodes) from the BBC website
"""
episodes_dates = {}
for filename, url in episodes_urls.items():
    page_content = bs(urlopen(url), 'html.parser')
    airing_date = page_content.find('span', {'class': 'broadcast-event__date'}).get_text()
    airing_date = strptime(airing_date, '%a %d %b %Y')
    episodes_dates[filename] = {'airing_date': airing_date}
    print(url, '---', filename)
    print()
    dates = page_content.find_all('a', {'class': 'block-link__target'})
    
    prev_date = dates[0].get_text()
    episodes_dates[filename]['prev_date'] = prev_date
    if not prev_date.startswith('P'):
        episodes_dates[filename]['prev_date'] = strptime(prev_date, '%d/%m/%Y')

    print(episodes_dates[filename]['prev_date'])
    print(episodes_dates[filename]['airing_date'])
"""


wiki_url = 'https://eastenders.fandom.com/wiki/2010'
page_content = bs(urlopen(wiki_url), 'html.parser')
earliest_date, latest_date = None, None

for filename, url in episodes_urls.items():
    page_content = bs(urlopen(url), 'html.parser')
    airing_date = page_content.find('span', {'class': 'broadcast-event__date'}).get_text()
    airing_date = strptime(airing_date, '%a %d %b %Y')

    if latest_date == None or earliest_date < airing_date:
        latest_date = airing_date 

    prev_date = page_content.find('a', {'class': 'block-link__target'}).get_text()
    try:
        prev_date = strptime(prev_date, '%d/%m/%Y')
        if earliest_date == None or earliest_date > prev_date:
            earliest_date = prev_date 
    except Exception as e:
        continue
        # print('Exception: ', str(e))

print("Earliest date:", earliest_date)
print("Latest date:", latest_date)

url = 'https://eastenders.fandom.com/wiki/2010'
page_content = bs(urlopen(url), 'html.parser')
table = page_content.find_all('table', {'class': 'sortable'})[1]

synopses = {}
credits = {}

for row in table.find_all('a', {'class': 'mw-redirect'} ):
    try:
        date = row.get_text()
        tdate = strptime(date, '%d %B %Y')
    except:
        continue # ignore links that don't contain dates
    
    if earliest_date < tdate < latest_date:
        # scraping synopsis
        synopses[date] = []
        article_url = 'https://eastenders.fandom.com' + row.get('href')
        page_content = bs(urlopen(article_url), 'html.parser')
        synopsis_title = page_content.find('h2', text='Synopsis')
        synopsis_paragraph = synopsis_title.find_next_sibling()
        while synopsis_paragraph.name == 'p':
            synopses[date].append(synopsis_paragraph.get_text())
            synopsis_paragraph = synopsis_paragraph.find_next_sibling()
        synopses[date] = ''.join(synopses[date])
        
        # scraping credits
        credits_title = page_content.find('h2', text='Credits')
        mapping = {}

        ttable = credits_title.find_next('table')
        if ttable:
            tds = [td.get_text().strip() for td in ttable.find_all('td')]
            roles = tds[::2]
            actors = tds[1::2]
            mapping = dict(zip(roles, actors))
        ulists = credits_title.find_all_next('ul')
        
        if ulists:
            for ulist in ulists: 
                for li in ulist.find_all('li'):
                    if ' - ' in li.get_text():
                        role, actor = li.get_text().split(' - ')
                        mapping[role.strip()] = actor.strip()
        
        credits[date] = mapping


# Packaging the final data
# Every episode takes the synopses and credits from the the previous week episodes
data = {}
for episode_filename in episodes_filenames:
    data[episode_filename] = {
        'url': episodes_urls[episode_filename], 
        'airing_date': episodes_dates[episode_filename]['airing_date'],
        # 'previous_airing': episodes_dates[episode_filename]['prev_date'],
        'episodes_descriptions': episodes_descriptions[episode_filename],
        'episodes_web_description': episodes_web_description[episode_filename],
        'characters': episodes_characters[episode_filename],
    }
    data[episode_filename]['summaries'] = [(date, synopses[date])
                                           for date in synopses
                                           if datetime.timedelta(days=0) <= 
                                              data[episode_filename]['airing_date'] - strptime(date, '%d %B %Y') < 
                                              datetime.timedelta(days=7)]
    data[episode_filename]['credits'] = [(date, credits[date])
                                           for date in credits
                                           if datetime.timedelta(days=0) <= 
                                              data[episode_filename]['airing_date'] - strptime(date, '%d %B %Y') < 
                                              datetime.timedelta(days=7)]

pickle.dump(data, open('episodes_data.pickle', 'wb'))