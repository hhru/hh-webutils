# coding=utf-8

import unittest

from hhwebutils import url_validator


class TestUrlValidator(unittest.TestCase):
    def test_invalid_characters(self):
        self.assertEqual(url_validator.validate(''), None)
        self.assertEqual(url_validator.validate('', 'filter'), None)
        self.assertEqual(url_validator.validate('', 'validate'), None)

        self.assertEqual(url_validator.validate('http://xfdf"dsy   a.ru'), 'http://xfdf"dsy   a.ru')
        self.assertEqual(url_validator.validate('http//fasdfsdf^&^&#.ru'), None)
        self.assertEqual(url_validator.validate('jav&#x0A;ascript:alert("XSS");'), None)
        self.assertEqual(url_validator.validate('http://h\th.ru'), None)
        self.assertEqual(url_validator.validate('javascript%3Aalert%28%22aa%22%29'), None)

        self.assertEqual(
            url_validator.validate(
                'http://&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;'
                '&#40;&#39;&#88;&#83;&#83;&#39;&#41;'
            ),
            'http://&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;'
            '&#40;&#39;&#88;&#83;&#83;&#39;&#41;'
        )

        self.assertEqual(
            url_validator.validate(
                'http://&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116'
                '&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083'
                '&#0000039&#0000041'
            ),
            'http://&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116'
            '&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083'
            '&#0000039&#0000041'
        )

        self.assertEqual(url_validator.validate('jav&#x09;ascript:alert("XSS");'), None)
        self.assertEqual(url_validator.validate('http://xfdf"dsy   a.ru', 'filter'), 'http://xfdf"dsy   a.ru')
        self.assertEqual(url_validator.validate('http//fasdfsdf^&^&#.ru', 'filter'), 'http://http//fasdfsdf^&^&#.ru')
        self.assertEqual(
            url_validator.validate('jav&#x0A;ascript:alert("XSS");', 'filter'), 'http://jav&#x0A;ascript:alert("XSS");'
        )

        self.assertEqual(url_validator.validate('http://h\th.ru', 'filter'), 'http://hh.ru')

        self.assertEqual(
            url_validator.validate('javascript%3Aalert%28%22aa%22%29', 'filter'),
            'http://javascript%3Aalert%28%22aa%22%29'
        )

        self.assertEqual(
            url_validator.validate(
                '&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;'
                '&#88;&#83;&#83;&#39;&#41;', 'filter'
            ),
            'http://&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;'
            '&#40;&#39;&#88;&#83;&#83;&#39;&#41;'
        )

        self.assertEqual(
            url_validator.validate(
                '&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058'
                '&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039'
                '&#0000041', 'filter'
            ),
            'http://&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116'
            '&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083'
            '&#0000039&#0000041'
        )

        self.assertEqual(
            url_validator.validate('jav&#x09;ascript:alert("XSS");', 'filter'), 'http://jav&#x09;ascript:alert("XSS");'
        )

    def test_invalid_scheme(self):
        self.assertEqual(url_validator.validate('ff.ru'), None)
        self.assertEqual(url_validator.validate('//ff.ru'), None)
        self.assertEqual(url_validator.validate('javascript:alert("XSS");'), None)
        self.assertEqual(url_validator.validate('data:sdfsdfff'), None)

        self.assertEqual(url_validator.validate('//ff.ru', 'validate'), 'http://ff.ru')
        self.assertEqual(url_validator.validate('http://www.ff.ru/dfd"fs', 'validate'), 'http://www.ff.ru/dfd"fs')
        self.assertEqual(url_validator.validate('javascript:alert(\'aa\');', 'validate'), 'http://alert(\'aa\');')
        self.assertEqual(
            url_validator.validate('javascript:alert(document.cookie);', 'validate'), 'http://alert(document.cookie);'
        )

        self.assertEqual(url_validator.validate('//ff.ru', 'filter'), 'http://ff.ru')
        self.assertEqual(url_validator.validate('ff.ru?a=10#fff', 'filter'), 'http://ff.ru?a=10#fff')
        self.assertEqual(url_validator.validate('/page1?a=10#fff', 'filter'), 'http://page1?a=10#fff')
        self.assertEqual(url_validator.validate('/page1/?a=10#fff', 'filter'), 'http://page1/?a=10#fff')
        self.assertEqual(url_validator.validate('/ff.ru', 'filter'), 'http://ff.ru')
        self.assertEqual(url_validator.validate(':/ff.ru', 'filter'), None)
        self.assertEqual(url_validator.validate('ttp:/ff.ru', 'filter'), 'http://ff.ru')
        self.assertEqual(url_validator.validate('ttp://ff.ru', 'filter'), 'http://ff.ru')
        self.assertEqual(url_validator.validate('ff.ru', 'filter'), 'http://ff.ru')
        self.assertEqual(
            url_validator.validate('javascript:alert(document.cookie);', 'filter'), 'http://alert(document.cookie);'
        )

    def test_invalid_path(self):
        self.assertEqual(url_validator.validate('hh.ru'), None)
        self.assertEqual(url_validator.validate('hh.ru', 'validate'), 'http://hh.ru')
        self.assertEqual(url_validator.validate('http://%68%68%2E%72%75/%6C%6F%67\t%6F%66%66%2E%64%6F'), None)
        self.assertEqual(url_validator.validate('http://%68%68%2E%72%75/%6C%6F%67%09%6F%66%66%2E%64%6F'), None)

        self.assertEqual(url_validator.validate('/logoff.do', 'validate'), 'http://logoff.do')
        self.assertEqual(url_validator.validate('http://hh.ru/l\togoff.do', 'validate'), None)
        self.assertEqual(url_validator.validate('www.hh.ru/l ogoff.do', 'filter'), 'http://www.hh.ru/l ogoff.do')
        self.assertEqual(url_validator.validate('?a=123', 'filter'), None)
        self.assertEqual(url_validator.validate('?logoff.do', 'filter'), None)

    def test_valid_url(self):
        self.assertEqual(url_validator.validate('http://hh.ru'), 'http://hh.ru')
        self.assertEqual(
            url_validator.validate('http://hh.ru/path/path?parma1=23&param2=выавыа#dd'),
            'http://hh.ru/path/path?parma1=23&param2=выавыа#dd'
        )

        self.assertEqual(url_validator.validate('http://пиши-код.рф?dsfd=вапвап'), 'http://пиши-код.рф?dsfd=вапвап')
        self.assertEqual(
            url_validator.validate(
                'http://www.proprofs.com/quiz-school/usercertificate.php?uname=%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0'
                '%D0%BD%D0%B4%D1%80%20%D0%9C%D1%8F%D1%81%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2'
            ),
            'http://www.proprofs.com/quiz-school/usercertificate.php?uname=%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0'
            '%D0%BD%D0%B4%D1%80%20%D0%9C%D1%8F%D1%81%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2'
        )

        self.assertEqual(
            url_validator.validate(
                u'http://www.proprofs.com/quiz-school/usercertificate.php?uname=%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0'
                u'%B0%D0%BD%D0%B4%D1%80%20%D0%9C%D1%8F%D1%81%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2'
            ),
            u'http://www.proprofs.com/quiz-school/usercertificate.php?uname=%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0'
            u'%D0%BD%D0%B4%D1%80%20%D0%9C%D1%8F%D1%81%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2'
        )

    def test_validate_backurl(self):
        permitted_hosts = ['hh.ru']

        permitted_app_schemes = ['app']

        def validate_backurl(url, fallback='/'):
            return url_validator.validate_backurl(
                url,
                permitted_hosts,
                permitted_app_schemes,
                fallback
            )

        self.assertEqual(validate_backurl(''), '/')
        self.assertEqual(validate_backurl(None), '/')
        self.assertEqual(validate_backurl(None), '/')
        self.assertEqual(validate_backurl('', None), None)
        self.assertEqual(validate_backurl(None, None), None)

        self.assertEqual(validate_backurl('data:sdfsdfff'), '/')
        self.assertEqual(validate_backurl('javascript:alert();//'), '/')
        self.assertEqual(validate_backurl('javascript:alert(document.cookie);'), '/')
        self.assertEqual(validate_backurl('javascripT://anything%0D%0A%0D%0Awindow.alert(document.cookie)'), '/')

        self.assertEqual(validate_backurl('myapp://applicant/resumes'), '/')

        self.assertEqual(validate_backurl('/ff.ru'), '/ff.ru')
        self.assertEqual(validate_backurl('ttp:/ff.ru'), '/')
        self.assertEqual(validate_backurl('ttp://ff.ru'), '/')

        self.assertEqual(validate_backurl('hh.ru'), 'hh.ru')
        self.assertEqual(validate_backurl('https://ya.ru'), '/')
        self.assertEqual(validate_backurl('https://ya.ru', None), None)
        self.assertEqual(validate_backurl('https://hh.ru'), 'https://hh.ru')
        self.assertEqual(validate_backurl('app://applicant/resumes'), 'app://applicant/resumes')

        self.assertEqual(
            validate_backurl('jav&#x0A;ascript:alert("XSS");'), 'jav&#x0A;ascript:alert("XSS");'
        )

        self.assertEqual(
            validate_backurl('path/to/something'),
            'path/to/something'
        )

        self.assertEqual(
            validate_backurl('/path/to/user/12345'),
            '/path/to/user/12345'
        )

        self.assertEqual(
            validate_backurl('https://hh.ru/path/to/something'),
            'https://hh.ru/path/to/something'
        )

        self.assertEqual(
            validate_backurl('/path?param1=value1&param2=value2'),
            '/path?param1=value1&param2=value2'
        )

        self.assertEqual(
            validate_backurl('/path/to/something#withhash'),
            '/path/to/something#withhash'
        )
