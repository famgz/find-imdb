from urllib.error import HTTPError
from imdb import Cinemagoer as IMDb
from time import sleep
from rich import print
from famgz_utils import clean_name, timeit

TRIES = 1
INTERVAL = 0  # + random()
SEARCH_TOLERANCE = 5


def normalize_strings(names):
    # normalize movie titles
    if isinstance(names, str):
        return clean_name(names, dot=False).lower()
    # normalize people names
    elif isinstance(names, list):
        first_names = sorted([normalize_strings(str(x)).split()[0] for x in names if x])  # reduces all clean names to its first name
        first_names.sort()
        return first_names


@timeit
def main(title_eng=None, original_title=None, directors=None, data:dict=None):

    def search_id_by_director():
        # Search by director name and compares by title_eng/original_title unidecode lower
        for director in directors_list:
            people = ia.search_person(director)
            for p in people:
                person = ia.get_person(p.getID())
                filmography = person.get('filmography', {}).get('director')
                if filmography:
                    for f in filmography:
                        film = normalize_strings(str(f))
                        if film in [normalize_strings(x) for x in titles]:  # match title
                            ID = f.getID()
                            return 'tt' + ID
                sleep(INTERVAL)
        return None

    def search_id_by_title(movies):
        # Search by title_eng/original_title and compares by director's first name unidecode lower
        if movies:
            for m in movies[:SEARCH_TOLERANCE]:
                ID = m.getID()
                movie = ia.get_movie(ID)
                imdb_directors = movie.get('directors')
                if imdb_directors:
                    imdb_directors = normalize_strings(imdb_directors)
                    matches = [x for x in directors if x in imdb_directors]  # match directors' first names
                    if matches:
                        return 'tt' + ID
                sleep(INTERVAL)
            return None

    # Parsing entries, if data
    if data:
        if isinstance(data, dict):
            if data.get('directors'):
                directors = data['directors']
            if data.get('title_eng'):
                title_eng = data['title_eng']
            elif data.get('title'):
                title_eng = data['title']
            if data.get('original_title'):
                original_title = data['original_title']

    assert directors, '[find_imdb] directors missing'
    assert title_eng or original_title, '[find_imdb] no title was given'

    if isinstance(directors, str):
        directors = [directors]

    # Treating data
    directors = sorted([clean_name(x, dot=False) for x in directors])[:SEARCH_TOLERANCE]
    directors_list = directors[:]  # To search_id_by_director()
    directors = normalize_strings(directors)  # To search_id_by_title() *person' first names

    titles = [x.replace("`", "'") for x in [title_eng, original_title] if x]

    # Starting
    ia = IMDb()
    print('[bright_black]\[find_imdb] Searching imdb id...', flush=True)

    # Search id by directors
    new_imdb_id = search_id_by_director()

    if new_imdb_id:
        return new_imdb_id

    # Search id by title
    for title in titles:
        # try `search_movie_advanced` (more accurate, less results)
        try:
            movies = ia.search_movie_advanced(title)
        except (AttributeError, ValueError):
            pass
        else:
            new_imdb_id = search_id_by_title(movies)

        if new_imdb_id:
            return new_imdb_id

        # try regular `search_movie` (less accurate, more results)
        movies = ia.search_movie(title)
        new_imdb_id = search_id_by_title(movies)

        if new_imdb_id:
            return new_imdb_id

    print(f'[bright_black]\[find_imdb] Not found: {title_eng} ({original_title})', flush=True)


def finder(title_eng=None, original_title=None, directors=None, data=None):
    for _ in range(TRIES):
        try:
            new_imdb_id = main(title_eng=title_eng, original_title=original_title, directors=directors, data=data)
            return new_imdb_id
        except Exception as e:
            print(f'[find_imdb] Got Error:[yellow] {e} ')
    return None


if __name__ == '__main__':
    ...
