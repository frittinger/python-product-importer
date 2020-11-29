from dataclasses import dataclass


@dataclass
class LanguageInfo:
    id: str
    short_cut: str
    short_name: str
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

    def __str__(self):
        return 'Attribute: key {}, key2 {}'.format(self.key, self.key2)


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

    def __str__(self):
        return 'Product: id={}, names: {}, attr: {}'. \
            format(self.id, self.names, len(self.attributes))


class Structure:
    def __init__(self, level):
        self.level = level
        self.id = None
        self.item_number = None
        self.sort_key = None
        self.has_drawing = False
        self.has_certificate = False
        self.layout_variant = '200'
        self.names = {}
        self.attributes = []
        self.products = []
        # articles?
        self.children = []

    def __str__(self):
        return 'Structure: level {}, id={}, children: {}, attr: {}'.\
            format(self.level, self.id, len(self.children), len(self.attributes))
