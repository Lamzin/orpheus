# -*- coding: utf-8 -*-

import requests

from lxml import html


best_muzon_config = {
    'selectors': {
        'name': u'//span[contains(text(),"Песня")]/../text()',
        'author': u'//span[contains(text(),"Исполнитель:")]/../a/text()',
        'url_track': u'//div[@class="song_info_links"]/div[@class="song_info_link_2"]//a/@href'
    }
}

pesni_tut_config = {
    'selectors': {
        'name': u'//div[@class="song_info_block"]/b/a/text()',
        'author': u'//div[@class="song_info_block"]/b/text()',
        'url_track': u'//a[@class="download_song"]/@href'
    },
    'coding': u'cp1251'
}


class EmptyPage(Exception):
    pass


class Parser(object):

    MUSIC_DIRECTORY = u'/media/oleh/data/orpheus/'

    def __init__(self):
        self.parser = html.HTMLParser(encoding='utf-8')
        self.session = requests.session()

        self.selectors = best_muzon_config.get('selectors')
        self.coding = best_muzon_config.get('coding')

    def proceed(self, url):
        response = self.session.get(url, timeout=30)

        response.raise_for_status()

        content = response.content \
            if not self.coding else response.content.decode(self.coding)

        document = html.document_fromstring(content, parser=self.parser)

        result = {
            key: document.xpath(selector)[0].replace("'", "")
            for key, selector in self.selectors.iteritems()
        }

        for key, value in result.iteritems():
            if not value:
                raise EmptyPage()

        response = self.session.get(result['url_track'], timeout=60, stream=True)
        response.raise_for_status()

        result['url_disk'] = self.MUSIC_DIRECTORY + result['url_track'].split(u'/')[-1]

        with open(result['url_disk'], 'wb+') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        return result
