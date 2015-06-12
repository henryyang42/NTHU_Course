# -*- encoding: utf-8 -*-

from collections import defaultdict

import requests
import lxml.html


listing_url = (
    'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.6/JH626001.php'
)


class Any(list):
    def __repr__(self):
        return 'Any({})'.format(super(Any, self).__repr__())


class All(list):
    def __repr__(self):
        return 'All({})'.format(super(All, self).__repr__())


class Not(tuple):
    def __repr__(self):
        return 'Not{}'.format(super(Not, self).__repr__())


def extract_text(element):
    return ''.join(element.xpath('.//text()')).strip()


def extract_rows(element):
    return [o.strip() for o in element.xpath('.//text()')]


def get_document():
    r = requests.get(listing_url)
    r.encoding = 'cp950'
    return lxml.html.fromstring(r.text)


def iter_rows(document):
    trs = document.xpath('//tr[@valign="top"]')
    first = None

    for tr in trs:
        tds = tr.xpath('td')
        if len(tds) == 5:
            first, tds = tds[0], tds[1:]
        else:
            assert len(tds) == 4, len(tds)
        course = extract_text(first)
        requires = extract_rows(tds[0])
        scAnye = extract_rows(tds[1])
        note = extract_text(tds[2])
        object_ = extract_text(tds[3]).replace('&nbsp', '')
        assert len(requires) == len(scAnye), (course, requires, scAnye)
        yield course, requires, scAnye, note, object_


def get_prerequisites():
    result = defaultdict(All)
    for course, requires, scAnye, note, object_ in iter_rows(get_document()):
        target = result[course, object_]
        req_pairs = zip(requires, scAnye)
        if not note:
            target.extend(req_pairs)
        elif note == u'任選一科':
            target.append(Any(req_pairs))
        elif note == u'修過「先修科目」者，不可修「欲修科目」':
            target.extend(map(Not, req_pairs))
        else:
            assert False, 'unexpected note %r' % note
    return result


if __name__ == '__main__':
    import pprint
    pprint.pprint(get_prerequisites())
