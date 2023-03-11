from bs4 import BeautifulSoup

from util import Util

class ProductsPage:
    def __init__(self, url, source) -> None:
        self.url = url
        self.source = source
        self.soup = BeautifulSoup(source, 'html.parser')
        self.util = Util()

    
    def scrap_products_urls(self):
        container_div = self.util.find_element_by_class(self.soup, 'div', 'test-articleDisplay css-1yuo7po')
        product_divs = self.util.find_elements_by_class(container_div, 'div', 'itemCardArea-cards test-card css-dhpxhu')
        product_urls = []
        for product_div in product_divs:
            a_tag = self.util.find_element_by_tag(product_div, 'a')
            href_path = self.util.get_href(a_tag)
            if href_path:
                product_urls.append(self.util.join_url_path(self.url, href_path))
        return product_urls
    
    def scrap_products_next_page_url(self):
        next_buttons = self.util.find_elements_by_class(self.soup, 'li', 'arrowButton test-arrowButton test-next next test-active-link css-1bwzh30')
        next_tag = self.util.find_element_by_tag(next_buttons[0], 'a') if len(next_buttons) > 0 else None
        href_path = self.util.get_href(next_tag)
        next_page_link = self.util.join_url_path(self.url, href_path)
        return next_page_link