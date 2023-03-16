class Token:
	"""Token class"""
	def __init__(self, content, count):
		self.content = content
		self.count = count

seps = ['\n', '\t', '\v', '\f', '\r', ' ', #spaces
		'.', ',',';', ":", '!', '?'] #punctuation

def tokenize(path) -> list:
	l = []
	txt = ""
	start = 0
	i = 0
	with open(path) as f:
		txt = f.read()

	while i < len(txt):
		print(txt[i], i)
		if (start < i and txt[i] in seps):
			l.append(txt[start:i])
			start = i = i + 1
		while (i < len(txt) and txt[i] in seps):
			start = i = i + 1
		i = i + 1
	if (start < i):
		l.append(txt[start:i])
	l = [item.strip() for item in l]
	return l

#def load_list_token(path) -> list:
#	

def load_stopwords(path) -> list:
	l = []
	with open(path) as f:
		l = f.read()
	l = l.split()
	return l

toks = tokenize("asimov.txt")
print(toks)
#print(load_stopwords("stopwords.txt"))
#print(str(Token("fefez", 1)))