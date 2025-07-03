from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class EntryWindow:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Search in archives")
        self.root.geometry("1000x600")
        self.query = None

        self.mainframe = ttk.Frame(self.root, padding='30 30 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.surname = StringVar()
        surname_entry = ttk.Entry(self.mainframe, width=20, textvariable=self.surname)
        surname_entry.grid(column=1, row=1, sticky=(W, E))

        self.name = StringVar()
        name_entry = ttk.Entry(self.mainframe, width=20, textvariable=self.name)
        name_entry.grid(column=1, row=2, sticky=(W, E))
        


        self.patronymic = StringVar()
        patronymic_entry = ttk.Entry(self.mainframe, width= 20 , textvariable=self.patronymic)
        patronymic_entry.grid(column=1, row=3, sticky=(W, E))

        ttk.Label(self.mainframe, text='Введіть дані особи').grid(column=1, row=0, sticky=(W, E))

        ttk.Label(self.mainframe, text='Прізвище').grid(column=2, row=1, sticky=(W, E))
        ttk.Label(self.mainframe, text='Ім`я').grid(column=2, row=2, sticky=(W, E))
        ttk.Label(self.mainframe, text="По-батькові").grid(column=2, row=3, sticky=(W, E))

        ttk.Button(self.mainframe, text="Пошук", command=self.submit).grid(column=1, row=4, sticky=(W, E))

        self.result_label = ttk.Label(self.mainframe, text="")
        self.result_label.grid(column=1, row=5, columnspan=2, sticky=(W, E))

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def submit(self):
        surname = self.surname.get()
        name = self.name.get()
        patronymic = self.patronymic.get()

        self.query = {
            'surname':surname,
            'name':name,
            'patronymic':patronymic
        }

        self.result_label.config(text=f"Запит: {self.query}")
        messagebox.showinfo(title="Результат пошуку", message=str(self.query))



