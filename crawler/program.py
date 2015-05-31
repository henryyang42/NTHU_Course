from __future__ import absolute_import

import lxml.html
import requests

from crawler.decaptcha import Entrance


class ProgramCrawler(object):
    form_url = (
        'https://www.ccxp.nthu.edu.tw/'
        'ccxp/INQUIRE/JH/6/6.1/6.1.11/6.1.11.6/JH61b6001.php')
    form_action_url = (
        'https://www.ccxp.nthu.edu.tw/'
        'ccxp/INQUIRE/JH/6/6.1/6.1.11/6.1.11.6/JH61b6002.php')
    encoding = 'cp950'

    def __init__(self, ys, acixstore=None, captcha=None):
        self.ys = ys
        self._acixstore = acixstore
        self._captcha = captcha

    def update_keypair(self):
        self._acixstore, self._captcha = Entrance(
            self.form_url,
            self.form_action_url
        ).get_ticket()

    @property
    def acixstore(self):
        if self._acixstore is None:
            self.update_keypair()
        return self._acixstore

    @property
    def captcha(self):
        if self._captcha is None:
            self.update_keypair()
        return self._captcha

    def iget_targets(self):
        response = requests.get(self.form_url)
        response.encoding = self.encoding
        document = lxml.html.fromstring(response.text)
        for tr in document.xpath('/html/body/div/form/table[1]/tr'):
            classify = tr.xpath('td[1]/input')
            word = tr.xpath('td[2]')
            if len(classify) == len(word) == 1:
                yield classify[0].attrib['value'], word[0].text

    def get_targets(self):
        '''
        returns list of form_value - name pair:
        [('A', '(跨院系)奈米與光電半導體產業學分學程'),
         ('B', '(跨院系)生物產業技術學分學程'),
         ('C', '(跨院系)生物資訊學分學程'),
         ('CSP', '文化研究學程(台聯大跨校學程)'),
         ...]
        '''
        return list(self.iget_targets())

    def get_response_from_program(self, classify):
        response = requests.post(
            self.form_action_url,
            data={
                'YS': self.ys,
                'CLASSIFY': classify,
                'ACIXSTORE': self.acixstore,
                'auth_num': self.captcha
            }
        )
        response.encoding = self.encoding
        return response

    def get_courses_from_program(self, classify):
        '''
        returns courses of a program as a list:
        ['10410EE  335000', '10410EE  336000', '10410EE  432000', ...]
        '''
        document = lxml.html.fromstring(
            self.get_response_from_program(classify).content)
        return [
            td.text
            for td
            in document.xpath('//tr[@class="class3"]/td[1]')
        ]

    def ifetch_all(self):
        for classify, name in self.iget_targets():
            yield (classify, name), self.get_courses_from_program(classify)

    def fetch_all(self):
        '''
        returns list of ((classify, program_name), [course1, course2, ...])
        '''
        return list(self.ifetch_all())


if __name__ == '__main__':
    import pprint

    for pcpair in ProgramCrawler('104|10').ifetch_all():
        pprint.pprint(pcpair)
