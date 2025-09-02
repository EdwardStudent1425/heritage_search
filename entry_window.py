from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class EntryWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Search in archives")
        self.root.geometry("800x600")
        self.placeholders = {}  # Словник відповідностей Entry → текст плейсхолдера


        self.query = {}

        self.mainframe = ttk.Frame(self.root, padding="20 20 20 20")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.surname = StringVar()
        ttk.Label(self.mainframe, text="Прізвище").grid(column=0, row=0, sticky=W)
        self.surname_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.surname)
        self.surname_entry.grid(column=1, row=0, sticky=W)
        self.add_placeholder(self.surname_entry, "Прізвище")

        self.name = StringVar()
        ttk.Label(self.mainframe, text="Ім'я").grid(column=0, row=1, sticky=W)
        self.name_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.name)
        self.name_entry.grid(column=1, row=1, sticky=W)
        self.add_placeholder(self.name_entry, "Ім'я")

        self.patronymic = StringVar()
        ttk.Label(self.mainframe, text="По-батькові").grid(column=0, row=2, sticky=W)
        self.patronymic_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.patronymic)
        self.patronymic_entry.grid(column=1, row=2, sticky=W)
        self.add_placeholder(self.patronymic_entry, "По-батькові")

        ttk.Button(self.mainframe, text="Пошук", command=self.submit).grid(column=1, row=3, sticky=W)

        # --- Розширений пошук ---
        self.advanced_enabled = BooleanVar(value=False)
        self.advanced_checkbox = ttk.Checkbutton(
            self.mainframe,
            text="Розширений пошук",
            variable=self.advanced_enabled,
            command=self.toggle_advanced
        )
        self.advanced_checkbox.grid(column=2, row=3, sticky=W)

        self.advanced_area = ttk.Frame(self.mainframe)
        self.advanced_area.grid(column=0, row=4, columnspan=3, sticky=W)
        self.advanced_area.grid_remove()  # ховаємо на старті

        # Dropdown для вибору групи
        ttk.Label(self.advanced_area, text="Оберіть групу параметрів:").grid(column=0, row=0, sticky=W)
        self.param_choice = StringVar()
        self.param_box = ttk.Combobox(self.advanced_area, width=30, textvariable=self.param_choice,
                                      values=["Роки життя", "Поховання", "Звинувачення", "Народження", "Про людину"])
        self.param_box.grid(column=1, row=0, sticky=W)
        self.param_box.bind("<<ComboboxSelected>>", self.show_selected_group)

        # Фрейми для кожної категорії
        self.group_frames = {}

        # === Група 1: Роки життя ===
        frame_life = ttk.Frame(self.advanced_area)
        self.birth_year = StringVar()
        self.death_year = StringVar()
        ttk.Label(frame_life, text="Рік народження").grid(column=0, row=0, sticky=W)
        birth_entry = ttk.Entry(frame_life, width=30, textvariable=self.birth_year)
        birth_entry.grid(column=1, row=0, sticky=W)
        self.add_placeholder(birth_entry, "Рік народження")
        ttk.Label(frame_life, text="Рік смерті").grid(column=0, row=1, sticky=W)
        death_entry = ttk.Entry(frame_life, width=30, textvariable=self.death_year)
        death_entry.grid(column=1, row=1, sticky=W)
        self.add_placeholder(death_entry, "Рік смерті")
        self.group_frames["Роки життя"] = frame_life

        # === Група 2: Поховання ===
        frame_burial = ttk.Frame(self.advanced_area)

        self.burial_region = StringVar()
        self.burial_city = StringVar()
        self.burial_village = StringVar()
        self.burial_place = StringVar()

        ttk.Label(frame_burial, text="Область поховання").grid(column=0, row=0, sticky=W)
        burial_region_entry = ttk.Entry(frame_burial, width=30, textvariable=self.burial_region)
        burial_region_entry.grid(column=1, row=0, sticky=W)
        self.add_placeholder(burial_region_entry, "Область поховання")

        ttk.Label(frame_burial, text="Місто поховання").grid(column=0, row=1, sticky=W)
        burial_city_entry = ttk.Entry(frame_burial, width=30, textvariable=self.burial_city)
        burial_city_entry.grid(column=1, row=1, sticky=W)
        self.add_placeholder(burial_city_entry, "Місто поховання")

        ttk.Label(frame_burial, text="Село поховання").grid(column=0, row=2, sticky=W)
        burial_village_entry = ttk.Entry(frame_burial, width=30, textvariable=self.burial_village)
        burial_village_entry.grid(column=1, row=2, sticky=W)
        self.add_placeholder(burial_village_entry, "Село поховання")

        ttk.Label(frame_burial, text="Місце поховання").grid(column=0, row=3, sticky=W)
        burial_place_entry = ttk.Entry(frame_burial, width=30, textvariable=self.burial_place)
        burial_place_entry.grid(column=1, row=3, sticky=W)
        self.add_placeholder(burial_place_entry, "Місце поховання")

        self.group_frames["Поховання"] = frame_burial

        # === Група 3: Звинувачення ===
        frame_conviction = ttk.Frame(self.advanced_area)

        self.arrest_min = StringVar()
        self.arrest_max = StringVar()
        self.indictment = StringVar()
        self.conviction_min = StringVar()
        self.conviction_max = StringVar()
        self.conviction_org = StringVar()
        self.sentence = StringVar()
        self.detentionplace = StringVar()
        self.release_min = StringVar()
        self.release_max = StringVar()
        self.execution_min = StringVar()
        self.execution_max = StringVar()
        self.archive_case_number = StringVar()

        ttk.Label(frame_conviction, text="Дата арешту (мінімум)").grid(column=0, row=0, sticky=W)
        arrest_min_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.arrest_min)
        arrest_min_entry.grid(column=1, row=0, sticky=W)
        self.add_placeholder(arrest_min_entry, "Дата арешту (мінімум)")

        ttk.Label(frame_conviction, text="Дата арешту (максимум)").grid(column=0, row=1, sticky=W)
        arrest_max_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.arrest_max)
        arrest_max_entry.grid(column=1, row=1, sticky=W)
        self.add_placeholder(arrest_max_entry, "Дата арешту (максимум)")

        ttk.Label(frame_conviction, text="Обвинувачення").grid(column=0, row=2, sticky=W)
        indictment_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.indictment)
        indictment_entry.grid(column=1, row=2, sticky=W)
        self.add_placeholder(indictment_entry, "Обвинувачення")

        ttk.Label(frame_conviction, text="Дата вироку (мінімум)").grid(column=0, row=3, sticky=W)
        conviction_min_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.conviction_min)
        conviction_min_entry.grid(column=1, row=3, sticky=W)
        self.add_placeholder(conviction_min_entry, "Дата вироку (мінімум)")

        ttk.Label(frame_conviction, text="Дата вироку (максимум)").grid(column=0, row=4, sticky=W)
        conviction_max_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.conviction_max)
        conviction_max_entry.grid(column=1, row=4, sticky=W)
        self.add_placeholder(conviction_max_entry, "Дата вироку (максимум)")

        ttk.Label(frame_conviction, text="Орган, що виніс вирок").grid(column=0, row=5, sticky=W)
        conviction_org_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.conviction_org)
        conviction_org_entry.grid(column=1, row=5, sticky=W)
        self.add_placeholder(conviction_org_entry, "Орган, що виніс вирок")

        ttk.Label(frame_conviction, text="Покарання").grid(column=0, row=6, sticky=W)
        sentence_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.sentence)
        sentence_entry.grid(column=1, row=6, sticky=W)
        self.add_placeholder(sentence_entry, "Покарання")

        ttk.Label(frame_conviction, text="Місце утримання").grid(column=0, row=7, sticky=W)
        detentionplace_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.detentionplace)
        detentionplace_entry.grid(column=1, row=7, sticky=W)
        self.add_placeholder(detentionplace_entry, "Місце утримання")

        ttk.Label(frame_conviction, text="Дата звільнення (мінімум)").grid(column=0, row=8, sticky=W)
        release_min_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.release_min)
        release_min_entry.grid(column=1, row=8, sticky=W)
        self.add_placeholder(release_min_entry, "Дата звільнення (мінімум)")

        ttk.Label(frame_conviction, text="Дата звільнення (максимум)").grid(column=0, row=9, sticky=W)
        release_max_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.release_max)
        release_max_entry.grid(column=1, row=9, sticky=W)
        self.add_placeholder(release_max_entry, "Дата звільнення (максимум)")

        ttk.Label(frame_conviction, text="Дата страти (мінімум)").grid(column=0, row=10, sticky=W)
        execution_min_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.execution_min)
        execution_min_entry.grid(column=1, row=10, sticky=W)
        self.add_placeholder(execution_min_entry, "Дата страти (мінімум)")

        ttk.Label(frame_conviction, text="Дата страти (максимум)").grid(column=0, row=11, sticky=W)
        execution_max_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.execution_max)
        execution_max_entry.grid(column=1, row=11, sticky=W)
        self.add_placeholder(execution_max_entry, "Дата страти (максимум)")

        ttk.Label(frame_conviction, text="Номер справи в архіві").grid(column=0, row=12, sticky=W)
        archive_case_number_entry = ttk.Entry(frame_conviction, width=30, textvariable=self.archive_case_number)
        archive_case_number_entry.grid(column=1, row=12, sticky=W)
        self.add_placeholder(archive_case_number_entry, "Номер справи в архіві")

        self.group_frames["Звинувачення"] = frame_conviction

        # === Група 4: Народження ===
        frame_birthplace = ttk.Frame(self.advanced_area)

        self.birth_region = StringVar()
        self.place_birth = StringVar()

        ttk.Label(frame_birthplace, text="Область народження").grid(column=0, row=0, sticky=W)
        birth_region_entry = ttk.Entry(frame_birthplace, width=30, textvariable=self.birth_region)
        birth_region_entry.grid(column=1, row=0, sticky=W)
        self.add_placeholder(birth_region_entry, "Область народження")

        ttk.Label(frame_birthplace, text="Місто/село народження").grid(column=0, row=1, sticky=W)
        place_birth_entry = ttk.Entry(frame_birthplace, width=30, textvariable=self.place_birth)
        place_birth_entry.grid(column=1, row=1, sticky=W)
        self.add_placeholder(place_birth_entry, "Місто/село народження")

        self.group_frames["Народження"] = frame_birthplace

        # === Група 5: Про людину ===
        frame_person = ttk.Frame(self.advanced_area)

        self.birth_min = StringVar()
        self.birth_max = StringVar()
        self.death_min = StringVar()
        self.death_max = StringVar()
        self.birthplace = StringVar()
        self.liveplace = StringVar()
        self.nationality = StringVar()
        self.social = StringVar()
        self.profession = StringVar()
        self.deathplace = StringVar()
        self.burialplace = StringVar()
        self.body = StringVar()
        self.categories = StringVar()

        ttk.Label(frame_person, text="Рік народження (мінімум)").grid(column=0, row=0, sticky=W)
        birth_min_entry = ttk.Entry(frame_person, width=30, textvariable=self.birth_min)
        birth_min_entry.grid(column=1, row=0, sticky=W)
        self.add_placeholder(birth_min_entry, "Рік народження (мінімум)")

        ttk.Label(frame_person, text="Рік народження (максимум)").grid(column=0, row=1, sticky=W)
        birth_max_entry = ttk.Entry(frame_person, width=30, textvariable=self.birth_max)
        birth_max_entry.grid(column=1, row=1, sticky=W)
        self.add_placeholder(birth_max_entry, "Рік народження (максимум)")

        ttk.Label(frame_person, text="Рік смерті (мінімум)").grid(column=0, row=2, sticky=W)
        death_min_entry = ttk.Entry(frame_person, width=30, textvariable=self.death_min)
        death_min_entry.grid(column=1, row=2, sticky=W)
        self.add_placeholder(death_min_entry, "Рік смерті (мінімум)")

        ttk.Label(frame_person, text="Рік смерті (максимум)").grid(column=0, row=3, sticky=W)
        death_max_entry = ttk.Entry(frame_person, width=30, textvariable=self.death_max)
        death_max_entry.grid(column=1, row=3, sticky=W)
        self.add_placeholder(death_max_entry, "Рік смерті (максимум)")

        ttk.Label(frame_person, text="Місце народження").grid(column=0, row=4, sticky=W)
        birthplace_entry = ttk.Entry(frame_person, width=30, textvariable=self.birthplace)
        birthplace_entry.grid(column=1, row=4, sticky=W)
        self.add_placeholder(birthplace_entry, "Місце народження")

        ttk.Label(frame_person, text="Місце проживання").grid(column=0, row=5, sticky=W)
        liveplace_entry = ttk.Entry(frame_person, width=30, textvariable=self.liveplace)
        liveplace_entry.grid(column=1, row=5, sticky=W)
        self.add_placeholder(liveplace_entry, "Місце проживання")

        ttk.Label(frame_person, text="Національність").grid(column=0, row=6, sticky=W)
        nationality_entry = ttk.Entry(frame_person, width=30, textvariable=self.nationality)
        nationality_entry.grid(column=1, row=6, sticky=W)
        self.add_placeholder(nationality_entry, "Національність")

        ttk.Label(frame_person, text="Соціальний стан").grid(column=0, row=7, sticky=W)
        social_entry = ttk.Entry(frame_person, width=30, textvariable=self.social)
        social_entry.grid(column=1, row=7, sticky=W)
        self.add_placeholder(social_entry, "Соціальний стан")

        ttk.Label(frame_person, text="Професія").grid(column=0, row=8, sticky=W)
        profession_entry = ttk.Entry(frame_person, width=30, textvariable=self.profession)
        profession_entry.grid(column=1, row=8, sticky=W)
        self.add_placeholder(profession_entry, "Професія")

        ttk.Label(frame_person, text="Місце смерті").grid(column=0, row=9, sticky=W)
        deathplace_entry = ttk.Entry(frame_person, width=30, textvariable=self.deathplace)
        deathplace_entry.grid(column=1, row=9, sticky=W)
        self.add_placeholder(deathplace_entry, "Місце смерті")

        # ttk.Label(frame_person, text="Місце поховання").grid(column=0, row=10, sticky=W)
        # burialplace_entry = ttk.Entry(frame_person, width=30, textvariable=self.burialplace)
        # burialplace_entry.grid(column=1, row=10, sticky=W)
        # self.add_placeholder(burialplace_entry, "Місце поховання")

        ttk.Label(frame_person, text="Орган, що склав справу").grid(column=0, row=11, sticky=W)
        body_entry = ttk.Entry(frame_person, width=30, textvariable=self.body)
        body_entry.grid(column=1, row=11, sticky=W)
        self.add_placeholder(body_entry, "Орган, що склав справу")

        ttk.Label(frame_person, text="Категорії").grid(column=0, row=12, sticky=W)
        categories_entry = ttk.Entry(frame_person, width=30, textvariable=self.categories)
        categories_entry.grid(column=1, row=12, sticky=W)
        self.add_placeholder(categories_entry, "Категорії")

        self.group_frames["Про людину"] = frame_person



    def toggle_advanced(self):
        if self.advanced_enabled.get():
            self.advanced_area.grid()
        else:
            self.advanced_area.grid_remove()
            for frame in self.group_frames.values():
                frame.grid_remove()

    def show_selected_group(self, event):
        selected = self.param_choice.get()
        for name, frame in self.group_frames.items():
            frame.grid_remove()
        if selected in self.group_frames:
            self.group_frames[selected].grid(column=0, row=1, columnspan=3, pady=10, sticky=W)


    def submit(self):
        self.query = {}

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, StringVar):
                value = attr.get().strip()
                entry = self.get_entry_widget_for_var(attr)
                if entry:
                    placeholder = self.placeholders.get(entry)
                    if value and value != placeholder:
                        self.query[attr_name] = value
        messagebox.showinfo("Згенерований запит", f"{self.query}")



    def get_entry_widget_for_var(self, var):
        containers = [self.mainframe, self.advanced_area] + list(self.group_frames.values())
        for container in containers:
            for child in container.winfo_children():
                if isinstance(child, ttk.Entry) and child.cget("textvariable") == str(var):
                    return child
        return None


    def add_placeholder(self, widget, text):
        widget.insert(0, text)
        widget.config(foreground="gray")
        self.placeholders[widget] = text 

        def on_focus_in(event):
            if widget.get() == text:
                widget.delete(0, END)
                widget.config(foreground="black")

        def on_focus_out(event):
            if not widget.get():
                widget.insert(0, text)
                widget.config(foreground="gray")

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)


if __name__ == "__main__":
    root = Tk()
    app = EntryWindow(root)
    root.mainloop()
