from bs4 import BeautifulSoup

from util import Util

class NavigationPage:

    def __init__(self, url, source) -> None:
        self.url = url
        self.source = source
        self.soup = BeautifulSoup(source, 'html.parser')
        self.util = Util()


    def scrap_navigation_links(self):
        ul = self.util.find_element_by_class(self.soup, 'ul', 'lpc-ukLocalNavigation_itemList js-animetionTarget')
        a_tags = self.util.find_elements_by_tag(ul, 'a')
        links = [self.util.join_url_path(self.url, self.util.get_href(a)) for a in a_tags]
        return links