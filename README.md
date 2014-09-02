
## About

MetaFiles is a small Python 3 library that maintains a collection
of lazily cached static files with metadata and content, just like
[Flask-FlatPages][] and [Flask-JSONPages][] do for [Flask][].

The main difference is that MetaFiles is library agnostic. Both the
metadata and the body can be parsed with any library (YAML, JSON,
Markdown, Jinja2) and it's not tied to a Flask application. It can
be used with [Flask][], [Django][], [Bottle][] or any other framework.

Additionally, it's reusable, meaning you can create multiple instances
of MetaFiles for different folders using different parsers in a single
application.

[Bottle]: http://bottlepy.org
[Django]: https://www.djangoproject.com
[Flask]: http://flask.pocoo.org

[Flask-FlatPages]: https://pypi.python.org/pypi/Flask-FlatPages
[Flask-JSONPages]: https://pypi.python.org/pypi/Flask-JSONPages

## Installation and usage

MetaFiles is a single, small Python 3.3+ file with no dependencies other than
the Python 3 standard library. You can just include it in your projects
or install it using setuptools:

```bash
$ cd Source
$ python setup.py install
```

The usage is very similar to that of Flask-FlatPages. Instead of using
the Flask application configuration, the options are specified when creating
the MetaFiles instance:

```python
from MetaFiles import MetaFiles

# We will be using Markdown as markup
# and YAML as the metadata parser:
import markdown
import yaml

posts = MetaFiles(
    root = 'posts',
    extensions = ('.md', '.markdown'),
    encoding = 'utf-8-sig',
    meta_render = yaml.load,
    body_render = markdown.markdown
)

# Load all posts.
# Can be called multiple times to reload.
# Preserves previous content in case of an error/exception.
posts.load()

# Print the post titles (assuming a title key in the metadata):
for post in posts:
    print(post.meta['title'])
```

## Portability

MetaFiles is tested on Windows 7 and 8 and on Debian (both x86 and x86-64)
using Python 3.3+. Older versions are not supported.

## Status

This program is finished!

MetaFiles is feature-complete and has no known bugs. Unless issues are reported
I plan no further development on it other than maintenance.

## License

Like all my hobby projects, this is Free Software. See the [Documentation][]
folder for more information. No warranty though. Because it's based on the
work of Simon Sapin in Flask-FlatPages it uses the same license.

[Documentation]: https://github.com/Beluki/MetaFiles/tree/master/Documentation

