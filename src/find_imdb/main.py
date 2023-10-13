from difflib import SequenceMatcher
from famgz_utils import print, timeit
from imdb import Cinemagoer as IMDb
from time import sleep
from string import ascii_lowercase, digits
from unidecode import unidecode
from urllib.error import HTTPError

TRIES = 1
INTERVAL = 0.1
DEBUG = False
DIRECTORS_SEARCH_TOLERANCE = 2
MOVIES_SEARCH_TOLERANCE = 5
SIMILARITY_THRESHOLD = 0.9
allowed_chars = ascii_lowercase + digits + ' '
removed_title_words = ['the', 'that']


def dprint(*x):
    if not DEBUG:
        return
    for i in x:
        print(f'[bright_black]{i}', end=' ')
    print()


def is_similar_string(a, b):
    similarity = SequenceMatcher(None, a, b).ratio()
    return similarity >= SIMILARITY_THRESHOLD


def clean_string(s):
    s = unidecode(s)
    s = s.lower()
    s = ''.join([x for x in s if x in allowed_chars])
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s


def clean_title(s):
    s = clean_string(s)
    return ' '.join([x for x in s.split() if x not in removed_title_words])


def clean_names(names):
    # normalize people names and reduce to first name
    return sorted([clean_string(str(x)).split()[0] for x in names if x])  # reduces all clean names to its first name


@timeit
def main(*titles, directors=None, data: dict = None):

    def search_id_by_director():
        # Search by director name and compare titles
        dprint('\n>> search_id_by_director')
        for director in directors:
            dprint('director=', director)
            people = ia.search_person(director)[:DIRECTORS_SEARCH_TOLERANCE]
            for p in people:
                dprint('person=', p)
                person = ia.get_person(p.getID())
                filmography = person.get('filmography', {}).get('director')  # it only returns display titles
                if filmography:
                    for f in filmography:
                        dprint('film=', f)
                        film = clean_title(str(f))
                        dprint('cleaned film=', film)
                        if film in cleaned_titles:  # match title
                            ID = f.getID()
                            return 'tt' + ID
                sleep(INTERVAL)
        return None

    def search_id_by_title(movies):
        # Search by titles and compares by director's first name
        dprint('\n>> search_id_by_title')
        for m in movies[:MOVIES_SEARCH_TOLERANCE]:
            dprint('movie=', m)
            ID = m.getID()
            movie = ia.get_movie(ID)
            imdb_directors = movie.get('directors')
            dprint('imdb_directors=', imdb_directors)
            if imdb_directors:
                imdb_directors = clean_names(imdb_directors)
                dprint('cleaned imdb_directors=', imdb_directors)
                matches = [x for x in cleaned_directors if x in imdb_directors]  # match directors' first names
                dprint('matched directors=', matches)
                if matches:
                    return 'tt' + ID
            sleep(INTERVAL)
        return None

    titles = list(titles)

    # Parsing entries, if data
    if data and isinstance(data, dict):
        if data.get('directors'):
            directors = data['directors']
        if data.get('title_eng'):
            titles.append(data['title_eng'])
        if data.get('title'):
            titles.append(data['title'])
        if data.get('original_title'):
            titles.append(data['original_title'])

    assert directors, '[yellow]\[find_imdb] no director was given'
    assert titles, '[yellow]\[find_imdb] no title was given'

    if isinstance(directors, str):
        directors = [directors]

    # Simplifying data
    # directors = sorted([clean_string(x) for x in directors])[:SEARCH_TOLERANCE]  # To search_id_by_director()
    directors = sorted(directors)  # To search_id_by_director()
    cleaned_directors = clean_names(directors)  # To search_id_by_title() *person' first names

    titles = [x.replace("`", "'") for x in titles if x]  # ` causes search innacuracy
    cleaned_titles = [clean_title(x) for x in titles]

    # Starting
    ia = IMDb()
    print(f'[bright_black]\[find_imdb] Searching imdb id (titles={" ".join(titles)} | directors={" ".join(directors)} ...')

    dprint('parsed directors=', directors)
    dprint('cleaned parsed directors=', directors)
    dprint('parsed titles=', titles)
    dprint('cleaned parsed titles=', titles)

    # Search id by directors
    new_imdb_id = search_id_by_director()

    if new_imdb_id:
        return new_imdb_id

    # Search id by title
    for title in titles:
        # try `search_movie_advanced` (more accurate, less results)
        try:
            dprint('>> search_movie_advanced')
            movies = ia.search_movie_advanced(title)  # can raise error
        except (AttributeError, ValueError):
            pass
        else:
            new_imdb_id = search_id_by_title(movies)

        if new_imdb_id:
            return new_imdb_id

        # try regular `search_movie` (less accurate, more results)
        dprint('>> search_movie')
        movies = ia.search_movie(title)
        new_imdb_id = search_id_by_title(movies)

        if new_imdb_id:
            return new_imdb_id

    print(f'[bright_black]\[find_imdb] Not found: {" ".join(titles)}')


# def finder(title_eng=None, original_title=None, directors=None, data=None, debug=False):
def finder(*titles, directors=None, data=None, debug=False):
    global DEBUG
    DEBUG = debug

    new_imdb_id = main(*titles, directors=directors, data=data)
    return new_imdb_id

    # for _ in range(TRIES):
    #     try:
    #         new_imdb_id = main(*titles, directors=directors, data=data)
    #         return new_imdb_id
    #     except Exception as e:
    #         print(f'[find_imdb] Got Error:[yellow] {e} ')
    # return None
