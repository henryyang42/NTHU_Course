'''
NTHU CCXP Decaptcha

Requires tesseract binary & lxml
'''

from __future__ import print_function

import logging
import subprocess
import tempfile
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import lxml.html
import requests


logger = logging.getLogger(__name__)

captcha_url_base = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/mod/auth_img/auth_img.php'  # noqa


class DecaptchaFailure(Exception):
    pass


def tesseract(path):
    return subprocess.check_output([
        'tesseract',
        path, '-',
        '-psm', '8',
        '-c', 'tessedit_char_whitelist=0123456789', 'nobatch'
    ]).strip()


def tesseract_versions():
    return subprocess.check_output(
        ['tesseract', '--version'],
        stderr=subprocess.STDOUT
    )


def decaptcha_url(url):
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpimg:
        tmpimg.write(requests.get(url).content)
        tmpimg.flush()
        return tesseract(tmpimg.name).replace(b' ', b'')


def get_captcha_url(acixstore):
    return '%s?ACIXSTORE=%s' % (captcha_url_base, acixstore)


class Entrance(object):
    def __init__(
        self,
        form_url,
        form_action_url=None,
        page_encoding='cp950',
        captcha_length_hint=3
    ):
        self.form_url = form_url
        if form_action_url is None:
            self.form_action_url = None
        else:
            self.form_action_url = urljoin(form_url, form_action_url)
        self.page_encoding = page_encoding
        self.captcha_length_hint = captcha_length_hint

    def get_acixstore(self):
        response = requests.get(self.form_url)
        response.encoding = self.page_encoding
        document = lxml.html.fromstring(response.content)
        return document.xpath('//input[@name="ACIXSTORE"]')[0].value

    def guess_form_action_url(self):
        response = requests.get(self.form_url)
        response.encoding = self.page_encoding
        document = lxml.html.fromstring(response.text, base_url=self.form_url)
        element = document.xpath('//input[@type="submit"]')[0]
        while element is not None:
            element = element.getparent()
            if element.tag == 'form':
                return element.action
        raise DecaptchaFailure('Cannot guess form action url')

    def validate_by_post(self, acixstore, captcha):
        response = requests.post(
            self.form_action_url,
            data={
                'ACIXSTORE': acixstore,
                'auth_num': captcha,
            }
        )
        response.encoding = self.page_encoding
        if b'interrupted' in response.content:
            logger.info('%r: %r session is interrupted', acixstore, captcha)
            return False
        elif b'Wrong check code' in response.content:
            logger.info('%r: %r is simply incorrect', acixstore, captcha)
            return False
        else:
            # assume the code is correct if nothing indicates it's not
            logger.info('%r: %r is correct', acixstore, captcha)
            logger.debug('RESPOSE: %r', response.text)
            return True

    def validate(self, acixstore, captcha):
        if not captcha.isdigit():
            logger.info('%r: %r is not a number', acixstore, captcha)
            return False
        if (
            self.captcha_length_hint is not None and
            not len(captcha) == self.captcha_length_hint
        ):
            logger.info(
                '%r: %r does not have length == 3', acixstore, captcha)
            return False
        return self.validate_by_post(acixstore, captcha)

    def get_ticket(self, retries=32):
        logger.info('trying acixstore-captcha pair for %r', self.form_url)
        if self.form_action_url is None:
            self.form_action_url = self.guess_form_action_url()
            logger.info(
                'form_action_url not provided, assuming %r',
                self.form_action_url)
        for try_ in range(retries):
            acixstore = self.get_acixstore()
            captcha = decaptcha_url(get_captcha_url(acixstore))
            if self.validate(acixstore, captcha):
                return acixstore, captcha
        raise DecaptchaFailure('Cannot decaptcha for, retries=%i' % retries)


try:
    tesseract_versions()
except subprocess.CalledProcessError:
    raise ImportError('%r requires tesseract binary' % __name__)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Get a ticket of an acixstore-captcha pair to CCXP'
    )

    parser.add_argument(
        '--form-url',
        help='target form url',
        default='https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.9/JH629001.php',  # noqa
    )
    parser.add_argument(
        '--form-action-url',
        help='where to post to validate captcha (auto detect if not provided)',
        default=None
    )
    parser.add_argument(
        '--retires',
        help='max_retries',
        default=32,
        type=int
    )
    parser.add_argument(
        '--quiet',
        help='do not log',
        action='store_true'
    )

    args = parser.parse_args()

    if not args.quiet:
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())

    print(
        Entrance(
            args.form_url,
            args.form_action_url
        ).get_ticket(
            args.retires
        )
    )
