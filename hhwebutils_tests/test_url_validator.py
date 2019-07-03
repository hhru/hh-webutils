# coding=utf-8

import unittest

from hhwebutils import url_validator


class TestUrlValidator(unittest.TestCase):
    def test_invalid_characters(self):
        self.assertEqual(url_validator.validate(''), None)
        self.assertEqual(url_validator.validate('', 'filter'), None)
        self.assertEqual(url_validator.validate('', 'validate'), None)

        self.assertEqual(url_validator.validate('http://xfdf"dsy   a.ru'), None)
        self.assertEqual(url_validator.validate('http//fasdfsdf^&^&#.ru'), None)
        self.assertEqual(url_validator.validate('jav&#x0A;ascript:alert("XSS");'), None)
        self.assertEqual(url_validator.validate('http://h\th.ru'), None)
        self.assertEqual(url_validator.validate('javascript%3Aalert%28%22aa%22%29'), None)

        self.assertEqual(
            url_validator.validate(
                'http://&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;'
                '&#40;&#39;&#88;&#83;&#83;&#39;&#41;.ru'
            ),
            None
        )

        self.assertEqual(
            url_validator.validate(
                'http://&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116'
                '&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083'
                '&#0000039&#0000041'
            ),
            None
        )

        self.assertEqual(url_validator.validate('jav&#x09;ascript:alert("XSS");'), None)
        self.assertEqual(url_validator.validate('http://xfdf"dsy   a.ru', 'filter'), 'http://xfdf"dsya.ru')
        self.assertEqual(url_validator.validate('http//fasdfsdf^&^&#.ru', 'filter'), None)
        self.assertEqual(
            url_validator.validate('jav&#x0A;ascript:alert("XSS");', 'filter'), None
        )

        self.assertEqual(url_validator.validate('http://h\th.ru', 'filter'), 'http://hh.ru')

        self.assertEqual(
            url_validator.validate('javascript%3Aalert%28%22aa%22%29', 'filter'), None
        )

        self.assertEqual(
            url_validator.validate(
                '&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;'
                '&#88;&#83;&#83;&#39;&#41;', 'filter'
            ),
            None
        )

        self.assertEqual(
            url_validator.validate('http://example.com; https://foo.bar^%#$^%#^#', 'filter'),
            'http://example.comhttps://foo.bar^%#$^%#^#'
        )

        self.assertEqual(
            url_validator.validate(
                '&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058'
                '&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039'
                '&#0000041', 'filter'
            ),
            None
        )

        self.assertEqual(
            url_validator.validate('jav&#x09;ascript:alert("XSS");', 'filter'), None
        )

    def test_invalid_host(self):
        self.assertEqual(url_validator.validate('hhru'), None)
        self.assertEqual(url_validator.validate('hhru', 'validate'), None)
        self.assertEqual(url_validator.validate('hhru.', 'validate'), None)

    def test_invalid_scheme(self):
        self.assertEqual(url_validator.validate('ff.ru'), None)
        self.assertEqual(url_validator.validate('//ff.ru'), None)
        self.assertEqual(url_validator.validate('javascript:alert("XSS");'), None)
        self.assertEqual(url_validator.validate('data:sdfsdfff'), None)

        self.assertEqual(url_validator.validate('//ff.ru', 'validate'), 'http://ff.ru')
        self.assertEqual(url_validator.validate('http://www.ff.ru/dfd"fs', 'validate'), 'http://www.ff.ru/dfd"fs')
        self.assertEqual(url_validator.validate("javascript:alert('aa');", 'validate'), None)
        self.assertEqual(url_validator.validate('javascript:alert(document.cookie);', 'validate'), None)

        self.assertEqual(url_validator.validate('//ff.ru', 'filter'), 'http://ff.ru')
        self.assertEqual(url_validator.validate('ff.ru?a=10#fff', 'filter'), 'http://ff.ru?a=10#fff')
        self.assertEqual(url_validator.validate('/page1?a=10#fff', 'filter'), None)
        self.assertEqual(url_validator.validate('/ff.ru', 'filter'), 'http://ff.ru')
        self.assertEqual(url_validator.validate(':/ff.ru', 'filter'), None)
        self.assertEqual(url_validator.validate('ttp:/ff.ru', 'filter'), 'http://ff.ru')
        self.assertEqual(url_validator.validate('ttp://ff.ru', 'filter'), 'http://ff.ru')
        self.assertEqual(url_validator.validate('ff.ru', 'filter'), 'http://ff.ru')

    def test_invalid_path(self):
        self.assertEqual(url_validator.validate('hh.ru'), None)
        self.assertEqual(url_validator.validate('hh.ru', 'validate'), 'http://hh.ru')
        self.assertEqual(url_validator.validate('t.me', 'validate'), 'http://t.me')
        self.assertEqual(url_validator.validate('http://%68%68%2E%72%75/%6C%6F%67\t%6F%66%66%2E%64%6F'), None)
        self.assertEqual(url_validator.validate('http://%68%68%2E%72%75/%6C%6F%67%09%6F%66%66%2E%64%6F'), None)

        self.assertEqual(url_validator.validate('/logoff.do', 'validate'), 'http://logoff.do')
        self.assertEqual(url_validator.validate('http://hh.ru/l\togoff.do', 'validate'), None)
        self.assertEqual(url_validator.validate('www.hh.ru/l ogoff.do', 'filter'), 'http://www.hh.ru/logoff.do')
        self.assertEqual(url_validator.validate('?a=123', 'filter'), None)
        self.assertEqual(url_validator.validate('?logoff.do', 'filter'), None)

    def test_valid_url(self):
        self.assertEqual(url_validator.validate('hh.r', 'validate'), 'http://hh.r')
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
        # Falsy values
        self.assertEqual(validate_backurl(''), '/')
        self.assertEqual(validate_backurl(None), '/')
        self.assertEqual(validate_backurl(None), '/')
        self.assertEqual(validate_backurl('', None), None)
        self.assertEqual(validate_backurl(None, None), None)

        # invalid schemes
        self.assertEqual(validate_backurl('data:sdfsdfff'), '/')
        self.assertEqual(validate_backurl('javascript:alert();//'), '/')
        self.assertEqual(validate_backurl('javascript:alert(document.cookie);'), '/')
        self.assertEqual(validate_backurl('javascripT://anything%0D%0A%0D%0Awindow.alert(document.cookie)'), '/')
        self.assertEqual(validate_backurl('jav&#x0A;ascript:alert("XSS");'), '/')
        self.assertEqual(validate_backurl('myapp://applicant/resumes'), '/')

        # other
        self.assertEqual(validate_backurl('/ff.ru'), '/ff.ru')
        self.assertEqual(validate_backurl('ttp:/ff.ru'), '/')
        self.assertEqual(validate_backurl('ttp://ff.ru'), '/')
        self.assertEqual(validate_backurl('hh.ru'), '/')
        self.assertEqual(validate_backurl('https://ya.ru'), '/')
        self.assertEqual(validate_backurl('https://ya.ru', None), None)

        # scheme-relative urls:
        self.assertEqual(validate_backurl('//ff.ru'), '/')
        self.assertEqual(validate_backurl('%2F%2F/ff.ru'), '/')
        self.assertEqual(validate_backurl('/%2Fff.ru'), '/')
        self.assertEqual(validate_backurl('\\ff.ru'), '/')
        self.assertEqual(validate_backurl('\\\\ff.ru'), '/')
        self.assertEqual(validate_backurl('\\//ff.ru'), '/')
        self.assertEqual(validate_backurl('\/ff.ru'), '/')
        self.assertEqual(validate_backurl('\/\/ff.ru'), '/')
        self.assertEqual(validate_backurl('////ff.ru'), '/')
        self.assertEqual(validate_backurl('////ff.ru'), '/')
        self.assertEqual(validate_backurl('/////ff.ru'), '/')
        self.assertEqual(validate_backurl('\///ff.ru'), '/')
        self.assertEqual(validate_backurl('\////ff.ru'), '/')
        self.assertEqual(validate_backurl('///\;@ff.ru'), '/')

        # valid urls
        self.assertEqual(validate_backurl('https://hh.ru'), 'https://hh.ru')
        self.assertEqual(validate_backurl('app://applicant/resumes'), 'app://applicant/resumes')
        self.assertEqual(validate_backurl('/path/to/something'), '/path/to/something')
        self.assertEqual(validate_backurl('/path/to/user/12345'), '/path/to/user/12345')
        self.assertEqual(validate_backurl('https://hh.ru/path/to/something'), 'https://hh.ru/path/to/something')
        self.assertEqual(validate_backurl('/path?param1=value1&param2=value2'), '/path?param1=value1&param2=value2')
        self.assertEqual(validate_backurl('/path/to/something#withhash'), '/path/to/something#withhash')

        # payloads from
        # https://github.com/cujanovic/Open-Redirect-Payloads
        self.assertEqual(validate_backurl('//google.com/%2f..'), '/')
        self.assertEqual(validate_backurl('//www.hh.ru@google.com/%2f..'), '/')
        self.assertEqual(validate_backurl('///google.com/%2f..'), '/')
        self.assertEqual(validate_backurl('///www.hh.ru@google.com/%2f..'), '/')
        self.assertEqual(validate_backurl('////google.com/%2f..'), '/')
        self.assertEqual(validate_backurl('////www.hh.ru@google.com/%2f..'), '/')
        self.assertEqual(validate_backurl('https://google.com/%2f..'), '/')
        self.assertEqual(validate_backurl('https://www.hh.ru@google.com/%2f..'), '/')
        self.assertEqual(validate_backurl('/https://google.com/%2f..'), '/https://google.com/%2f..')
        self.assertEqual(
            validate_backurl('/https://www.hh.ru@google.com/%2f..'),
            '/https://www.hh.ru@google.com/%2f..'
        )
        self.assertEqual(validate_backurl('//google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('//www.hh.ru@google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('///google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('///www.hh.ru@google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('////google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('////www.hh.ru@google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('https://google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('https://www.hh.ru@google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('/https://google.com/%2f%2e%2e'), '/https://google.com/%2f%2e%2e')
        self.assertEqual(
            validate_backurl('/https://www.hh.ru@google.com/%2f%2e%2e'),
            '/https://www.hh.ru@google.com/%2f%2e%2e'
        )
        self.assertEqual(validate_backurl('//google.com/'), '/')
        self.assertEqual(validate_backurl('//www.hh.ru@google.com/'), '/')
        self.assertEqual(validate_backurl('///google.com/'), '/')
        self.assertEqual(validate_backurl('///www.hh.ru@google.com/'), '/')
        self.assertEqual(validate_backurl('////google.com/'), '/')
        self.assertEqual(validate_backurl('////www.hh.ru@google.com/'), '/')
        self.assertEqual(validate_backurl('https://google.com/'), '/')
        self.assertEqual(validate_backurl('https://www.hh.ru@google.com/'), '/')
        self.assertEqual(validate_backurl('/https://google.com/'), '/https://google.com/')
        self.assertEqual(validate_backurl('/https://www.hh.ru@google.com/'), '/https://www.hh.ru@google.com/')
        self.assertEqual(validate_backurl('//google.com//'), '/')
        self.assertEqual(validate_backurl('//www.hh.ru@google.com//'), '/')
        self.assertEqual(validate_backurl('///google.com//'), '/')
        self.assertEqual(validate_backurl('///www.hh.ru@google.com//'), '/')
        self.assertEqual(validate_backurl('////google.com//'), '/')
        self.assertEqual(validate_backurl('////www.hh.ru@google.com//'), '/')
        self.assertEqual(validate_backurl('https://google.com//'), '/')
        self.assertEqual(validate_backurl('https://www.hh.ru@google.com//'), '/')
        self.assertEqual(validate_backurl('//https://google.com//'), '/')
        self.assertEqual(validate_backurl('//https://www.hh.ru@google.com//'), '/')
        self.assertEqual(validate_backurl('//google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('//www.hh.ru@google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('///google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('///www.hh.ru@google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('////google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('////www.hh.ru@google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('https://google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('https://www.hh.ru@google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('//https://google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('//https://www.hh.ru@google.com/%2e%2e%2f'), '/')
        self.assertEqual(validate_backurl('///google.com/%2e%2e'), '/')
        self.assertEqual(validate_backurl('///www.hh.ru@google.com/%2e%2e'), '/')
        self.assertEqual(validate_backurl('////google.com/%2e%2e'), '/')
        self.assertEqual(validate_backurl('////www.hh.ru@google.com/%2e%2e'), '/')
        self.assertEqual(validate_backurl('https:///google.com/%2e%2e'), '/')
        self.assertEqual(validate_backurl('https:///www.hh.ru@google.com/%2e%2e'), '/')
        self.assertEqual(validate_backurl('//https:///google.com/%2e%2e'), '/')
        self.assertEqual(validate_backurl('//www.hh.ru@https:///google.com/%2e%2e'), '/')
        self.assertEqual(validate_backurl('/https://google.com/%2e%2e'), '/https://google.com/%2e%2e')
        self.assertEqual(
            validate_backurl('/https://www.hh.ru@google.com/%2e%2e'),
            '/https://www.hh.ru@google.com/%2e%2e'
        )
        self.assertEqual(validate_backurl('///google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('///www.hh.ru@google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('////google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('////www.hh.ru@google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('https:///google.com/%2f%2e%2e'), '/')
        self.assertEqual(validate_backurl('https:///www.hh.ru@google.com/%2f%2e%2e'), '/')
        self.assertEqual(
            validate_backurl('/https://google.com/%2f%2e%2e'),
            '/https://google.com/%2f%2e%2e'
        )
        self.assertEqual(
            validate_backurl('/https://www.hh.ru@google.com/%2f%2e%2e'),
            '/https://www.hh.ru@google.com/%2f%2e%2e'
        )
        self.assertEqual(validate_backurl('/https:///google.com/%2f%2e%2e'), '/https:///google.com/%2f%2e%2e')
        self.assertEqual(
            validate_backurl('/https:///www.hh.ru@google.com/%2f%2e%2e'),
            '/https:///www.hh.ru@google.com/%2f%2e%2e'
        )
        self.assertEqual(validate_backurl('/%09/google.com'), '/')
        self.assertEqual(validate_backurl('/%09/www.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('//%09/google.com'), '/')
        self.assertEqual(validate_backurl('//%09/www.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('///%09/google.com'), '/')
        self.assertEqual(validate_backurl('///%09/www.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('////%09/google.com'), '/')
        self.assertEqual(validate_backurl('////%09/www.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('https://%09/google.com'), '/')
        self.assertEqual(validate_backurl('https://%09/www.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('/%5cgoogle.com'), '/')
        self.assertEqual(validate_backurl('/%5cwww.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('//%5cgoogle.com'), '/')
        self.assertEqual(validate_backurl('//%5cwww.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('///%5cgoogle.com'), '/')
        self.assertEqual(validate_backurl('///%5cwww.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('////%5cgoogle.com'), '/')
        self.assertEqual(validate_backurl('////%5cwww.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('https://%5cgoogle.com'), '/')
        self.assertEqual(validate_backurl('https://%5cwww.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('/https://%5cgoogle.com'), '/https://%5cgoogle.com')
        self.assertEqual(validate_backurl('/https://%5cwww.hh.ru@google.com'), '/https://%5cwww.hh.ru@google.com')
        self.assertEqual(validate_backurl('https://google.com'), '/')
        self.assertEqual(validate_backurl('https://www.hh.ru@google.com'), '/')
        self.assertEqual(validate_backurl('javascript:123'), '/')
        self.assertEqual(validate_backurl('javascript:alert(1);'), '/')
        self.assertEqual(validate_backurl('javascript:alert(1)'), '/')
        self.assertEqual(validate_backurl('//javascript:alert(1);'), '/')
        self.assertEqual(validate_backurl('/javascript:alert(1);'), '/')
        self.assertEqual(validate_backurl('//javascript:alert(1)'), '/')
        self.assertEqual(validate_backurl('/javascript:alert(1)'), '/javascript:alert(1)')
        self.assertEqual(validate_backurl('/%5cjavascript:alert(1);'), '/')
        self.assertEqual(validate_backurl('/%5cjavascript:alert(1)'), '/')
        self.assertEqual(validate_backurl('//%5cjavascript:alert(1);'), '/')
        self.assertEqual(validate_backurl('//%5cjavascript:alert(1)'), '/')
        self.assertEqual(validate_backurl('/%09/javascript:alert(1);'), '/')
        self.assertEqual(validate_backurl('/%09/javascript:alert(1)'), '/')
        self.assertEqual(validate_backurl('java%0d%0ascript%0d%0a:alert(0)'), '/')
        self.assertEqual(validate_backurl('//google.com'), '/')
        self.assertEqual(validate_backurl('https:google.com'), '/')
        self.assertEqual(validate_backurl('//google%E3%80%82com'), '/')
        self.assertEqual(validate_backurl('\/\/google.com/'), '/')
        self.assertEqual(validate_backurl('/\/google.com/'), '/')
        self.assertEqual(validate_backurl('/\/google.com/'), '/')
        self.assertEqual(validate_backurl('\//google.com/'), '/')
        self.assertEqual(validate_backurl('http://google.com\\\\.www.hh.ru/'), '/')
        # //\/google.com/
        self.assertEqual(
            validate_backurl('/%2f%5c%2f%67%6f%6f%67%6c%65%2e%63%6f%6d/'), '/')
        self.assertEqual(validate_backurl('//google%00.com'), '/')
        self.assertEqual(
            validate_backurl('https://www.hh.ru/https://google.com/'),
            'https://www.hh.ru/https://google.com/'
        )
        self.assertEqual(validate_backurl('";alert(0);//'), '/')
        self.assertEqual(validate_backurl('javascript://www.hh.ru?%a0alert%281%29'), '/')
        self.assertEqual(validate_backurl('javascript://www.ff.ru?%a0alert%281%29'), '/')
        self.assertEqual(validate_backurl('http://0xd8.0x3a.0xd6.0xce'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@0xd8.0x3a.0xd6.0xce'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@0xd8.0x3a.0xd6.0xce'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@0xd8.0x3a.0xd6.0xce'), '/')
        self.assertEqual(validate_backurl('http://0xd83ad6ce'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@0xd83ad6ce'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@0xd83ad6ce'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@0xd83ad6ce'), '/')
        self.assertEqual(validate_backurl('http://3627734734'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@3627734734'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@3627734734'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@3627734734'), '/')
        self.assertEqual(validate_backurl('http://472.314.470.462'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@472.314.470.462'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@472.314.470.462'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@472.314.470.462'), '/')
        self.assertEqual(validate_backurl('http://0330.072.0326.0316'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@0330.072.0326.0316'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@0330.072.0326.0316'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@0330.072.0326.0316'), '/')
        self.assertEqual(validate_backurl('http://00330.00072.0000326.00000316'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@00330.00072.0000326.00000316'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@00330.00072.0000326.00000316'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@00330.00072.0000326.00000316'), '/')
        self.assertEqual(validate_backurl('http://[::216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@[::216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@[::216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@[::216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http://[::ffff:216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@[::ffff:216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@[::ffff:216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@[::ffff:216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http://0xd8.072.54990'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@0xd8.072.54990'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@0xd8.072.54990'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@0xd8.072.54990'), '/')
        self.assertEqual(validate_backurl('http://0xd8.3856078'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@0xd8.3856078'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@0xd8.3856078'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@0xd8.3856078'), '/')
        self.assertEqual(validate_backurl('http://00330.3856078'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@00330.3856078'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@00330.3856078'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@00330.3856078'), '/')
        self.assertEqual(validate_backurl('http://00330.0x3a.54990'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru@00330.0x3a.54990'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@00330.0x3a.54990'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@00330.0x3a.54990'), '/')
        self.assertEqual(validate_backurl('http:0xd8.0x3a.0xd6.0xce'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@0xd8.0x3a.0xd6.0xce'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@0xd8.0x3a.0xd6.0xce'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@0xd8.0x3a.0xd6.0xce'), '/')
        self.assertEqual(validate_backurl('http:0xd83ad6ce'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@0xd83ad6ce'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@0xd83ad6ce'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@0xd83ad6ce'), '/')
        self.assertEqual(validate_backurl('http:3627734734'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@3627734734'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@3627734734'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@3627734734'), '/')
        self.assertEqual(validate_backurl('http:472.314.470.462'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@472.314.470.462'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@472.314.470.462'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@472.314.470.462'), '/')
        self.assertEqual(validate_backurl('http:0330.072.0326.0316'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@0330.072.0326.0316'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@0330.072.0326.0316'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@0330.072.0326.0316'), '/')
        self.assertEqual(validate_backurl('http:00330.00072.0000326.00000316'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@00330.00072.0000326.00000316'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@00330.00072.0000326.00000316'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@00330.00072.0000326.00000316'), '/')
        self.assertEqual(validate_backurl('http:[::216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@[::216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@[::216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@[::216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http:[::ffff:216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@[::ffff:216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@[::ffff:216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@[::ffff:216.58.214.206]'), '/')
        self.assertEqual(validate_backurl('http:0xd8.072.54990'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@0xd8.072.54990'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@0xd8.072.54990'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@0xd8.072.54990'), '/')
        self.assertEqual(validate_backurl('http:0xd8.3856078'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@0xd8.3856078'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@0xd8.3856078'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@0xd8.3856078'), '/')
        self.assertEqual(validate_backurl('http:00330.3856078'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@00330.3856078'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@00330.3856078'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@00330.3856078'), '/')
        self.assertEqual(validate_backurl('http:00330.0x3a.54990'), '/')
        self.assertEqual(validate_backurl('http:www.hh.ru@00330.0x3a.54990'), '/')
        self.assertEqual(validate_backurl('http:3H6k7lIAiqjfNeN@00330.0x3a.54990'), '/')
        self.assertEqual(validate_backurl('http:XY>.7d8T\205pZM@00330.0x3a.54990'), '/')
        self.assertEqual(validate_backurl('〱google.com'), '/')
        self.assertEqual(validate_backurl('〵google.com'), '/')
        self.assertEqual(validate_backurl('ゝgoogle.com'), '/')
        self.assertEqual(validate_backurl('ーgoogle.com'), '/')
        self.assertEqual(validate_backurl('ｰgoogle.com'), '/')
        self.assertEqual(validate_backurl('/〱google.com'), '/〱google.com')
        self.assertEqual(validate_backurl('/〵google.com'), '/〵google.com')
        self.assertEqual(validate_backurl('/ゝgoogle.com'), '/ゝgoogle.com')
        self.assertEqual(validate_backurl('/ーgoogle.com'), '/ーgoogle.com')
        self.assertEqual(validate_backurl('/ｰgoogle.com'), '/ｰgoogle.com')
        self.assertEqual(validate_backurl('%68%74%74%70%3a%2f%2f%67%6f%6f%67%6c%65%2e%63%6f%6d'), '/')
        self.assertEqual(validate_backurl('http://%67%6f%6f%67%6c%65%2e%63%6f%6d'), '/')
        self.assertEqual(validate_backurl('<>javascript:alert(1);'), '/')
        self.assertEqual(validate_backurl('<>//google.com'), '/')
        self.assertEqual(validate_backurl('//google.com\@www.hh.ru'), '/')
        self.assertEqual(validate_backurl('https://:@google.com\@www.hh.ru'), '/')
        self.assertEqual(validate_backurl('\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x3aalert(1)'), '/')
        self.assertEqual(
            validate_backurl('\u006A\u0061\u0076\u0061\u0073\u0063\u0072\u0069\u0070\u0074\u003aalert(1)'),
            '/'
        )
        self.assertEqual(validate_backurl('ja\nva\tscript\r:alert(1)'), '/')
        self.assertEqual(validate_backurl('\j\av\a\s\cr\i\pt\:\a\l\ert\(1\)'), '/')
        self.assertEqual(validate_backurl('\152\141\166\141\163\143\162\151\160\164\072alert(1)'), '/')
        self.assertEqual(validate_backurl('http://google.com:80#@www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('http://google.com:80?@www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@www.hh.ru+@google.com/'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@www.hh.ru+@google.com/'), '/')
        self.assertEqual(validate_backurl('http://3H6k7lIAiqjfNeN@www.hh.ru@google.com/'), '/')
        self.assertEqual(validate_backurl('http://XY>.7d8T\205pZM@www.hh.ru@google.com/'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru+&@google.com#+@www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('http://google.com\twww.hh.ru/'), '/')
        self.assertEqual(validate_backurl('//google.com:80#@www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('//google.com:80?@www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('//3H6k7lIAiqjfNeN@www.hh.ru+@google.com/'), '/')
        self.assertEqual(validate_backurl('//XY>.7d8T\205pZM@www.hh.ru+@google.com/'), '/')
        self.assertEqual(validate_backurl('//3H6k7lIAiqjfNeN@www.hh.ru@google.com/'), '/')
        self.assertEqual(validate_backurl('//XY>.7d8T\205pZM@www.hh.ru@google.com/'), '/')
        self.assertEqual(validate_backurl('//www.hh.ru+&@google.com#+@www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('//google.com\twww.hh.ru/'), '/')
        self.assertEqual(validate_backurl('//;@google.com'), '/')
        self.assertEqual(validate_backurl('http://;@google.com'), '/')
        self.assertEqual(validate_backurl('@google.com'), '/')
        self.assertEqual(validate_backurl('javascript://https://www.hh.ru/?z=%0Aalert(1)'), '/')
        self.assertEqual(validate_backurl('data:text/html;base64,PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4='), '/')
        self.assertEqual(validate_backurl('http://google.com%2f%2f.www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('http://google.com%5c%5c.www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('http://google.com%3F.www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('http://google.com%23.www.hh.ru/'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru:80%40google.com/'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru%2egoogle.com/'), '/')
        self.assertEqual(validate_backurl('/x:1/:///%01javascript:alert(document.cookie)/'), '/')
        self.assertEqual(validate_backurl('/https:/%5cgoogle.com/'), '/https:/%5cgoogle.com/')
        self.assertEqual(validate_backurl('javascripT://anything%0D%0A%0D%0Awindow.alert(document.cookie)'), '/')
        self.assertEqual(validate_backurl('/http://google.com'), '/http://google.com')
        self.assertEqual(validate_backurl('/%2f%2fgoogle.com'), '/')
        self.assertEqual(validate_backurl('/google.com/%2f%2e%2e'), '/google.com/%2f%2e%2e')
        self.assertEqual(validate_backurl('/http:/google.com'), '/http:/google.com')
        self.assertEqual(validate_backurl('/.google.com'), '/.google.com')
        self.assertEqual(validate_backurl('///\;@google.com'), '/')
        self.assertEqual(validate_backurl('///google.com'), '/')
        self.assertEqual(validate_backurl('/////google.com/'), '/')
        self.assertEqual(validate_backurl('/////google.com'), '/')
        self.assertEqual(validate_backurl('java%0ascript:alert(1)'), '/')
        self.assertEqual(validate_backurl('java%09script:alert(1)'), '/')
        self.assertEqual(validate_backurl('java%0dscript:alert(1)'), '/')
        self.assertEqual(validate_backurl('javascript://%0aalert(1)'), '/')
        self.assertEqual(validate_backurl('//nothh.ru/'), '/')
        self.assertEqual(validate_backurl('http://nothh.ru/'), '/')
        self.assertEqual(validate_backurl('http://www.hh.ru.ru/'), '/')
