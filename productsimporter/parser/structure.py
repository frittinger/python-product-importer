from productsimporter.parser.model import Product
from productsimporter.parser.attribute import Attribute


class Structure:
    """Structure resembles a product family in the ERP
    The hierarchy can be nested up to three levels deep, although this has no real meaning.
    Attributes or products can be attached at any level.
    Attributes are inherited, but this is handled by the ERP.
    """

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
        return 'Structure: level {}, id={}, children: {}, attr: {}'. \
            format(self.level, self.id, len(self.children), len(self.attributes))

    @staticmethod
    def create_structure_from_xml(element, level):
        structure = Structure(level)
        # <structure1 id='5' itemNumber='ZZ01000005' sortkey='101000' hasDrawing='0' hasCertificate='0' layoutVariant='200'>
        structure.id = element.get('id')
        structure.item_number = element.get('itemNumber')
        structure.sort_key = element.get('sortkey')
        structure.has_drawing = element.get('hasDrawing')
        structure.has_certificate = element.get('hasCertificate')
        structure.layout_variant = element.get('layoutVariant')
        children = element.getchildren()
        for child in children:
            if child.tag == 'structure2':
                child_struct = Structure.create_structure_from_xml(child, '2')
                structure.children.append(child_struct)
            elif child.tag == 'structure3':
                child_struct = Structure.create_structure_from_xml(child, '3')
                structure.children.append(child_struct)
            elif child.tag == 'structurename':
                structure.names[child.get('languageId')] = child.text
            elif child.tag == 'attribute':
                structure.attributes.append(Attribute.create_attribute_from_xml(child))
            elif child.tag == 'product':
                product = Product.create_product_from_xml(child)
                structure.products.append(product)
            else:
                print(child.tag)

        return structure

    def get_cloudsearch_doc(self, languages, lookup_tables):
        """Creates the cloudsearch document for this structure element"""
        attributes = {}
        attributes["number"] = self.item_number
        attributes["sortkey"] = self.sort_key
        attributes["type"] = "structure" + self.level
        attributes["layout_variant"] = self.layout_variant
        attributes["has_certificates"] = self.has_certificate
        attributes["has_drawing"] = self.has_drawing
        attributes["opacc_id"] = self.id

        # German is the fall back name if a language variant doesn't exist
        # If one is missing, take the German one, i.e. number 1
        # TODO how to define German as a constant?
        german_language_key = '1'
        german_text = self.names.get(german_language_key, 'no default text')
        for language_key in languages.keys():
            language_info = languages[language_key]
            attributes["name_" + language_info.short_name_lowercase] = \
                self.names.get(language_key, german_text)

        # get attributes
        for attribute in self.attributes:
            attributes.update(attribute.get_cloudsearch_attributes(languages, lookup_tables))

        return attributes

# number	ZZ03010009
# sortkey	105000
# name_de	Druckregler
# free_f3_2004_es	max 65° C
# free_e3_2004_value	1; 4; 5
# free_e1_2004_es	OEM Global
# free_e1_2004_value	1
# free_e3_2004_de	Sanitärarmaturen; Hoteleinsatz; Getränkeautomaten
# free_e1_2004_en	OEM Global
# type	structure1
# free_f4_2004_de	0.5 - 10 bar
# free_f3_2004_de	max. 65° C
# name_es	Regulador de presión
# free_f4_2004_value	0.5 - 10 bar
# layout_variant	200
# free_f3_2004_en	max 65° C
# name_en	Pressure regulator
# has_certificate	0
# free_e3_2004_es	Sanitary tap; Hotel application; Beverage machines
# opacc_id	9
# free_e3_2004_en	Sanitary tap; Hotel application; Beverage machines
# free_f3_2004_value	max. 65° C
# has_drawing	0
# free_e1_2004_de	OEM Global
