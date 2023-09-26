# find_imdb
Find a film's IMDb Id from its title and director.

Installation
-----
```
pip install git+https://github.com/famgz/find-imdb.git
```

Usage
-----
- To use on your application:
```python
from find_imdb import finder

imdbID = finder([director1, director2, ...], title1, title2)
```
- To perform a direct search on your terminal:
```
python -m find_imdb
>>> Insert directors:
>>> Insert titles:
```
