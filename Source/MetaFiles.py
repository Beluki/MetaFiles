# -*- coding: utf-8 -*-

"""
MetaFiles.
Like Flask-FlatPages or Flask-JSONPages, but reusable and library/markup agnostic.

The original Flask-FlatPages was written by Simon Sapin:
<https://github.com/SimonSapin/Flask-FlatPages>
"""


import itertools
import os


# IO utils:

def walk_filepaths(folder):
    """ Walk 'folder' recursively and return the path for each file found. """
    for root, dirs, files in os.walk(folder):
        for filename in files:
            yield os.path.join(root, filename)


# Data representation:

class MetaFile(object):
    """ Represents a file with separate metadata and body content. """

    def __init__(self, filepath, meta, body, meta_render, body_render):
        """
        Initialize a MetaFile instance.

          .filepath: filesystem path where this MetaFile was found.

          .meta: metadata content.
          .body: body content.

          .meta_render: metadata processor (e.g. 'yaml.load')
          .body_render: body processor (e.g. 'markdown.markdown')
        """
        self.filepath = filepath

        self._meta = meta
        self._body = body

        self._meta_rendered = False
        self._body_rendered = False

        self.meta_render = meta_render
        self.body_render = body_render

    @property
    def meta(self):
        """
        The metadata content, lazily rendered by the configured
        'meta_render' function.
        """
        if not self._meta_rendered:
            self._meta = self.meta_render(self._meta)
            self._meta_rendered = True

        return self._meta

    @property
    def body(self):
        """
        The body content, lazily rendered by the configured
        'body_render' function.
        """
        if not self._body_rendered:
            self._body = self.body_render(self._body)
            self._body_rendered = True

        return self._body

    def __repr__(self):
        """ Machine representation of this instance. """
        return '<MetaFile {!r}>'.format(self.filepath)


class MetaFiles(object):
    """ Represents a collection of MetaFile objects in the filesystem. """

    def __init__(self, root, extensions, encoding = 'utf-8-sig',
                                         meta_render = lambda x: x,
                                         body_render = lambda x: x):
        """
        Initialize a MetaFiles collection.

          .root: the path where the files are stored.

          .extensions: the file extensions that should be considered MetaFiles
                       as a string (one extension) or a tuple of strings (multiple).

          .encoding: what encoding to use when reading content.
          .meta_render: metadata processor (e.g. 'yaml.load')
          .body_render: body processor (e.g. 'markdown.markdown')

        By default, 'meta_render' and 'body_render' are an identity function.
        """
        self.root = root
        self.extensions = extensions
        self.encoding = encoding
        self.meta_render = meta_render
        self.body_render = body_render

        # dicts of { filepath: MetaFile } and { filepath: last modified }
        self._metafiles = {}
        self._mtimes = {}

    def split(self, string):
        """ Separate 'string' into meta and body parts. """

        # I prefer the Jekyll front matter format
        # but for compatibility keep the Flask-FlatPages one:

        lines = iter(string.split('\n'))

        meta = '\n'.join(itertools.takewhile(str.strip, lines))
        body = '\n'.join(lines)

        return meta, body

    def load_file(self, filepath):
        """ Read 'filepath' and return a MetaFile instance. """
        with open(filepath, encoding = self.encoding) as descriptor:
            content = descriptor.read()
            meta, body = self.split(content)

            return MetaFile(filepath, meta, body, self.meta_render, self.body_render)

    def load(self):
        """
        Traverse the root directory collecting MetaFiles.
        This method can be called multiple times to reload.
        On errors/exceptions the previous content is preserved.
        """
        metafiles = {}
        mtimes = {}

        for filepath in walk_filepaths(self.root):
            if filepath.endswith(self.extensions):
                mtime = os.path.getmtime(filepath)

                # see if it already exists and the mtime matches:
                if self._mtimes.get(filepath) == mtime:
                    metafile = self._metafiles[filepath]
                else:
                    metafile = self.load_file(filepath)

                metafiles[filepath] = metafile
                mtimes[filepath] = mtime

        self._metafiles = metafiles
        self._mtimes = mtimes

    def get(self, filepath, default = None):
        """ Returns the MetaFile at 'filepath' or 'default' on lookup error. """
        if filepath in self._metafiles:
            return self._metafiles[filepath]
        else:
            return default

    def __iter__(self):
        """ Iterate on all the MetaFile objects. """
        return iter(self._metafiles.values())

    def __repr__(self):
        """ Machine representation of this instance. """
        return '<MetaFiles {!r}>'.format(self.root)

