
"""
The `find_job_titles` library finds mentions of job titles in strings.
In order to do so it compiles a search datastructure (Aho Corasick) and uses
    a precompiled list of >70k job titles as a reference list.
It returns the longest matching job title, including cross-overlapping matches,
    together with the start and end position in the given string.
TODO:
* also compare to https://github.com/scrapinghub/webstruct/blob/master/webstruct/utils.py#L155
"""

import logging
from collections import namedtuple

from acora import AcoraBuilder
import ahocorasick


Match = namedtuple('Match', ['start', 'end', 'match'])

# ----- #
# not sure if this must be done but for now lest do this
# It could be the case that this is preventing an error later on
import os
file_to_sort = 'job_titles/titles_combined.txt'
os.system('sort -o {} {}'.format(file_to_sort, file_to_sort))


def load_titles():
    """
    load job titles as generator from txt.gz file included in the library
    """

    with open('job_titles/titles_combined.txt') as f:
        for line in f:
            yield line.strip()


def longest_match(matches):
    """
    find respective longest matches from all overlapping aho corasick matches
    """
    longest = next(matches)
    if longest is None:
        return

    for elt in matches:
        # if (a contains b) or (b contains a)
        if (elt.start >= longest.start and elt.end <= longest.end) or \
           (longest.start >= elt.start and longest.end <= elt.end):
            longest = max(longest, elt, key=lambda x: x.end - x.start)
        else:
            yield longest
            longest = elt
    yield longest


def add_start(matches):
    """
    convert acora `(match, start)` tuples into `Match(start, end, match)` format
    """
    return (Match(start=start, end=start + len(match), match=match)
            for match, start in matches)


class BaseFinder(object):
    """
    Base class containing query methods
    """
    def findall(self, string, use_longest=True):
        """
        utility function returning `list` of results from `finditer`
        :param string: string to search target patterns in
        :param use_longest: if True only return longest matches,
                            else return all overlapping matches
        :returns: list of matches of type `Match`
        """
        return list(self.finditer(string, use_longest=use_longest))

    def finditer(self, string, use_longest=True):
        """
        iterator of all (longest) matches of target patterns in `string`
        :param string: string to search target patterns in
        :param use_longest: if True only return longest matches,
                            else return all overlapping matches
        :returns: generator of matches of type `Match`
        """
        if use_longest:
            return longest_match(self.find_raw(string))
        else:
            return self.find_raw(string)


# https://github.com/scoder/acora
class FinderAcora(BaseFinder):
    """
    Finder class based on "acora" library.
    Note: Building data structure seems to be significantly slower than with
          pyahocorasick
    """
    def __init__(self, use_unicode=True, ignore_case=False, titles=None):
        """
        :param use_unicode: whether to use `titles` as unicode or bytestrings
        :param ignore_case: if True ignore case in all matches
        :param titles: if given, overrides default `load_titles()` values
        """
        titles = titles if titles else load_titles()
        titles = (titles
                  if use_unicode
                  else (s.encode('ascii') for s in titles))
        builder = AcoraBuilder()
        logging.info('building job title searcher')
        builder.update(titles)
        self.ac = builder.build(ignore_case=ignore_case)
        logging.info('building done')

    def find_raw(self, string):
        """
        generator of raw, overlapping matches of all lengths from automaton
        """
        return add_start(self.ac.finditer(string))


class FinderPyaho(BaseFinder):
    """
    Finder class based on "pyahocorasick" library.
    TODO:
    - use pickle and unpickle support for `self.autom`
    """
    def __init__(self, titles=None):
        """
        :param titles: if given, overrides default `load_titles()` values
        """
        titles = titles if titles else load_titles()
        logging.info('building job title searcher')
        autom = ahocorasick.Automaton()
        for title in titles:
            autom.add_word(title, title)
        autom.make_automaton()
        self.autom = autom
        logging.info('building done')

    def find_raw(self, string):
        """
        generator of raw, overlapping matches of all lengths from automaton
        """
        for end, match in self.autom.iter(string):
            start = end - len(match) + 1
            yield Match(start=start, end=end, match=match)


Finder = FinderPyaho


# ------------------------- #


from helpers import get_domain_from_url
import re
import unicodedata


def get_job_titles(google_data):

    titles_parsed = {}
    finder = Finder()
    for item in google_data['items']:
        """
        TODO: try except is not good here. finadall fails sometimes for unknown reason with 
        RuntimeError: generator raised StopIteration. Have to investigate and fix this
        """
        try:
            job_titles = finder.findall(item['title'] + '. ' + item['snippet'])
            job_titles = [title.match for title in job_titles]

            if job_titles:
                job_titles = [re.sub(r'\W+', ' ', i.lower()) for i in job_titles]
                job_titles = [''.join((c for c in unicodedata.normalize('NFD', i) if unicodedata.category(c) != 'Mn')) for i in job_titles]
                source = get_domain_from_url(item['url'])
                for title in job_titles:
                    if titles_parsed.get(title):
                        titles_parsed[title]['count'] += 1
                        titles_parsed[title]['sources'].add(source)
                    else:
                        titles_parsed.update({title: {'count': 1, 'sources': {source}}})
        except RuntimeError:
            continue

    return titles_parsed
