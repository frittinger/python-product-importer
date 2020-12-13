from dataclasses import dataclass


@dataclass
class LanguageInfo:
    id: str
    short_cut: str
    short_name: str
    short_name_lowercase: str
    name: str


@dataclass
class PathInfo:
    picture_path: str
    picto_path: str


@dataclass
class LookupTable:
    id: str
    multi_select: bool
    items: dict


@dataclass
class TableItem:
    value: str
    sort_id: str
    short_name: str
    descriptions: dict


class Attribute:
    def __init__(self, key, key2, multilingual, has_relation, relation_key):
        self.key = key
        self.key2 = key2
        self.multilingual = multilingual
        self.has_relation = has_relation
        self.relation_key = relation_key

    @staticmethod
    def create_attribute_from_xml(element):
    # <attribute key='FreeB29' key2='2003' multilingual='0' hasRelation='1' realtionkey='100035'>
        attribute = Attribute(element.get('key'),
                              element.get('key2'),
                              element.get('multilingual'),
                              element.get('hasRelation'),
                              element.get('realtionkey'))
        values = {}
        for value in element.getchildren():
            values[value.get('languageId')] = value.text
        attribute.values = values
        return attribute

    def __str__(self):
        return 'Attribute: key {}, key2 {}, #values: {}'.\
            format(self.key, self.key2, len(self.values))


class Product:
    def __init__(self, id, item_number, sort_key, has_drawing, has_certificate, layout_variant):
        self.id = id
        self.item_number = item_number
        self.sort_key = sort_key
        self.has_drawing = has_drawing
        self.has_certificate = has_certificate
        self.layout_variant = layout_variant
        self.names = {}
        self.descriptions = {}
        self.attributes = []

    @staticmethod
    def create_product_from_xml(element):
        product = Product(element.get('id'),
                          element.get('itemNumber'),
                          element.get('sortkey'),
                          element.get('hasDrawing'),
                          element.get('hasCertificate'),
                          element.get('layoutVariant'))
        for child in element.getchildren():
            if child.tag == 'name':
                product.names[child.get('languageId')] = child.text
            elif child.tag == 'description':
                product.descriptions[child.get('languageId')] = child.text
            elif child.tag == 'attribute':
                product.attributes.append(Attribute.create_attribute_from_xml(child))
            else:
                print(child.tag)

        print('Product created: {}'.format(product))
        return product

    def __str__(self):
        return 'Product: id={}, names: {}, attr: {}'.\
            format(self.id, self.names, len(self.attributes))


