import json
import os
import sys
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

def load_list_token(stpwpath, path) -> Doc:
	stopwords = load_stopwords(stpwpath)
	l = tokenize(path)
	uniq = []
	[uniq.append(u) for u in l if u not in uniq if u not in stopwords
		if len(u) > 2 #additional rule
	]
	#toks = [Token(u, l.count(u)) for u in uniq]
	toks = [{"str": u, "count": l.count(u)} for u in uniq]
	toks.sort(reverse=True, key=lambda token: token["count"])
	doc = {"name": path, "words": toks}
	return (doc)

def path_search(basepath) -> list[str]:
	paths = []
	for root, dirs, files in os.walk(basepath):
		for name in files:
			paths.append(os.path.join(root, name))
	return paths

def indexing(basepath = ".") -> List[Doc]:
	path_lst = []
	doc_lst = []
	if (os.path.isfile(DATABASE_PATH)):
		f = open(DATABASE_PATH, "r")
		doc_lst = json.loads(f.read())
		f.close()
		return doc_lst
	path_lst = path_search(basepath)
	for p in path_lst:
		try:
			doc = load_list_token(STPW_PATH, p)
			doc_lst.append(doc)
			print(f"{p} LOADED", file=sys.stderr)
		except:
			print(f"{p} FAILURE LOADING", file=sys.stderr)
	with open(DATABASE_PATH, "w") as f:
		f.write(json.dumps(doc_lst, indent=4))
	return doc_lst

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

if __name__ == '__main__':
	ldoc = indexing()
	#occurs = get_occur("robot", *ldoc)
	#print(occurs)
	#summary(doc)