import tkinter as tk
from tkinter import filedialog

from settings import *


def menu1_pushed(frame):

    # call test class

    global item_frame
    item_frame.destroy()
    item_frame = tk.Frame(frame, bg=ITEM_COLOR)
    item_frame.place(x=0, y=40 + MENU_HEIGHT, width=WIDTH, height=HEIGHT)

    input_frame = tk.Frame(item_frame, width=WIDTH, height=MENU_HEIGHT, bg=ITEM_COLOR)
    input_path_entry = tk.Entry(input_frame, width=(WIDTH - 2 * MENU_WIDTH - 55) // 6)
    input_path_entry.insert(tk.END, FOLDER_PATH)
    input_path_btn = tk.Button(
        input_frame, text="찾아보기", bg=MENU_COLOR, repeatdelay=1000, command=lambda: folder_find(input_path_entry)
    )
    test_btn = tk.Button(
        input_frame,
        text="검사 시작",
        bg=MENU_COLOR,
        repeatdelay=1000,
        command=lambda: test_pushed(input_path_entry, result_text),
    )

    output_path_btn = tk.Button(
        menu_frame, text="출력 경로 입력", bg=MENU_COLOR, repeatdelay=1000, command=lambda: menu2_pushed(frame)
    )
    result_text = tk.Text(item_frame, bg=LEBEL_COLOR, width=MENU_WIDTH * 2)
    result_text.config(state="disabled")

    input_frame.place(x=40, y=10)
    input_path_entry.pack(side="left", padx=5)
    test_btn.pack(side="left", padx=5)
    input_path_btn.pack(side="left", padx=5)

    result_text.place(x=40, y=MENU_HEIGHT + 40, width=WIDTH - 80, height=HEIGHT - 40 * MENU_HEIGHT - 40)


def write_log_text(result_text, log_text):
    result_text.config(state="normal")
    # result_text.delete('1.0', 'end')
    result_text.insert("current", log_text + "\n")
    result_text.config(state="disabled")


def folder_find(
    input_path_entry,
):
    folder_path = filedialog.askdirectory(initialdir="./image")
    input_path_entry.delete(0, tk.END)
    input_path_entry.insert(tk.END, folder_path)


def test_pushed(input_path_entry, result_text):
    input_path = input_path_entry.get()
    if len(input_path):
        write_log_text(result_text, "Testing Products...")
    else:
        write_log_text(result_text, "Worng Directory Path")


def menu2_pushed(frame):
    # call test class
    pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Epoxy Test Modul")
    root.geometry(f"{WIDTH}x{HEIGHT}+100+100")
    root.resizable(False, True)

    frame = tk.Frame(root, bg=FRAME_COLOR)
    menu_frame = tk.Frame(frame, bg=MENU_COLOR)
    item_frame = tk.Frame(frame, bg=ITEM_COLOR)

    menu1 = tk.Button(
        menu_frame, text="전체 이미지 검사", bg=MENU_COLOR, repeatdelay=1000, command=lambda: menu1_pushed(frame)
    )
    menu2 = tk.Button(
        menu_frame, text="단일 이미지 검사", bg=MENU_COLOR, repeatdelay=1000, command=lambda: menu2_pushed(frame)
    )

    menu1.pack(side="left", padx=10)
    menu2.pack(side="left", padx=10)
    menu_frame.place(x=WIDTH / 2 - MENU_WIDTH - 15, y=10, height=MENU_HEIGHT + 20, width=WIDTH)
    item_frame.place(x=0, y=40 + MENU_HEIGHT, width=WIDTH, height=HEIGHT)
    frame.place(x=0, y=0, width=WIDTH, height=HEIGHT)
    root.mainloop()
