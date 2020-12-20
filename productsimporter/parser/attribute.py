NO_DEFAULT_TEXT = 'no default text'
GERMAN_LANGUAGE_KEY = '1'


class Attribute:
    """Class comment goes here ...
    XML representation of attributes:
    <attribute key='FreeB29' key2='2003' multilingual='0' hasRelation='1' realtionkey='100035'>
    """
    def __init__(self, key, key2, multilingual, has_relation, relation_key):
        self.key = key
        self.key2 = key2
        self.multilingual = multilingual
        self.has_relation = has_relation
        self.relation_key = relation_key
        self.values = {}

    @staticmethod
    def create_attribute_from_xml(element):
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

    def is_multilingual(self):
        return self.multilingual == '1'

    def get_cloudsearch_attributes(self, languages, lookup_tables):
        # free_a25_1001_en or free_e1_1001_value
        attributes = {}
        key_prefix = 'free_' + self.key[4:].lower() + '_' + self.key2.lower() + '_'

        # if this attribute has no lookup relation, just use the existing values
        if self.has_relation == '0':
            german_value = self.values.get(GERMAN_LANGUAGE_KEY, NO_DEFAULT_TEXT)
            attributes[key_prefix + 'value'] = german_value

            if self.is_multilingual():
                for language_key in languages.keys():
                    language_info = languages[language_key]
                    attributes[key_prefix + language_info.short_name_lowercase] = \
                        self.values.get(language_key, german_value)

        else:
            table = lookup_tables[self.relation_key]
            table_item = table.items[self.values[GERMAN_LANGUAGE_KEY]]
            german_value = table_item.descriptions[GERMAN_LANGUAGE_KEY]
            attributes[key_prefix + 'value'] = german_value

            # if multilingual than create the language variants, else only create the value
            if self.is_multilingual():
                for language_key in languages.keys():
                    language_info = languages[language_key]
                    attributes[key_prefix + language_info.short_name_lowercase] = \
                        table_item.descriptions.get(language_key, german_value)

        return attributes

    def __str__(self):
        return 'Attribute: key {}, key2 {}, #values: {}'. \
            format(self.key, self.key2, len(self.values))
