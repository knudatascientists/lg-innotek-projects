import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk
from tkinter import filedialog

from settings import *


class test_gui:
    def __init__(self):
        self.root = tk.Tk()
        self.font = tkfont.Font(family=FONT, size=FONT_SIZE)
        self.root.title("Epoxy Test Modul")
        self.root.geometry(f"{WIDTH}x{HEIGHT}+100+100")
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg=FRAME_COLOR)
        self.frame.place(x=0, y=0, width=WIDTH, height=HEIGHT)

        self.make_menu_frame()
        self.make_item_frame()
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def start_gui(self):
        self.root.mainloop()

    def make_menu_frame(self):
        self.menu_frame = tk.Frame(self.frame, bg=FRAME_COLOR)
        self.menu1 = tk.Button(
            self.menu_frame,
            text="전체 이미지 검사",
            bg=MENU_COLOR,
            repeatdelay=1000,
            command=lambda: self.menu1_pushed(),
            relief="groove",
            font=self.font,
        )
        self.menu2 = tk.Button(
            self.menu_frame,
            text="단일 이미지 검사",
            bg=MENU_COLOR,
            repeatdelay=1000,
            command=lambda: self.menu2_pushed(),
            relief="groove",
            font=self.font,
        )

        self.menu1.pack(side="left", padx=10)
        self.menu2.pack(side="left", padx=10)
        self.menu_frame.place(x=WIDTH / 2 - MENU_WIDTH - 15, y=10, height=MENU_HEIGHT + 20, width=WIDTH)

    def make_item_frame(self):
        try:
            self.item_frame.destroy()
        except:
            pass
        self.item_frame = tk.Frame(self.frame, bg=ITEM_COLOR)
        self.item_frame.place(x=0, y=40 + MENU_HEIGHT, width=WIDTH, height=HEIGHT)

    def make_input_frame(self):
        self.input_frame = tk.Frame(self.item_frame, width=WIDTH, height=MENU_HEIGHT, bg=ITEM_COLOR)
        self.input_path_entry = tk.Entry(self.input_frame, width=(WIDTH - 2 * MENU_WIDTH - 55) // 6)
        self.input_path_entry.insert(tk.END, FOLDER_PATH)
        self.input_path_btn = tk.Button(
            self.input_frame,
            text="찾아보기",
            bg=MENU_COLOR,
            repeatdelay=1000,
            command=lambda: self.folder_find(),
            font=self.font,
        )
        self.test_btn = tk.Button(
            self.input_frame,
            text="검사 시작",
            bg=MENU_COLOR,
            repeatdelay=1000,
            command=lambda: self.test_pushed(),
            font=self.font,
        )
        self.input_frame.place(x=40, y=10)
        self.input_path_entry.pack(side="left", padx=5)
        self.test_btn.pack(side="left", padx=5)
        self.input_path_btn.pack(side="left", padx=5)

    def make_result_frame(self):
        self.result_frame = tk.Frame(self.item_frame, width=WIDTH - 80, height=HEIGHT - MENU_HEIGHT - 140, bg="#000")

        self.result_frame.place(
            x=40,
            y=MENU_HEIGHT + 40,
        )
        self.result_text = tk.Text(
            self.result_frame,
            bg=LEBEL_COLOR,
            # width=MENU_WIDTH // 2,
            font=self.font,
            width=MENU_WIDTH // 2,
            height=(HEIGHT - MENU_HEIGHT - 140) // 15,
        )
        self.result_text.config(state="disabled")

        self.scrollb = ttk.Scrollbar(self.result_frame, command=self.result_text.yview)
        self.result_text["yscrollcommand"] = self.scrollb.set

        self.progressbar = ttk.Progressbar(self.result_frame, maximum=100)
        self.progressbar.pack(side="bottom", fill="x")
        self.result_text.pack(side="left", fill="y")
        self.scrollb.pack(side="left", fill="y")

    def menu1_pushed(self):

        # call test class
        self.make_item_frame()
        self.make_input_frame()
        self.make_result_frame()

    def menu2_pushed(self):
        # call test class
        self.make_item_frame()

    def write_log_text(self, log_text):
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, log_text + "\n")
        self.result_text.config(state="disabled")

    def folder_find(self):
        self.folder_path = filedialog.askdirectory(initialdir="./image")
        self.input_path_entry.delete(0, tk.END)
        self.input_path_entry.insert(tk.END, self.folder_path)

    def test_pushed(self):
        self.folder_path = self.input_path_entry.get()
        try:
            self.write_log_text(f"Testing Products from {self.folder_path}...")
        except:
            self.write_log_text("Worng Directory Path")

    def set_test_func(self, func):
        self.test_func = func


if __name__ == "__main__":
    gui = test_gui()
    gui.start_gui()
