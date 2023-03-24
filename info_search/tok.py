import json
import os
from typing import Dict, List

Doc = Dict

DATABASE_PATH = "./.db"

"""class Token:
	def __init__(self, content, count=1):
		self.content = content
		self.count = count
	def __str__(self):
		return f"({self.content}: {self.count})"
	def __repr__(self):
   		return self.__str__()
"""

seps = ['\n', '\t', '\v', '\f', '\r', ' ', #spaces
		'.', ',',';', ":", '!', '?', #punctuation
		'\'', '\`', '\"'
	]

def load_stopwords(path) -> list:
	l = []
	with open(path) as f:
		l = f.read()
	l = l.split()
	return l

def tokenize(path) -> list:
	l = []
	txt = ""
	start = 0
	i = 0
	with open(path) as f:
		txt = f.read()

	while i < len(txt):
		#print(txt[i], i)
		if (start < i and txt[i] in seps):
			l.append(txt[start:i].lower())
			start = i = i + 1
		while (i < len(txt) and txt[i] in seps):
			start = i = i + 1
		i = i + 1
	if (start < i):
		l.append(txt[start:i].lower())
	l = [item.strip() for item in l]
	return l

def load_list_token(path, stpwpath) -> Doc:
	if (os.path.isfile(DATABASE_PATH)):
		f = open(DATABASE_PATH, "r")
		return json.loads(f.read())
	l = tokenize(path)
	stopwords = load_stopwords(stpwpath)
	uniq = []
	[uniq.append(u) for u in l if u not in uniq if u not in stopwords
		if len(u) > 2 #additional rule
	]
	#toks = [Token(u, l.count(u)) for u in uniq]
	toks = [{"str": u, "count": l.count(u)} for u in uniq]
	toks.sort(reverse=True, key=lambda token: token["count"])
	doc = {"name": path, "words": toks}
	f = open(DATABASE_PATH, "w")
	f.write(json.dumps(doc, indent=4))
	f.close()
	return doc


def summary(*argv: Doc):
	#Should take doc or list_doc and print summary
	for arg in argv:
		print(f'===Document: {arg["name"]}===')
		total_count = 0
		for t in arg["words"]:
			total_count = total_count + t["count"]
		for t in arg["words"]:
			print(f'{t["str"]} -  freq: ', "{:.2f}".format(t["count"]/total_count))

def get_occur(word: str, *docs: Doc) -> list:
	l = []
	for d in docs:
		for w in d["words"]:
			if w["str"] == word:
				l.append((d["name"], w["count"]))
	l.sort(reverse=True, key=lambda occur: occur[1])
	return l

doc = load_list_token("asimov.txt", "stopwords.txt")
occurs = get_occur("robot", doc)
print(occurs)
summary(doc)