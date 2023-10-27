# find-imdb
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

imdbID = finder(title1, title2, ..., directors='director_name')
```
- To perform a direct search on your terminal:
```
python -m find_imdb
>>> Insert directors:
>>> Insert titles:
```
---

![usage](https://raw.githubusercontent.com/famgz/find-imdb/main/screenshots/usage.png)