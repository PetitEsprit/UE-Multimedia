import glob
import zipfile
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
import xml.dom.minidom

"""
os.listdir() -> list files

EXT_LINK
- word/_rels/document.xml.rels:
	<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
		<Relationship Id="rId1" ... Target="styles.xml"/>
		<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target=".../name.docx" TargetMode="External"/>
		<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>
		<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
	</Relationships>

	=> <Relationships> -> <Relationship> -> Type=http://schemas.openxmlformats.org/.../hyperlink Target="<name>.docx"

- word/document.xml:
	<w:hyperlink r:id="..."><...>Lien</...></w:hyperlink>
	textinstr(file1#id1 -> file2#id2/ ignore don't know it works)

INT_LINK
- word/document.xml:
	<w:bookmarkStart w:id="0" w:name="Marque-page_1"/>
	<w:hyperlink w:anchor="Marque-page_1"><...><w:t>Lien 3</w:t></...></w:hyperlink>

DocXml = rel file + doc file + parsed_data ()


link = [doc_name, link_id, link_text, link_target, link_target_mode]
"""

class DocXmlLink:
	def __init__(self, fname):
		self.links = []
		self.name = fname
		with zipfile.ZipFile(self.name, 'r') as archive:
			hlink_type = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
			doc_main = archive.read('word/document.xml')
			doc_rel = archive.read('word/_rels/document.xml.rels')
			DOMTree = xml.dom.minidom.parseString(doc_rel)
			rel = DOMTree.documentElement.getElementsByTagName("Relationship")
			for r in rel:
				if r.getAttribute("Type") ==  hlink_type:
					self.links.append([self.name, r.getAttribute("Id"),"",r.getAttribute("Target"), "External"])
			DOMTree = xml.dom.minidom.parseString(doc_main)
			rel = DOMTree.documentElement.getElementsByTagName("w:bookmarkStart")
			for r in rel:
				if r.getAttribute("w:name"):
					self.links.append([self.name, r.getAttribute("w:id"),"", r.getAttribute("w:name"), "Internal"])
			anchors = DOMTree.documentElement.getElementsByTagName("w:hyperlink")
			for a in anchors:
				i = 0
				for l in self.links:
					if (l[-1] == "External"  and a.getAttribute("r:id") == l[1]):
						l[2] = a.getElementsByTagName("w:t")[0].firstChild.nodeValue
						l[1] = "@" + str(i) #l[1]
					elif (l[-1] == "Internal" and a.getAttribute("w:anchor") == l[3]):
						l[2] = a.getElementsByTagName("w:t")[0].firstChild.nodeValue
						l[1] = "#" + str(i) #l[1]
						l[3] = "#" + l[3]
					i = i + 1
		self.anchors = []
		[self.anchors.append([l[1], l[2]]) for l in self.links]
		print(self.anchors)

def load_docs_in_folder():
	l = []
	for name in glob.glob('*.docx'):
		l.append(DocXmlLink(name))
	return l

def print_graph(DocxLinkList):
	graph = "digraph Links {\ncompound=true;\n"
	for d in DocxLinkList:
		subgraph = "subgraph \"cluster_" + d.name + "\" {\n"
		subgraph += "label = \"" + d.name + "\"\n"
		subgraph += "\"" + d.name + "\"[style=invis]\n"
		for a in d.anchors:
			subgraph += "\"" + d.name + a[0] + "\"[label=\"" + a[1] + "\"]\n"
		for l in d.links:
			if l[-1] == "Internal":
				subgraph += "\"" + d.name + l[1] + "\" -> \"" + d.name + l[3] + "\"\n"
		subgraph += "}\n"
		graph += subgraph
	for d in DocxLinkList:
		for l in d.links:
			if l[-1] == "External":
				graph += "\"" + d.name + l[1] + "\" -> \"" + l[3] + "\"[lhead=\"" + d.name + l[1] + "\"]\n"
	graph += "}"
	print(graph)

docs = load_docs_in_folder()
print_graph(docs)