# coding=utf-8


from hhwebutils.device_detection import Device


EXPECTED_DEVICE_TYPE_AND_UA = [
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10A523'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10A551'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko)'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1'),
    (Device.ANDROID, 'Opera/9.80 (Android; Opera Mini/7.5.32193/28.3392; U; ru) Presto/2.8.119 Version/11.10'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; Android 4.0.3; HTC Sensation XE with Beats Audio Z715e Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10A403'),
    (None, 'Mozilla/5.0 (Symbian/3; Series60/5.3 NokiaN8-00/111.040.1511; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/535.1 (KHTML, like Gecko) NokiaBrowser/8.3.1.4 Mobile Safari/535.1 3gpp-gba'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10A525'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A551 Safari/8536.25'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 4.0.4; ru-ru; GT-I9100 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 2.3.5; ru-ru; HTC Desire S Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X; ru-ru) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/23.0.1271.100 Mobile/10A523 Safari/8536.25'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; ru-ru) AppleWebKit/533.17.9 (KHTML, like Gecko)'),
    (Device.WINDOWS_PHONE, 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 710)'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 2.3.5; ru-ru; HTC Wildfire S A510e Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
    (Device.WINDOWS_PHONE, 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 800)'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 4.0.4; ru-ru; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 2.3.6; ru-ru; GT-I8160 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 4.0.4; ru-ru; HTC Incredible S Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 4.1.2; ru-ru; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; ru-ru) AppleWebKit/533.17.9 (KHTML, like Gecko)'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko)'),
    (Device.ANDROID, 'Opera/9.80 (Android 4.0.3; Linux; Opera Mobi/ADR-1212030829) Presto/2.11.355 Version/12.10'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 4.0.3; ru-ru; HTC Sensation Z710e Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 4.0.4; ru-ru; GT-N7000 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
    (Device.ANDROID, 'Opera/9.80 (Android; Opera Mini/7.5.31657/28.3392; U; ru) Presto/2.8.119 Version/11.10'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 4.1.1; ru-ru; GT-I9300 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
    (None, 'Opera/9.80 (Series 60; Opera Mini/7.0.31380/28.3392; U; ru) Presto/2.8.119 Version/11.10'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A525 Safari/8536.25'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 2.2; nl-nl; Desire_A8181 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
    (Device.ANDROID, 'Opera/9.80 (Android; Opera Mini/7.0.29952/28.3392; U; ru) Presto/2.8.119 Version/11.10'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B206'),
    (Device.ANDROID, 'Opera/9.80 (Android; Opera Mini/6.5.27452/28.3392; U; ru) Presto/2.8.119 Version/11.10'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; Android 4.1.1; HTC One X Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 2.3.5; ru-ru; HTC_WildfireS_A510e Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 2.3.5; ru-ru; HTC Desire HD A9191 Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; Android 4.1.1; GT-I9300 Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 2.3.5; ru-ru; HTC_DesireS_S510e Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
    (Device.IOS, 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; ru-ru) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5'),
    (Device.ANDROID, 'Opera/9.80 (Android; Opera Mini/6.5.29194/28.3392; U; ru) Presto/2.8.119 Version/11.10'),
    (None, 'Mozilla/5.0 (Mobile; rv:26.0) Gecko/26.0 Firefox/26.0'),
    (Device.ANDROID, 'Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0'),
    (Device.ANDROID, 'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
    (Device.IOS, 'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26'),
    (None, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.45 Safari/537.36'),
    (None, 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00'),
    (None, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'),
    (None, 'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166'),
    (Device.WINDOWS_PHONE, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10A523 not_mobile_user_agentMozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; Microsoft; Lumia 435) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537')
]

EXPECTED_IOS_VERSIONS_AND_UA = [
    (6.0, 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10A551'),
    (10.0, 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1'),
    (11.0, 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1'),
    (5.1, 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10A551'),
    (10.3, 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1')
]
