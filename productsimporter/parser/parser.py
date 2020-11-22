import xmltodict


def handle_structure1(structure1):
    structure_names = structure1['structurename']
    if isinstance(structure_names, list):
        for name in structure_names:
            print(name['@languageId'])
            print(name['#text'])
    else:
        print(structure_names['@languageId'])
        print(structure_names['#text'])

    print(structure1.keys())
    # structure2 = structure1['structure2']
    # print(structure2)

    structure1_id = structure1['@id']
    item_number = structure1['@itemNumber']
    sort_key = structure1['@sortkey']
    has_drawing = structure1['@hasDrawing']
    has_certificate = structure1['@hasCertificate']
    layout_variant = structure1['@layoutVariant']
    print(structure1_id, item_number, sort_key)


with open('../../data/simple.xml') as fd:
    doc = xmltodict.parse(fd.read())
    structure1_list = doc['home']['structure']['structure1']
    print(len(structure1_list))
    for elem in structure1_list:
        handle_structure1(elem)
    # print(structure1_list.values())
    # print(structure1_list.items())


