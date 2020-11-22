from lxml import etree


def parse_xml(xml_file):
    dom = etree.parse(xml_file)
    root = dom.getroot()

    children = root.getchildren()
    print('# num of top level elements: {}'.format(len(children)))

    structure1_list = root.find('tabledefinitions')
    print(len(structure1_list))
    for structure1 in structure1_list:
        print(etree.iselement(structure1))
        print(structure1.tag)
        print(structure1)

    # structure
    for child in children[0]:
        print(child.tag, child.get('id'))
        foo = child.get('foo')
        print("foo: {}".format(foo))
        for elem in child.getchildren():
            if not elem.text:
                text = "None"
            else:
                text = elem.text
            print(elem.tag + " => " + text)


if __name__ == "__main__":
    parse_xml('../../data/simple.xml')
