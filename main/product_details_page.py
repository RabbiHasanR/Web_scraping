from bs4 import BeautifulSoup

from util import Util

class ProductDetailsPage:
    def __init__(self,url, source, cordinate_products) -> None:
        self.url = url
        self.source = source
        self.cordinate_products = cordinate_products
        self.soup = BeautifulSoup(source, 'html.parser')
        self.util = Util()


    def scrap_breadcrumb_category(self):
        ul = self.util.find_element_by_class(self.soup, 'ul', 'test-breadcrumb')
        lis = self.util.find_elements_by_tag(ul, 'li')
        categories = [self.util.get_text(self.util.find_element_by_tag(li, 'a')) for li in lis]
        return categories
    
    def scrap_product_images_urls(self):
        ul = self.util.find_element_by_class(self.soup, 'ul', 'slider-list test-slider-list')
        img_tags = self.util.find_elements_by_tag(ul, 'img')
        images_urls = [self.util.join_url_path(self.url, self.util.get_text(img_tag)) for img_tag in img_tags]
        return images_urls
    
    def scrap_product_info(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'articlePurchaseBox css-gxzada')
        category_name = self.util.get_text(self.util.find_element_by_class(div, 'span', 'categoryName test-categoryName'))
        product_name = self.util.get_text(self.util.find_element_by_class(div, 'h1', 'itemTitle test-itemTitle'))
        product_price = self.util.get_text(self.util.find_element_by_class(div, 'span', 'price-value test-price-value'))
        buttons = self.util.find_elements_by_class(div, 'button', 'sizeSelectorListItemButton')
        available_sizes = [self.util.get_text(button) for button in buttons]
        return {
            'category_name': category_name,
            'product_name': product_name,
            'product_price': product_price,
            'available_sizes': available_sizes
        }
    
    def scrap_description(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'js-componentsTabTarget js-articlePromotion add-close css-62zuw8')
        description_title = self.util.get_text(self.util.find_element_by_class(div, 'h4', 'heading itemFeature test-commentItem-subheading'))
        general_description = self.util.get_text(self.util.find_element_by_class(div, 'div', 'commentItem-mainText test-commentItem-mainText'))
        lis = self.util.find_elements_by_class(div, 'li', 'articleFeaturesItem')
        general_itemization_description = [self.util.get_text(li) for li in lis]

        return {
                'description_title': description_title,
                'general_description': general_description,
                'general_itemization_description': general_itemization_description
            }
    
    def scrap_size_chart(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'sizeChart test-sizeChart css-l7ym9o')
        tables = self.util.find_elements_by_class(div, 'table', 'sizeChartTable')
        table_length = len(tables)
        if table_length > 1:
            item_table = tables[0]
            item_table_ths = self.util.find_elements_by_class(item_table, 'th', 'sizeChartTHeaderCell test-combined_table_header')
            item_table_ths.pop(0)

            item_value_table = tables[1]
            item_value_trs = self.util.find_elements_by_class(item_value_table, 'tr', 'sizeChartTRow')
            size_names_tr = item_value_trs.pop(0)
            size_names_span = self.util.find_elements_by_tag(size_names_tr, 'span')
            size_names = [self.util.get_text(span) for span in size_names_span]

            size_chart = {}
            count = 0
            while count < len(item_table_ths) and count < len(item_value_trs):
                value = self.util.get_text(item_table_ths[count])
                values_span = self.util.find_elements_by_tag(item_value_trs[count], 'span')
                values = [self.util.get_text(span) for span in values_span]
                size_chart[value] = dict(zip(size_names, values))
                count += 1
            return size_chart
        return {}
    
    def scrap_special_function(self):
        special_functions = []
        divs = self.util.find_elements_by_class(self.soup, 'div', 'contents clearfix')
        for div in divs:
            page_link_div = self.util.find_element_by_class(div, 'div', 'item_part illustration')
            page_link = self.util.join_url_path(
                self.url,
                self.util.get_href(
                    self.util.find_element_by_tag(page_link_div, 'a')
                )
                
            )

            image_link = self.util.get_src(
                self.util.find_element_by_class(page_link_div, 'img', 'illustrationBody')
            )

            title = self.util.get_text(
                self.util.find_element_by_class(div, 'a', 'tecTextTitle')
            )

            description = self.util.get_text(
                self.util.find_element_by_class(div, 'div', 'item_part details')
            )
            special_functions.append(
                    {
                        'page_link': page_link,
                        'image_link': image_link,
                        'title': title,
                        'description': description
                    }
                )
        return special_functions


    def scrap_product_review_info(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'BVRRQuickTakeCustomWrapper')
        rating = self.util.get_text(
            self.util.find_element_by_class(div, 'span', 'BVRRNumber BVRRRatingNumber')
        )
        number_of_review = self.util.get_text(
            self.util.find_element_by_class(div, 'span', 'BVRRNumber BVRRBuyAgainTotal')
        )
        recommended_rate = self.util.get_text(
            self.util.find_element_by_class(div, 'span', 'BVRRBuyAgainPercentage')
        )

        img_tags = self.util.find_elements_by_class(div, 'img', 'BVImgOrSprite')
        items_sence = [self.util.get_attribute_value(img, 'title') for img in img_tags]

        return {
                'rating': rating,
                'number_of_review': number_of_review,
                'recommended_rate': recommended_rate,
                'items_sence': items_sence
            }
    
    def scrap_users_reviews(self):
        div = self.util.find_element_by_id(self.soup, 'div', 'BVRRDisplayContentBodyID')
        all_review_divs = self.util.find_elements_by_class(div, 'div', 'BVRRContentReview')
        user_reviews = []
        for review_div in all_review_divs:
            rating = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRNumber BVRRRatingNumber')
            )
            date = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRValue BVRRReviewDate')
            )
            title = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRValue BVRRReviewTitle')
            )
            description = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRReviewText')
            )
            reviewer_id = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRNickname')
            )

            user_review = {
                    'rating': rating,
                    'date': date,
                    'title': title,
                    'description': description,
                    'reviewer_id': reviewer_id
                }

            user_reviews.append(user_review)
        return user_reviews
    
    def scrap_keywords(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'test-category_link null css-vxqsdw')
        all_a = self.util.find_elements_by_class(div, 'a', 'css-1ka7r5v')
        keywords = [self.util.get_text(a) for a in all_a]
        return keywords
    

    def get_product_data(self):
        data = {}
        data['url'] = self.url
        data['breadcrumb_category'] = self.scrap_breadcrumb_category()
        data['product_images_urls'] = self.scrap_product_images_urls()
        data['product_info'] = self.scrap_product_info()
        data['cordinate_products'] = self.cordinate_products
        data['description'] = self.scrap_description()
        data['special_functions'] = self.scrap_special_function()
        data['size_chart'] = self.scrap_size_chart()
        data['review_info'] = self.scrap_product_review_info()
        data['user_reviews'] = self.scrap_users_reviews()
        data['keywords'] = self.scrap_keywords()

        return data