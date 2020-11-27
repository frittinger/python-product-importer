from dataclasses import dataclass
from enum import Enum


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


StructureType = Enum('StructureType', '1 2 3')


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
        self.attributes = {}
        self.products = []
        # articles?
        self.children = []

    def __str__(self):
        return 'Structure: level {}, id={}'.format(self.level, self.id)
