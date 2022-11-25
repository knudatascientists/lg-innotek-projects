import tkinter as tk

from settings import *


def menu1_pushed(frame):
    global item_frame
    item_frame.destroy()
    item_frame = tk.Frame(frame, bg=ITEM_COLOR)
    item_frame.place(x=0, y=30 + MENU_HEIGHT, width=WIDTH, height=HEIGHT)

    input_frame = tk.Frame(item_frame)
    input_path_text = tk.Text(input_frame)
    input_path_btn = tk.Button(
        input_frame, text="입력 경로 입력", bg=MENU_COLOR, repeatdelay=1000, command=lambda: menu1_pushed(frame)
    )

    output_path_btn = tk.Button(
        menu_frame, text="출력 경로 입력", bg=MENU_COLOR, repeatdelay=1000, command=lambda: menu2_pushed(frame)
    )
    result_text = tk.Text(item_frame, bg=LEBEL_COLOR, width=MENU_WIDTH * 2)

    input_frame.place(width=WIDTH, height=MENU_HEIGHT)
    input_path_text.pack(side="left", padx=5)
    input_path_btn.pack(side="left", padx=5)


def write_log_text(result_text, log_text):
    result_text.config(state="normal")
    # result_text.delete('1.0', 'end')
    result_text.insert("current", log_text)
    result_text.config(state="disabled")


def menu2_pushed(frame):
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
    item_frame.place(x=0, y=30 + MENU_HEIGHT, width=WIDTH, height=HEIGHT)
    frame.place(x=0, y=0, width=WIDTH, height=HEIGHT)
    root.mainloop()
