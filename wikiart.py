import os
import json
from paintings import Painting


WIKIART_PATH = 'datasets/wikiart-saved'
META_PATH = os.path.join(WIKIART_PATH, 'meta')
IMAGES_PATH = os.path.join(WIKIART_PATH, 'images')


def list_artists():
    return list(map(lambda x: x.rstrip('.json'), os.listdir(META_PATH)))


def load_artist_meta(artist_url):
    meta_path = os.path.join(META_PATH, f'{artist_url}.json')
    with open(meta_path) as f:
        meta_json = f.read()
    return json.loads(meta_json)


def load_painting(meta):
    title = meta['title']
    content_id = meta['contentId']
    artist_url = meta['artistUrl']
    year = meta['completitionYear']
    yearString = 'unknown-year' if year is None else str(year)
    path = os.path.join(IMAGES_PATH, artist_url, yearString, f'{content_id}.jpg')
    return Painting(path, title, artist_url, year)


def load_artist(artist_url):
    result = []
    paintings = load_artist_meta(artist_url)
    for meta in paintings:
        print(f'Loading {meta["title"]}')
        result.append(load_painting(meta))
    return result
