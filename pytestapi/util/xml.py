from xml.etree.ElementTree import Element, tostring, fromstring

xml_doc = "<?xml version='1.1' encoding='UTF-8'?>"


def dict_to_xml_str(d):
    return xml_doc + tostring(dict_to_xml(d)).decode('utf-8')


def dict_to_xml(d):
    ele = None
    for k, v in d.items():
        ele = Element(k)
        if v.get("children"):
            for el in v.get("children"):
                ele.append(dict_to_xml(el))
        else:
            ele.text = v.get("text")
            ele.attrib = v.get("attrib")

    return ele


def xml_str_to_dict(xml_str):
    return xml_to_dict(fromstring(xml_str))


def xml_to_dict(ele):
    temp = {}
    if ele.text and len(ele.text.strip("\n").strip(" ")):
        temp.setdefault("text", ele.text.strip("\n").strip(" "))
    else:
        lis = [xml_to_dict(e) for e in ele]
        if lis:
            temp.setdefault("children", lis)

    if ele.attrib:
        temp.setdefault("attrib", ele.attrib)

    return {ele.tag: temp}
