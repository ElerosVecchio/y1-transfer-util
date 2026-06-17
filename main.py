import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
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


def icon_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    # Create Tk Root Window
    root = tk.Tk()
    root.title("Y1 Transfer Utility (v1.1.0)")
    root.iconbitmap(icon_path("icon.ico"))

    # Window Size and Positioning
    window_width = 600
    window_height = 150
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
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=4)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)

    # Field Variables
    input_file_string = tk.StringVar()
    output_file_string = tk.StringVar()
    convert_bool = tk.BooleanVar()
    copy_embed_cover_bool = tk.BooleanVar()

    # Input Fields (Row 0)
    input_label = ttk.Label(root, text="Input Folder:")
    input_entry = ttk.Entry(root, textvariable=input_file_string)
    input_browse = ttk.Button(root, text="Browse", command=input_dialog)
    input_label.grid(column=0, row=0, sticky=tk.E, padx=2)
    input_entry.grid(column=1, columnspan=2, row=0, sticky=tk.EW, padx=2)
    input_browse.grid(column=3, row=0, sticky=tk.EW, padx=5)

    # Output Fields (Row 1)
    output_label = ttk.Label(root, text="Output Folder:")
    output_entry = ttk.Entry(root, textvariable=output_file_string)
    output_browse = ttk.Button(root, text="Browse", command=output_dialog)
    output_label.grid(column=0, row=1, sticky=tk.E, padx=2)
    output_entry.grid(column=1, columnspan=2, row=1, sticky=tk.EW, padx=2)
    output_browse.grid(column=3, row=1, sticky=tk.EW, padx=5)

    # Convert Checkbox (Row 2)
    convert_checkbox = ttk.Checkbutton(
        root, text="Convert music to MP3?", variable=convert_bool
    )
    copy_embed_cover_checkbox = ttk.Checkbutton(root, text="Copy Embedded Cover? (Conversion Only)", variable=copy_embed_cover_bool)
    copy_embed_cover_bool.set(True)
    convert_checkbox.grid(column=1, columnspan=1, row=2, sticky=tk.EW)
    copy_embed_cover_checkbox.grid(column=2, columnspan=2, row=2, sticky=tk.EW)

    # Progress Bar (Row 3)
    progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")
    progress.grid(column=0, columnspan=4, row=3, sticky=tk.EW, padx=5)

    # Status and Start Button (Row 4)
    status_label = ttk.Label(root, text="")
    start_button = ttk.Button(root, text="Start", command=start_transfer)
    status_label.grid(column=0, columnspan=3, row=4, sticky=tk.EW, padx=5)
    start_button.grid(column=3, row=4, sticky=tk.EW, padx=5)

    # Start Program
    root.mainloop()
