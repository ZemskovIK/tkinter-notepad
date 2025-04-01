from tkinter import *
from tkinter import ttk, filedialog, messagebox, colorchooser
import encryption

current_file = None
is_modified = False
text_scale = 100
line_end = "Windows (CRLF)"
encoding = "UTF-8"

def font_changed(selected_font):
    text_area.config(font=selected_font)

def select_font():
    current_font = text_area["font"]
    root.call("tk", "fontchooser", "configure", "-font", current_font, "-command", root.register(font_changed))
    root.call("tk", "fontchooser", "show")

def select_color():
    result = colorchooser.askcolor(initialcolor=text_area["foreground"])
    if result[1]:
        text_area.config(foreground=result[1])

def update_window_title():
    if current_file:
        title = current_file.split("/")[-1]
    else:
        title = "Безымянный"
    if is_modified:
        title = f"*{title}"
    root.title(f"{title} - Блокнот AmTCD+")

def new_file(event=None):
    global current_file, is_modified
    current_file = None
    text_area.delete("1.0", END)
    is_modified = False
    update_window_title()


def open_file(event=None):
    global current_file, is_modified
    file_path = filedialog.askopenfilename(filetypes=[("Зашифрованные файлы", "*.txtx")])
    if not file_path:
        return
    current_file = file_path
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        decrypted_text = encryption.decrypt(content)
        text_area.delete("1.0", END)
        text_area.insert("1.0", decrypted_text)
        is_modified = False
        text_area.edit_modified(False)
        update_window_title()
    except ValueError:
        messagebox.showerror("Ошибка", "Файл поврежден или имеет неверный формат!")

def save_file(event=None):
    global current_file
    if current_file:
        save_as_file(current_file)
    else:
        save_as()

def save_as(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".txtx",
                                             filetypes=[("Зашифрованные файлы", "*.txtx")])
    if not file_path:
        return
    save_as_file(file_path)

def save_as_file(file_path):
    global current_file, is_modified
    current_file = file_path
    text = text_area.get("1.0", END).strip()
    encrypted_text = encryption.encrypt(text)  # Используем новый метод
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(encrypted_text)
    is_modified = False
    update_window_title()

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")

def show_about():
    messagebox.showinfo("О программе",
        "Программа для 'прозрачного шифрования'\n"
        "(с) Zemskov I.K., Russia, 2025\n"
        "\nС любовью и уважением родителям:\nКириллу Валентиновичу и Маргарите Геннадиевне")

def show_help():
    messagebox.showinfo("Справка",
        "«Блокнот AmTCD+» — приложение для работы с зашифрованными текстами.\n"
        "Возможности:\n"
        "  - Создание, открытие и сохранение зашифрованных файлов (.txtx).\n"
        "  - Ввод и сохранение личного ключа шифрования.\n"
        "  - Изменение шрифта и цвета текста.\n"
        "  - Модальная форма «О программе» и не модальная форма «Справка».")

def on_text_change(event=None):
    global is_modified
    if text_area.edit_modified():
        is_modified = True
        text_area.edit_modified(False)
    update_window_title()

def update_copy_state(event=None):
    if text_area.tag_ranges("sel"):
        edit_menu.entryconfig(0, state=NORMAL)
    else:
        edit_menu.entryconfig(0, state=DISABLED)

def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==86 and  ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")
    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

def update_status_bar(event=None):
    cursor_position = text_area.index(INSERT)
    line, column = map(int, cursor_position.split("."))
    text_content = text_area.get("1.0", "end-1c")
    char_count = len(text_content)
    left_text = f"Строка {line}, столбец {column}   |   {char_count} символов"
    right_text = f"|  {text_scale}%       |  {line_end}          |  {encoding}            "
    left_label.config(text=left_text)
    right_label.config(text=right_text)

root = Tk()
root.title("Безымянный - Блокнот AmTCD+")
root.geometry("1000x600+300+100")
root.iconbitmap(default="./notepad.ico")

scrollbar = Scrollbar(root, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

text_area = Text(root, wrap="word", yscrollcommand=scrollbar.set)
text_area.pack(expand=True, fill="both")
scrollbar.config(command=text_area.yview)

text_area.bind("<<Modified>>", on_text_change)
text_area.focus_set()

separator = ttk.Separator(root, orient=HORIZONTAL)
separator.pack(side=BOTTOM, fill=X)
status_frame = Frame(root, bd=1, relief=SUNKEN)
status_frame.pack(side=BOTTOM, fill=X)
left_label = Label(status_frame, text="", anchor=W, padx=10)
left_label.pack(side=LEFT)
right_label = Label(status_frame, text="", anchor=E, padx=10)
right_label.pack(side=RIGHT)

main_menu = Menu(root)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="Новый".ljust(30) + "CTRL+N", command=new_file)
file_menu.add_command(label="Открыть".ljust(29) + "CTRL+O", command=open_file)
file_menu.add_command(label="Сохранить".ljust(27) + "CTRL+S", command=save_file)
file_menu.add_command(label="Сохранить как...".ljust(24) + "CTRL+SHIFT+S", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Выход".ljust(31) + "CTRL+Q", command=root.quit)
main_menu.add_cascade(label="Файл", menu=file_menu)

edit_menu = Menu(main_menu, tearoff=0)
edit_menu.add_command(label="Копировать".ljust(20) + "CTRL+C", command=copy_text, state=DISABLED)
edit_menu.add_command(label="Вставить".ljust(24) + "CTRL+V", command=paste_text)
edit_menu.add_separator()
settings_menu = Menu(edit_menu, tearoff=0)
settings_menu.add_command(label="Выбрать шрифт", command=select_font)
settings_menu.add_command(label="Выбрать цвет текста", command=select_color)
edit_menu.add_cascade(label="Параметры...", menu=settings_menu)
main_menu.add_cascade(label="Правка", menu=edit_menu)

help_menu = Menu(main_menu, tearoff=0)
help_menu.add_command(label="Содержание", command=show_help)
help_menu.add_separator()
help_menu.add_command(label="О программе...", command=show_about)
main_menu.add_cascade(label="Справка", menu=help_menu)

root.config(menu=main_menu)

text_area.bind("<<Selection>>", update_copy_state)
text_area.bind("<KeyRelease>", update_status_bar)
text_area.bind("<ButtonRelease>", update_status_bar)
update_status_bar()
root.bind_all("<Key>", _onKeyRelease, "+")
root.bind("<Control-n>", new_file)
root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-Shift-S>", save_as)
root.bind("<Control-q>", lambda event=None: root.quit())

root.mainloop()
