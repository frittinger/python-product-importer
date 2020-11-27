from lxml import etree
from productsimporter.parser.model import LanguageInfo, PathInfo, LookupTable, TableItem, Structure


def parse_xml(xml_file):
    dom = etree.parse(xml_file)
    root = dom.getroot()

# fetch language infos
    languages = {}
    language_info_list = root.find('languageInfo')
    for language in language_info_list:
        lang = LanguageInfo(language.get('id'),
                            language.get('shortCut'),
                            language.get('shortName'),
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
    lookup_tables = {}
    table_list = root.find('tabledefinitions')
    for table in table_list:
        items = {}
        for item in table.getchildren():
            descriptions = {}
            for desc in item.getchildren():
                descriptions[desc.get('languageId')] = desc.text
            table_item = TableItem(item.get('value'), item.get('sortId'), item.get('shortName'), descriptions)
            items[table_item.value] = table_item
        lookup_tables[table.get('id')] = LookupTable(table.get('id'), table.get('multiselect'), items)

    print(lookup_tables.keys())
    # print(lookup_tables['100002'])
    # print(lookup_tables['100002'].items['2'].short_name)
    # print(lookup_tables['100002'].items['2'].descriptions[languages['1'].id])

# structure
    structure1_list = root.find('structure')
    print(len(structure1_list))
    families = {}
    for structure1 in structure1_list:
        structure = create_family(structure1, '1')
        families[structure.id] = structure

    print(families.keys())
    print(families['14'])
    print(families['14'].names)
    for f in families['14'].children:
        print(f)


def create_family(in_structure, level):
    structure = Structure(level)
    # <structure1 id='5' itemNumber='ZZ01000005' sortkey='101000' hasDrawing='0' hasCertificate='0' layoutVariant='200'>
    structure.id = in_structure.get('id')
    structure.item_number = in_structure.get('itemNumber')
    structure.sort_key = in_structure.get('sortkey')
    structure.has_drawing = in_structure.get('hasDrawing')
    structure.has_certificate = in_structure.get('hasCertificate')
    structure.layout_variant = in_structure.get('layoutVariant')
    children = in_structure.getchildren()
    for child in children:
        if child.tag == 'structure2':
            child_struct = create_family(child, '2')
            structure.children.append(child_struct)
        elif child.tag == 'structure3':
            child_struct = create_family(child, '3')
            structure.children.append(child_struct)
        elif child.tag == 'structurename':
            structure.names[child.get('languageId')] = child.text
        # elif child.tag == 'attribute':
        #     # <attribute key='FreeB29' key2='2003' multilingual='0' hasRelation='1' realtionkey='100035'>
        # elif child.tag == 'product':
        else:
            print(child.tag)
    return structure


if __name__ == "__main__":
    parse_xml('../../data/simple.xml')
