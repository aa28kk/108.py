import xml.etree.ElementTree as xml
tree = xml.parse(r"C:\Users\Ananya\Downloads\online_viewer_net.xml")
root = tree.getroot()
print(root.tag)
print(root.attrib)
print(root[0].tag)
print(root[1].tag)
print(root[0][1].tag)
print(root[0][1].text)
