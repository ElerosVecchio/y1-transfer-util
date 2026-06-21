import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.messagebox import askyesno, showerror, showinfo

import transfer


def disable_input():
    input_entry["state"] = "disabled"
    input_browse["state"] = "disabled"
    output_entry["state"] = "disabled"
    output_browse["state"] = "disabled"
    convert_checkbox["state"] = "disabled"
    start_button["state"] = "disabled"


def enable_input():
    input_entry["state"] = "enabled"
    input_browse["state"] = "enabled"
    output_entry["state"] = "enabled"
    output_browse["state"] = "enabled"
    convert_checkbox["state"] = "enabled"
    start_button["state"] = "enabled"


def finished_transfer(transferred, skipped):
    status_label.config(
        {"text": f"Done! {transferred} transferred, {skipped} skipped"},
    )
    showinfo(
        title="Transfer Completed",
        message=f"Done! {transferred} transferred, {skipped} skipped",
    )
    enable_input()


def start_transfer():
    """Starts the transfer process after checking paths and disabling fields"""

    src = os.path.abspath(input_file_string.get())
    dst = os.path.abspath(output_file_string.get())

    if not os.path.isdir(src):
        showerror(title="Error", message="Input Path is not a Directory")
        return
    if not os.path.isdir(dst):
        showerror(title="Error", message="Output Path is not a Directory")
        return

    if src == dst:
        if not askyesno(
            title="Same Paths", message="Input and Output Paths are the same, continue?"
        ):
            return

    excluded = exclude_text.get('1.0', 'end').split('\n')

    disable_input()
    thread = threading.Thread(
        target=transfer.transfer_loop,
        args=(
            src,
            dst,
            convert_bool.get(),
            copy_embed_cover_bool.get(),
            status_label,
            progress,
            root,
            excluded,
            finished_transfer,
        ),
    )
    thread.start()


def input_dialog():
    """Open folder dialogue to get input directory"""

    directory = fd.askdirectory()
    input_file_string.set(directory)


def output_dialog():
    """Open folder dialogue to get output directory"""

    directory = fd.askdirectory()
    output_file_string.set(directory)


def exclude_add_files_dialog():
    filenames = fd.askopenfilenames()
    for x in filenames:
        exclude_text.insert("end", f'{os.path.abspath(x)}\n')


def exclude_add_dirs_dialog():
    dirname = fd.askdirectory()
    if dirname != "":
        exclude_text.insert("end", f'{os.path.abspath(dirname)}\n')


def exclude_save_dialog():
    file = fd.asksaveasfile(initialdir=".", initialfile="excludelist.txt", filetypes=[
                            ("Text Documents", "*.txt")])
    if file:
        file.write(exclude_text.get("1.0", "end"))
        file.close()


def exclude_load_dialog():
    file = fd.askopenfile(filetypes=[("Text Documents", "*.txt")])
    if file:
        exclude_text.delete('1.0', 'end')
        exclude_text.insert('1.0', file.read())
        exclude_text.delete('end -1 chars', 'end')
        file.close()


def icon_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def create_exclude_frame(root):
    tmp = ttk.Frame(root)
    exclude_open_file = ttk.Button(tmp, text="Add Files...",
                                   command=exclude_add_files_dialog)
    exclude_open_dirs = ttk.Button(tmp, text="Add Folder...",
                                   command=exclude_add_dirs_dialog)
    exclude_save = ttk.Button(tmp, text="Save", command=exclude_save_dialog)
    exclude_load = ttk.Button(tmp, text="Load", command=exclude_load_dialog)
    exclude_open_file.pack(expand=True)
    exclude_open_dirs.pack(expand=True)
    exclude_save.pack(expand=True)
    exclude_load.pack(expand=True)

    return tmp


