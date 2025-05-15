import tkinter as tk
from tkinter import filedialog, messagebox
from lzw import lzw_compress, lzw_decompress
from file_handler import read_binary_file, write_binary_file, save_compressed_file, load_compressed_file
import os

def compress_file():
    filepath = filedialog.askopenfilename(title="Select file to compress")
    if not filepath:
        return

    try:
        data = read_binary_file(filepath)
        compressed = lzw_compress(data)
        original_ext = os.path.splitext(filepath)[1]

        save_path = filedialog.asksaveasfilename(defaultextension=".lzw", filetypes=[("LZW Compressed", "*.lzw")])
        if not save_path:
            return

        save_compressed_file(save_path, compressed, original_ext)

        log(f"✅ Compressed: {os.path.basename(filepath)}\n"
            f"Original size: {len(data)} bytes\n"
            f"Compressed codes: {len(compressed)}\n"
            f"Saved to: {save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decompress_file():
    filepath = filedialog.askopenfilename(title="Select .lzw file", filetypes=[("LZW Files", "*.lzw")])
    if not filepath:
        return

    try:
        ext, compressed = load_compressed_file(filepath)
        decompressed = lzw_decompress(compressed)

        save_path = filedialog.asksaveasfilename(
            title="Save decompressed file as",
            defaultextension=ext,
            filetypes=[("Recovered file", "*" + ext)]
        )
        if not save_path:
            return

        write_binary_file(save_path, decompressed)

        log(f"✅ Decompressed: {os.path.basename(filepath)}\n"
            f"Compressed codes: {len(compressed)}\n"
            f"Decompressed size: {len(decompressed)} bytes\n"
            f"Saved to: {save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def log(message):
    log_text.configure(state="normal")
    log_text.insert("end", message + "\n\n")
    log_text.configure(state="disabled")
    log_text.see("end")

def clear_log():
    log_text.configure(state="normal")
    log_text.delete("1.0", "end")
    log_text.configure(state="disabled")

# === GUI setup ===
root = tk.Tk()
root.title("🌀 LZW Compression & Decompression Tool")
root.geometry("580x400")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

title_label = tk.Label(root, text="LZW Compressor", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="steelblue")
title_label.pack(pady=10)

# Buttons frame
btn_frame = tk.Frame(root, bg="#f5f5f5")
btn_frame.pack(pady=10)

btn_compress = tk.Button(btn_frame, text="📦 Compress File", command=compress_file,
                         width=20, height=2, bg="steelblue", fg="white", font=("Consolas", 11))
btn_compress.grid(row=0, column=0, padx=10)

btn_decompress = tk.Button(btn_frame, text="📂 Decompress File", command=decompress_file,
                           width=20, height=2, bg="seagreen", fg="white", font=("Consolas", 11))
btn_decompress.grid(row=0, column=1, padx=10)

btn_clear = tk.Button(root, text="🧹 Clear Log", command=clear_log,
                      bg="gray", fg="white", font=("Consolas", 10), width=15)
btn_clear.pack(pady=5)

# Log display area
log_text = tk.Text(root, wrap="word", height=10, width=68, font=("Consolas", 10), state="disabled", bg="#ffffff")
log_text.pack(pady=10)

root.mainloop()
