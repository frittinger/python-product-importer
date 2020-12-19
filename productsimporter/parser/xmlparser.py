from lxml import etree
from productsimporter.parser.model import LanguageInfo, PathInfo, LookupTable, TableItem
from productsimporter.parser.structure import Structure


def parse_xml(xml_file):
    root = etree.fromstring(xml_file)

# fetch language infos
    languages = {}
    language_info_list = root.find('languageInfo')
    for language in language_info_list:
        lang = LanguageInfo(language.get('id'),
                            language.get('shortCut'),
                            language.get('shortName'),
                            language.get('shortName').lower(),
                            language.get('name'))
        # which key do we need? id or shortName?
        languages[lang.id] = lang
    print(languages)

# fetch path infos
    paths = root.find('pathInfo')
    if len(paths) == 2:
        path_infos = PathInfo(paths[0].text, paths[1].text)
    else:
        raise AssertionError('path info missing')
    print(path_infos)

# table definitions
    table_list = root.find('tabledefinitions')
    lookup_tables = create_lookup_tables(table_list)
    print(lookup_tables.keys())
    print_lookup_table(lookup_tables, '100002')

# structure
    structure1_list = root.find('structure')
    print(len(structure1_list))
    families = {}
    for structure1 in structure1_list:
        structure = Structure.create_structure_from_xml(structure1, '1')
        families[structure.id] = structure

    print(families.keys())
    # fam = families['78']
    fam = families['5']
    print(fam)
    print(fam.get_cloudsearch_doc(languages))
    print(fam.names)
    for f in fam.children:
        print('1 {}'.format(f))
        if len(f.children) > 0:
            for ff in f.children:
                print('2 {}'.format(ff))


def create_lookup_tables(table_list):
    lookup_tables = {}
    for table in table_list:
        items = {}
        for item in table.getchildren():
            descriptions = {}
            for desc in item.getchildren():
                descriptions[desc.get('languageId')] = desc.text
            table_item = TableItem(item.get('value'), item.get('sortId'), item.get('shortName'), descriptions)
            items[table_item.value] = table_item
        lookup_tables[table.get('id')] = LookupTable(table.get('id'), table.get('multiselect'), items)
    return lookup_tables


def print_lookup_table(lookup_tables, table_id):
    table = lookup_tables[table_id]
    print('Table {}, {}'.format(table.id, table.multi_select))
    for key in table.items.keys():
        item = table.items[key]
        print(' Item({},{}/{})'.format(item.value, item.short_name, item.descriptions['1']))


if __name__ == "__main__":
    xml_string = bytes(open('../../data/simple.xml').read(), encoding="utf-8")
    parse_xml(xml_string)
