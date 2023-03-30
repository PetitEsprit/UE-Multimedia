from tok import *
from tkinter import *

def kbevent(event, entry, docs, result_str):
	log = ""
	words = entry.get().split()
	for w in words:
		occurs = get_occur(w, *docs)
		#print("DEBUG: ", occurs)
		for o in occurs:
			log = log + f'{o[0]}: {o[1]}' + '\n'
	result_str.set(log)
    
def run():
	docs = indexing()
	window = Tk()
	window.geometry('600x400')
	window.bind("<Return>", lambda event: kbevent(event, entry, docs, result_str))
	window.bind("<Escape>", lambda x: window.destroy())

	label = Label(window, text="Info search")
	label.pack(side=TOP)

	entry_str = StringVar()
	entry_str.set("texte par défaut")
	entry = Entry(window, textvariable=entry_str, width=30)
	entry.pack()

	labelframe = LabelFrame(window, text="Results:")
	labelframe.pack(fill="both", expand="yes")
	result_str = StringVar()
	result = Label(labelframe, textvariable=result_str)
	result.pack(side=TOP)

	window.mainloop()