if __name__ == "__main__":
    # Create Tk Root Window
    root = tk.Tk()
    root.title("Y1 Transfer Utility (v1.3.0)")
    root.iconbitmap(icon_path("icon.ico"))

    # Window Size and Positioning
    window_width = 1000
    window_height = 300
    center_x = int((root.winfo_screenwidth() / 2) - (window_width / 2))
    center_y = int((root.winfo_screenheight() / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    root.resizable(True, True)
    root.minsize(window_width, window_height)

    # Window Layout Grid
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=1)
    root.rowconfigure(5, weight=1)
    root.rowconfigure(6, weight=1)
    root.rowconfigure(7, weight=1)
    root.columnconfigure(0, weight=5)
    root.columnconfigure(1, weight=35)
    root.columnconfigure(2, weight=5)
    root.columnconfigure(3, weight=5)
    root.columnconfigure(4, weight=30)
    root.columnconfigure(5, weight=15)

    # Field Variables
    input_file_string = tk.StringVar()
    output_file_string = tk.StringVar()
    convert_bool = tk.BooleanVar()
    copy_embed_cover_bool = tk.BooleanVar()
    folder_icon = tk.PhotoImage(file=icon_path("./folder.png"))

    # Left Half

    # Input Fields (Row 0)
    input_label = ttk.Label(root, text="Input Folder:")
    input_entry = ttk.Entry(root, textvariable=input_file_string)
    input_browse = ttk.Button(root, image=folder_icon, command=input_dialog)
    input_label.grid(column=0, row=0, sticky=tk.E, padx=2)
    input_entry.grid(column=1, row=0, sticky=tk.EW, padx=2)
    input_browse.grid(column=2, row=0, sticky=tk.EW, padx=5)

    # Output Fields (Row 1)
    output_label = ttk.Label(root, text="Output Folder:")
    output_entry = ttk.Entry(root, textvariable=output_file_string)
    output_browse = ttk.Button(root, image=folder_icon, command=output_dialog)
    output_label.grid(column=0, row=1, sticky=tk.E, padx=2)
    output_entry.grid(column=1, row=1, sticky=tk.EW, padx=2)
    output_browse.grid(column=2, row=1, sticky=tk.EW, padx=5)

    # Exclude Fields (Rows 2 - 5)
    exclude_label = ttk.Label(root, text="Exclude:")
    exclude_text = scrolledtext.ScrolledText(
        root, width=1, height=1, wrap="none")
    exclude_label.grid(column=0, row=2, sticky=tk.E, padx=2)
    exclude_text.grid(column=1, columnspan=2, row=2,
                      rowspan=4, sticky=tk.NSEW, padx=2)
    exclude_frame = create_exclude_frame(root)
    exclude_frame.grid(column=0, row=5, sticky=tk.SE, padx=2)

    # Separator
    sep = ttk.Separator(root, orient=tk.VERTICAL)
    sep.grid(column=3, row=0, rowspan=6, sticky=tk.NS, pady=5)

    # Right Half

    # Convert Checkbox (Row 0)
    convert_checkbox = ttk.Checkbutton(
        root, text="Convert music to MP3?", variable=convert_bool
    )
    convert_bool.set(True)
    convert_checkbox.grid(column=4, columnspan=2, row=0, sticky=tk.EW)

    # Embed Cover (Row 1)
    copy_embed_cover_checkbox = ttk.Checkbutton(
        root, text="Copy Embedded Cover? (Conversion Only)", variable=copy_embed_cover_bool)
    copy_embed_cover_bool.set(True)
    copy_embed_cover_checkbox.grid(column=4, columnspan=2, row=1, sticky=tk.EW)

    # Full Span

    # Progress Bar (Row 6)
    progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")
    progress.grid(column=0, columnspan=6, row=6, sticky=tk.EW, padx=5)

    # Status and Start Button (Row 7)
    status_label = ttk.Label(root, text="")
    start_button = ttk.Button(
        root, text="Transfer/Convert", command=start_transfer)
    status_label.grid(column=0, columnspan=3, row=7, sticky=tk.EW, padx=5)
    start_button.grid(column=5, row=7, sticky=tk.EW, padx=5)

    # Start Program
    root.mainloop()
