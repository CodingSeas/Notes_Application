from tkinter import *
from tkinter import messagebox
import os

BG_COLOR = '#B1DDC6'


class Note:
    def __init__(self):
        """MAIN"""
        self.notes_dict = {}

        self.window = Tk()
        self.window.title("Notes")
        # window.geometry("800x800")
        self.window.rowconfigure(0, minsize=80, weight=1)
        self.window.rowconfigure(1, minsize=400, weight=1)
        self.window.columnconfigure(1, minsize=300, weight=1)

        # Title Text
        self.title_text = Text(self.window, width=20, height=1, bg=BG_COLOR, font=("Comicsans", 40, "bold"))
        self.title_text.grid(row=0, column=1, sticky="nsew")

        # Text Editor
        self.edit_text = Text(self.window, width=20, height=20, wrap=WORD, bg="#DEF5E5", font=("Comicsans", 10))
        self.edit_text.grid(row=1, column=1, sticky="nsew", columnspan=3)

        # LEFT side Button list
        self.frm_button = Frame(self.window, relief=RAISED, bd=2, bg=BG_COLOR)
        self.frm_button.grid(row=0, column=0, sticky="nsew", rowspan=2)

        # Save Button
        self.save_btn = Button(text=" Save ", bg="#8EC3B0", command=self.save_note)
        self.save_btn.grid(row=0, column=2, sticky="nswe")

        # Delete Button
        self.delete_btn = Button(text="Delete", bg="#8EC3B0", command=self.delete_note)
        self.delete_btn.grid(row=0, column=3, sticky="nswe")

        self.show_notes()
        # Scrollbar
        scrollbar = Scrollbar(orient=VERTICAL, command=self.edit_text.yview)
        scrollbar.grid(row=1, column=3, sticky=N + S + E)

        self.edit_text.config(yscrollcommand=scrollbar.set)

        self.window.mainloop()

    def note_btn(self, title, row):
        """Making notes on screen."""

        def show():
            """It Shows the data on the text grid."""
            if title in self.notes_dict:
                details = self.notes_dict[title]
                self.edit_text.delete(0., END)
                self.edit_text.insert(END, str(details))
            else:
                messagebox.showerror(title="Error", message="Note Empty")

            # Showing Title on title text
            self.title_text.delete(0., END)
            self.title_text.insert(END, title)

        btn = Button(self.frm_button, text=title, command=show, bg='#9ED5C5')
        btn.grid(row=row, column=0, sticky="ew", pady=5, padx=5)

    def show_notes(self):
        # Displaying all the notes
        try:
            with open("data/notes_name.txt", "r+") as file_names:
                file_name_list = file_names.read().split("\n")
        except FileNotFoundError:
            with open('data/notes_name.txt', "w") as file:
                print("File Created!!")
                file.close()
                self.title_text.insert(0., "WELCOME")
                self.edit_text.insert(0., "Edit text")
            file_name_list = []
        for file_name in file_name_list:
            try:
                with open(f"data/{file_name}.txt", "r+") as file:
                    data = file.read()
            except FileNotFoundError:
                pass
            else:
                self.notes_dict[file_name] = data
        row = 0
        for note in self.notes_dict:
            self.note_btn(note, row)
            row += 1

        self.window.update()

    def save_note(self):
        title = self.title_text.get(0., END)[0:-1]
        text = self.edit_text.get(0., END)[0:-1]

        with open("data/notes_name.txt", "a+") as file:
            file.write(f"{title}\n")
        with open(f"data/{title}.txt", "w") as file:
            file.write(text)

        print("Note Saved!")
        self.show_notes()

    def delete_note(self):
        title = self.title_text.get(0., END)[:-1]
        confirm = messagebox.askokcancel(title="Delete", message=f"Do you want to delete note? \n{title}")
        if confirm:
            try:
                os.remove(f"data/{title}.txt")
            except FileNotFoundError:
                print(f"Note {title} is not saved.")
            else:
                print("Note Deleted!")
                self.notes_dict.pop(title)
                with open("data/notes_name.txt", "w") as file:
                    for note in self.notes_dict:
                        file.write(f"{note}\n")

            # Clearing the data on the tab.
            self.title_text.delete(0., END)
            self.edit_text.delete(0., END)
        self.update()
        self.show_notes()

    def update(self):
        self.frm_button.destroy()
        self.frm_button = Frame(self.window, relief=RAISED, bd=2, bg=BG_COLOR)
        self.frm_button.grid(row=0, column=0, sticky="nsew", rowspan=2)


if __name__ == "__main__":
    """Running Our Notes Application."""
    Note()
