# -*- coding: utf-8 -*-

from lxml import etree


def get_paging_xml(logger, items_number=None, total_pages=None, current_page=0, items_on_page=10,
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
            max_page = max(0, (items_number - 1) / items_on_page)
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

    start_page = max(0, current_page - paging_links_number / 2)

    end_page = start_page + paging_links_number - paging_links_number % 2
    if end_page > max_page:
        end_page = max_page
        start_page = max(0, end_page-paging_links_number)

    el_pager = etree.Element('pager')
    etree.SubElement(el_pager, 'previous', page=str(current_page-1), disabled=str(current_page == 0))

    if start_page > 0:
        etree.SubElement(el_pager, 'item', text='...', page=str(max(0, current_page-paging_links_number)))

    for i in xrange(start_page, end_page + 1):
        el = etree.SubElement(el_pager, 'item', text=str(i+1), page=str(i))
        if i == current_page:
            el.set('selected', 'true')

    if end_page < max_page:
        etree.SubElement(el_pager, 'item', text='...', page=str(min(max_page, current_page+paging_links_number)))

    etree.SubElement(el_pager, 'next', page=str(current_page+1), disabled=str(current_page == max_page))

    user_agent = user_agent.lower()
    if 'mac' in user_agent:
        os = 'Mac'
    elif 'linux' in user_agent:
        os = 'Linux'
    else:
        os = 'Win'

    etree.SubElement(el_pager, 'os').text = os

    return current_page, el_pager
