import json
import os
from typing import Dict, List

Doc = Dict

DATABASE_PATH = "./.db"
STPW_PATH = "./.stopwords.txt"

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

def load_list_token(stpwpath, *path) -> List[Doc]:
	if (os.path.isfile(DATABASE_PATH)):
		f = open(DATABASE_PATH, "r")
		return json.loads(f.read())
	stopwords = load_stopwords(stpwpath)
	docs = []
	for p in path:
		l = tokenize(p)
		uniq = []
		[uniq.append(u) for u in l if u not in uniq if u not in stopwords
			if len(u) > 2 #additional rule
		]
		#toks = [Token(u, l.count(u)) for u in uniq]
		toks = [{"str": u, "count": l.count(u)} for u in uniq]
		toks.sort(reverse=True, key=lambda token: token["count"])
		docs.append({"name": p, "words": toks})
	f = open(DATABASE_PATH, "w")
	f.write(json.dumps(docs, indent=4))
	f.close()
	return docs

def indexing() -> List[Doc]:
	path_lst = []
	path_lst.append("asimov.txt") # to replace by recursive search
	return load_list_token(STPW_PATH, *path_lst)

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
		#print(d["name"])
		for w in d["words"]:
			if w["str"] == word:
				l.append((d["name"], w["count"]))
	l.sort(reverse=True, key=lambda occur: occur[1])
	return l

#ldoc = indexing()
#occurs = get_occur("robot", ldoc)
#print(occurs)
#summary(doc)