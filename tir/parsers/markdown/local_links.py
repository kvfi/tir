import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import LinkInlineProcessor

from tir.utils import get_domain


class LocalLinksProcessor(LinkInlineProcessor):
    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))

        if not handled:
            return None, None, None

        href, title, index, handled = self.getLink(data, index)
        print(href)
        if not handled:
            return None, None, None

        el = etree.Element("a")
        el.text = text

        el.set("href", href)

        icons = ['wikipedia']
        site_name = get_domain(href, include_ext=False)

        if site_name in icons:
            el.set('class', 'icon ' + site_name)

        if site_name in ['ouafi', '']:
            el.set('class', 'icon internal')

        if title is not None:
            el.set("title", title)

        return el, m.start(0), index


class LocalLinksExtension(Extension):

    def extendMarkdown(self, md):
        md.inlinePatterns.register(LocalLinksProcessor(r'\[.*?\]', md), 'local_link', 1)
