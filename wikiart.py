import os
import json
import urllib
from paintings import Painting


WIKIART_PATH = 'datasets'
META_PATH = os.path.join(WIKIART_PATH, 'meta')
TMP_IMG_PATH = os.path.join(WIKIART_PATH, 'tmp.png')


def list_artists():
    return list(map(lambda x: x.rstrip('.json'), os.listdir(META_PATH)))


def load_artist_meta(artist_url):
    meta_path = os.path.join(META_PATH, f'{artist_url}.json')
    with open(meta_path) as f:
        meta_json = f.read()
    return json.loads(meta_json)


def load_painting(meta, url=None):
    title = meta['title']
    content_id = meta['contentId']
    artist_url = meta['artistUrl']
    year = meta['completitionYear']
    yearString = 'unknown-year' if year is None else str(year)
    try:
        urllib.request.urlretrieve(meta['image'] if url is None else url, TMP_IMG_PATH)
    except:
        return None
    return Painting(TMP_IMG_PATH, title, artist_url, year)


def load_artist(artist_url):
    result = []
    paintings = load_artist_meta(artist_url)
    for meta in paintings:
        print(f'Loading {meta["title"]}')
        painting = load_painting(meta)
        if painting is None:
            print('Failed')
        else:
            result.append(painting)
    return result


def find_by_title(painting_list, title):
    filtered = list(filter(lambda x: x.title == title, painting_list))
    return filtered[0] if filtered else None


def list_artist(artist_url):
    paintings = load_artist_meta(artist_url)
    return [meta['title'] for meta in paintings]


def load_painting_by_title(artist, title, url=None):
    paintings = load_artist_meta(artist)
    for meta in paintings:
        if meta['title'] == title:
            return load_painting(meta, url)
    return None
