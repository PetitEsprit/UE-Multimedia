from tok import *
from tkinter import *

def kbevent(event, entry, docs, frame):
	for l in frame.grid_slaves():
		l.destroy()
	words = entry.get().split()
	rownb = 0
	for w in words:
		occurs = get_occur(w, *docs)
		#print("DEBUG: ", occurs)
		for o in occurs:
			labelword = Label(frame, text=f"'{w} - ")
			labelpath = Label(frame, text=f"{o[0]}")
			labelcount = Label(frame, text=f": {o[1]}")
			labelword.grid(row=rownb, column=0)
			labelpath.grid(row=rownb, column=1)
			labelcount.grid(row=rownb, column=2)
			rownb = rownb + 1
    
def run():
	docs = indexing()
	window = Tk()
	window.geometry('800x600')
	window.bind("<Return>", lambda event: kbevent(event, entry, docs, labelframe))
	window.bind("<Escape>", lambda x: window.destroy())

	label = Label(window, text="Info search")
	label.pack(side=TOP)

	entry_str = StringVar()
	entry_str.set("Type text to search...")
	entry = Entry(window, textvariable=entry_str, width=30)
	entry.pack()

	labelframe = LabelFrame(window, text="Results:")
	labelframe.pack(fill="both", expand="yes")

	window.mainloop()