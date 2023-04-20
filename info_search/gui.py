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
	occurs = []
	for w in words:
		occurs.extend(get_occur(w, *docs))
		#print("DEBUG: ", occurs)
	for o in occurs:
		Button(frame, text=f"'{o[0]}' - {o[1]} : {o[2]}", relief=FLAT, command=lambda path=o[1]: showFile(path))\
		.grid(row=rownb, sticky=W)
		rownb = rownb + 1
    
def run():
	docs = indexing()
	summary(*docs)
	root = Tk()
	root.title("Info search")
	root.geometry('800x600')
	root.bind("<Return>", lambda event: search_event(event, entry, docs, resframe_inside))
	root.bind("<Escape>", lambda x: root.destroy())

	resframe = Canvas(root)
	searchframe = Frame(root)
	searchframe.pack(side=TOP, pady=50)
	scrollbar = Scrollbar(root, orient=VERTICAL, command=resframe.yview)
	scrollbar.pack(side=RIGHT, fill=Y)
	resframe.configure(yscrollcommand=scrollbar.set)
	resframe.bind('<Configure>', lambda e: resframe.configure(scrollregion=resframe.bbox("all")))
	resframe_inside = Frame(resframe)
	resframe.create_window((0,0), window=resframe_inside, anchor="nw")
	entry_str = StringVar()
	entry_str.set("Type text to search ...")
	entry = Entry(searchframe, textvariable=entry_str)
	entry.pack(side=LEFT)
	search_ico = PhotoImage(file = r"./res/search_ico.png").subsample(2, 2)
	Button(searchframe, relief=FLAT, image = search_ico, command=lambda event="<Button-1>": search_event(event, entry, docs, resframe_inside))\
		.pack(side=LEFT)
	resframe.pack(fill="both", expand="yes")
	root.mainloop()