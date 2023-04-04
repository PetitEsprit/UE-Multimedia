from tok import *
from tkinter import *

def showFile(path):
	file_w = Toplevel()
	file_w.geometry('400x300')
	file_w.title(path)
	text = Text(file_w)
	with open(path) as f:
		text.insert(INSERT,  f.read())
	text.config(state=DISABLED)
	text.pack(fill="both", expand="yes")
	file_w.bind("<Escape>", lambda x: file_w.destroy())

def search_event(event, entry, docs, frame):
	for l in frame.grid_slaves():
		l.destroy()
	words = entry.get().split()
	rownb = 0
	for w in words:
		occurs = get_occur(w, *docs)
		#print("DEBUG: ", occurs)
		for o in occurs:
			Button(frame, text=f"'{w}' - {o[0]} : {o[1]}", relief=FLAT, command=lambda path=o[0]: showFile(path))\
			.grid(row=rownb, sticky=W)
			rownb = rownb + 1
    
def run():
	docs = indexing()
	root = Tk()
	root.title("Info search")
	root.geometry('800x600')
	root.bind("<Return>", lambda event: search_event(event, entry, docs, resultframe))
	root.bind("<Escape>", lambda x: root.destroy())

	resultframe = LabelFrame(root, text="Results:")
	searchframe = Frame(root)
	searchframe.pack(side=TOP, pady=50)
	entry_str = StringVar()
	entry_str.set("Type text to search...")
	entry = Entry(searchframe, textvariable=entry_str)
	entry.pack(side=LEFT)
	search_ico = PhotoImage(file = r"./res/search_ico.png").subsample(2, 2)
	Button(searchframe, relief=FLAT, image = search_ico, command=lambda event="<Button-1>": search_event(event, entry, docs, resultframe))\
		.pack(side=LEFT)
	resultframe.pack(fill="both", expand="yes")
	root.mainloop()