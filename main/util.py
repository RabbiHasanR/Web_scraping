import requests

class Util:
    def __init__(self) -> None:
        pass

    def find_element_by_id(self, parent_element, tag_name, id):
        if parent_element:
            element = parent_element.find(tag_name, {"id": id})
            return element
        return None
    
    def find_element_by_class(self, parent_element, tag_name, class_name):
        if parent_element:
            element = parent_element.find(tag_name, class_=class_name)
            return element
        return None
    
    def find_element_by_tag(self, parent_element, tag_name):
        if parent_element:
            element = parent_element.find(tag_name)
            return element
        return None
    
    def find_elements_by_class(self, parent_element, tag_name, class_name):
        if parent_element:
            element = parent_element.find_all(tag_name, class_=class_name)
            return element
        return []
    
    def find_elements_by_tag(self, parent_element, tag_name):
        if parent_element:
            element = parent_element.find_all(tag_name)
            return element
        return []
    
    def get_text(self, element):
        if element:
            return str(element.get_text())
        return ''
    
    def get_attribute_value(self, element, attribute):
        if element and attribute:
            return element.get(attribute)
        return ''

    def get_src(self, element):
        if element:
            return element.get('src')
        return ''
    
    def get_href(self, element):
        if element:
            return element.get('href')
        return ''
    
    def join_url_path(self, url, path):
        return requests.compat.urljoin(url, path)