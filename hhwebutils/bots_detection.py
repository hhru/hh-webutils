# coding=utf-8
import re

from hhwebutils import compat


SEARCH_BOTS_DESKTOP = {
    # ОСНОВНЫЕ
    'Mail.RU_Bot': r'Mail.RU_Bot/\d',
    'Mail.RU_Bot_Fast': 'Mail.RU_Bot/Fast/',
    'YandexAccessibilityBot': 'YandexAccessibilityBot/',
    'YandexAdNet': 'YandexAdNet/',
    'YandexAntivirus': 'YandexAntivirus/',
    'YandexBot': 'YandexBot/',
    'YandexBlogs': 'YandexBlogs/',
    'YandexCalendar': 'YandexCalendar/',
    'YandexCatalog': 'YandexCatalog/',
    'YandexDirect_2': 'YandexDirect/2',
    'YandexDirect_3': 'YandexDirect/3',
    'YandexDirectDyn': 'YandexDirectDyn/',
    'YandexFavicons': 'YandexFavicons/',
    'YaDirectFetcher': 'YaDirectFetcher/',
    'YandexImageResizer': 'YandexImageResizer/',
    'YandexImages': 'YandexImages/',
    'YandexMarket': 'YandexMarket/',
    'YandexMedia': 'YandexMedia/',
    'YandexMetrika': 'YandexMetrika/',
    'YandexNews': 'YandexNews/',
    'YandexNewslinks': 'YandexNewslinks',
    'YandexPagechecker': 'YandexPagechecker/',
    'YandexScreenshotBot': 'YandexScreenshotBot/',
    'YandexSitelinks': 'YandexSitelinks/',
    'YandexVertis': 'YandexVertis/',
    'YandexVideo': 'YandexVideo/',
    'YandexVideoParser': 'YandexVideoParser/',
    'YandexWebmaster': 'YandexWebmaster/',
    'YandexZakladki': 'YandexZakladki/',
    'Googlebot': 'Googlebot/',
    'Googlebot-Image': 'Googlebot-Image/',
    'Googlebot-News': 'Googlebot-News',
    'Googlebot-Video': 'Googlebot-Video/',
    'Google-Read-Aloud': 'Google-Read-Aloud',
    'Google-Favicon': 'Google Favicon',
    'Mediapartners': 'Mediapartners-Google/',
    'Mediapartners-Google': '^Mediapartners-Google$',
    'AdsBot-Google': 'AdsBot-Google',
    'FeedFetcher-Google': 'FeedFetcher-Google',
    'DuplexWeb-Google': 'DuplexWeb-Google/',
    # менее известные
    'Bingbot': 'bingbot/',
    'BingPreview': 'BingPreview',
    'Slurp': 'Slurp',
    'DuckDuckBot': 'DuckDuckBot',
    'Baiduspider': 'Baiduspider',
    'Konqueror': 'Konqueror',
    'Exabot': 'Exabot',
    'facebot': 'facebookexternalhit',
    'ia_archiver': 'ia_archiver/',
    'MJ12bot': 'MJ12bot',
    'SimplePie': 'SimplePie',
    'SiteLockSpider': 'SiteLockSpider',
    'OkHttp': 'okhttp/',
    'BLEXBot': 'BLEXBot/',
    'ScoutJet': 'ScoutJet'
}

SEARCH_BOTS_MOBILE = {
    'YandexMobileBot': 'YandexMobileBot/',
    'YandexMobileScreenShotBot': 'YandexMobileScreenShotBot/',
    'Googlebot-Smartphone': 'Nexus.*Googlebot',
    'AdsBot-Google-Mobile': 'AdsBot-Google-Mobile',
    'Googlebot-Mobile': 'Googlebot-Mobile/',
    'Mediapartners-Google_mobile': 'Mediapartners-Google/',
    'AdsBot-Google-Mobile-Apps': 'AdsBot-Google-Mobile-Apps',
}

SEARCH_BOTS = {
    bot_name: re.compile(pattern) for bot_name, pattern in compat.iteritems(
        {**SEARCH_BOTS_DESKTOP, **SEARCH_BOTS_MOBILE}
    )
}


def get_bot_name(user_agent):
    for bot_name, regexp in compat.iteritems(SEARCH_BOTS):
        if regexp.search(user_agent) is not None:
            return bot_name

    return None


def is_mobile_search_bot(search_bot_name):
    return search_bot_name in SEARCH_BOTS_MOBILE
