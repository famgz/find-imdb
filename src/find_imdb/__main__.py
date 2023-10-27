# Execute with
# $ python -m find_imdb

from famgz_utils import print, input
from pathlib import Path
import sys

if __package__ is None:
    sys.path.insert(0, Path(__file__).resolve().parent.parent)

if __name__ == "__main__":
    from .main import finder

    titles = []
    directors = []

    for desc, stack in (('title', titles), ('director', directors)):
        while True:
            res = input(f'\nInsert a [bright_cyan]{desc} [white](or empty to proceed):\n>').strip()

            if not res:
                if stack:
                    print(f'{desc}s: [bright_blue]{", ".join(titles)}')
                    break
                print(f'[yellow]You must give at least one {desc}')
                continue

            stack.append(res)

    imdb_id = finder(*titles, directors=directors)
    print()
    if imdb_id:
        print(f'IMDb Id: [bright_green]{imdb_id}')
    else:
        print('Not found  :(')
