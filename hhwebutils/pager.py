# coding=utf-8

from lxml import etree


def get_paging_xml(logger, items_number=None, total_pages=None, current_page=0, items_on_page=10,
                   paging_links_number=5, user_agent=''):
    current_page, paging = get_paging(
        logger, items_number, total_pages, current_page, items_on_page, paging_links_number, user_agent
    )

    if paging is None:
        return current_page, paging

    el_pager = etree.Element('pager')
    etree.SubElement(
        el_pager, 'previous', page=str(paging['previous']['page']), disabled=str(paging['previous']['disabled']))

    if paging.get('firstPage') is not None:
        etree.SubElement(el_pager, 'firstPage', page=str(paging['firstPage']['page']))

    for item in paging.get('pages', []):
        el = etree.SubElement(el_pager, 'item', text=item['text'], page=str(item['page']))
        if item.get('selected'):
            el.set('selected', 'true')

    if paging.get('lastPage') is not None:
        etree.SubElement(el_pager, 'lastPage', page=str(paging['lastPage']['page']))

    if paging.get('next') is not None:
        etree.SubElement(el_pager, 'next', page=str(paging['next']['page']), disabled=str(paging['next']['disabled']))

    etree.SubElement(el_pager, 'os').text = paging['os']

    return current_page, el_pager


def get_paging(logger, items_number=None, total_pages=None, current_page=0, items_on_page=10,
               paging_links_number=10, user_agent=''):
    """
    :raise TypeError: if no one of `items_number` nor `total_pages` specified or specified both

    Other errors skipped with error log writen.
    """
    if (items_number is None) == (total_pages is None):
        raise TypeError('Only one of items_number or total_pages should be specified')

    try:
        current_page, items_on_page, paging_links_number = map(int, (current_page, items_on_page, paging_links_number))

        if items_on_page < 1:
            raise ValueError('Items_on_page must be greater then 0')

        if total_pages is not None:
            max_page = int(total_pages) - 1
        else:
            items_number = int(items_number)
            max_page = max(0, (items_number - 1) // items_on_page)
    except (TypeError, ValueError):
        logger.error(('Paging generator: Incorrect parameter type. Int or numeric string was expected, '
                      'items_on_page number must be greater then 0.'
                      'Got items_number: {0!r}, total_pages: {1!r} current_page: {2!r}, '
                      'items_on_page: {3!r}, paging_links_number: {4!r}').format(items_number, total_pages,
                                                                                 current_page, items_on_page,
                                                                                 paging_links_number))
        return None, None

    current_page = min(current_page, max_page)

    if max_page < 1:
        return current_page, None

    start_page = max(0, current_page - paging_links_number // 2)

    end_page = start_page + paging_links_number - paging_links_number % 2
    if end_page > max_page:
        end_page = max_page
        start_page = max(0, end_page - paging_links_number)

    pager = {
        'previous': {
            'page': current_page - 1,
            'disabled': current_page == 0,
        },
        'pages': []
    }

    def add_page(text, page, selected=False):
        pager['pages'].append({
            'text': text,
            'page': page,
            'selected': selected,
        })

    if start_page > 0:
        add_page('...', max(0, current_page - paging_links_number))

        pager['firstPage'] = {
            'page': 0
        }

    for i in range(start_page, end_page + 1):
        add_page(str(i + 1), i, i == current_page)

    if end_page < max_page:
        add_page('...', min(max_page, current_page + paging_links_number))

    if end_page == max_page - 1:
        add_page(str(max_page + 1), max_page)

    if end_page < max_page - 1:
        pager['lastPage'] = {
            'page': max_page,
            'selected': False,
        }

    pager['next'] = {
        'page': current_page + 1,
        'disabled': current_page == max_page,
    }

    user_agent = user_agent.lower()
    if 'mac' in user_agent:
        os = 'Mac'
    elif 'linux' in user_agent:
        os = 'Linux'
    else:
        os = 'Win'

    pager['os'] = os

    return current_page, pager
