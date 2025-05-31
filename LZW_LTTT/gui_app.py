'''
    Project: LZW Compression & Decompression Tool
    To fulfil the requirement of FIT Course by Pham@PTIT
    Nguyen Thanh Trung - B23DCCN861 - group 12
    Dang Phi Long - B23DCCN497 - group 12
    Tran Trung Kien - B23DCCN469 - group 12
    Pham Anh Tu - B23DCCN875 - group 12   
'''
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from lzw import lzw_compress, lzw_decompress
from file_handler import read_binary_file, write_binary_file, save_compressed_file, load_compressed_file
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import hashlib

batch_stats = []

def compress_file():
    filepath = filedialog.askopenfilename(title="Select file to compress")
    if not filepath:
        return

    try:
        data = read_binary_file(filepath)
        compressed = lzw_compress(data)
        original_ext = os.path.splitext(filepath)[1]
        original_size = len(data)

        # Nhập mật khẩu
        password = simpledialog.askstring("Password", "Nhập mật khẩu để bảo vệ file nén (có thể bỏ trống):", show="*")
        if password is None:
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".lzw", filetypes=[("LZW Compressed", "*.lzw")])
        if not save_path:
            return

        # Truyền mật khẩu
        save_compressed_file(save_path, compressed, original_ext, password)

        compressed_size = os.path.getsize(save_path)
        ratio = 100 * (1 - compressed_size / original_size) if original_size else 0

        # if ratio < 0:
        #     os.remove(save_path)
        #     messagebox.showwarning("⚠️ Compression Ineffective",
        #                            f"File nén ra ({compressed_size} bytes) lớn hơn file gốc ({original_size} bytes).\n"
        #                            f"File .lzw đã bị xoá và không được lưu.")
        #     return

        msg = (f"✅ Compressed: {os.path.basename(filepath)}\n"
               f"Original size: {original_size} bytes\n"
               f"Compressed size: {compressed_size} bytes ({len(compressed)} codes)\n"
               f"Compression ratio: {ratio:.2f}%\n"
               f"Saved to: {save_path}")
        log(msg)
        write_log_file("Compress", msg)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_ratio_chart():
    if not batch_stats:
        messagebox.showinfo("Chart", "Chưa có dữ liệu batch compress để vẽ.")
        return

    names = [entry[0] for entry in batch_stats]
    ratios = [entry[3] for entry in batch_stats]

    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    bars = ax.barh(range(len(names)), ratios)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Compression ratio (%)  –  càng cao càng tốt")
    ax.set_title("Tỷ lệ nén LZW cho từng file")

    for bar, r in zip(bars, ratios):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{r:.2f}%", va="center", fontsize=8)

    chart_win = tk.Toplevel(root)
    chart_win.title("Compression Ratio Chart")

    canvas = FigureCanvasTkAgg(fig, master=chart_win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

def batch_compress():
    global batch_stats
    batch_stats = []

    filepaths = filedialog.askopenfilenames(title="Select multiple files to compress")
    if not filepaths:
        return

    success_count = 0
    for filepath in filepaths:
        try:
            data = read_binary_file(filepath)
            compressed = lzw_compress(data)
            original_ext = os.path.splitext(filepath)[1]
            original_size = len(data)

            filename = os.path.basename(filepath)
            save_dir = os.path.dirname(filepath)
            save_path = os.path.join(save_dir, filename + ".lzw")

            save_compressed_file(save_path, compressed, original_ext)
            compressed_size = os.path.getsize(save_path)
            ratio = 100 * (1 - compressed_size / original_size) if original_size else 0

            if ratio < 0:
                os.remove(save_path)
                log(f"⚠️ Skipped: {filename} (ratio {ratio:.2f} %)")
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            batch_stats.append((filename, original_size, compressed_size, ratio, timestamp))

            msg = (f"📚 Batch Compressed: {filename}\n"
                   f"{original_size} → {compressed_size} bytes  |  {ratio:.2f}%")
            log(msg)
            write_log_file("Batch Compress", msg)
            success_count += 1

        except Exception as e:
            log(f"❌ Error with {filepath}: {str(e)}")

    messagebox.showinfo("Batch Compress Done",
                        f"Nén thành công {success_count} / {len(filepaths)} file.")
    if success_count:
        show_ratio_chart()

def export_csv_report():
    if not batch_stats:
        messagebox.showinfo("Export CSV", "Chưa có dữ liệu batch compress để xuất báo cáo.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Lưu báo cáo CSV"
    )
    if not save_path:
        return

    try:
        with open(save_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["File Name", "Original Size (bytes)", "Compressed Size (bytes)", "Compression Ratio (%)", "Timestamp"])

            for entry in batch_stats:
                filename, original_size, compressed_size, ratio, timestamp = entry
                writer.writerow([filename, original_size, compressed_size, f"{ratio:.2f}", timestamp])

        messagebox.showinfo("Export Successful", f"Báo cáo đã được lưu tại:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))

def decompress_file():
    filepath = filedialog.askopenfilename(title="Select .lzw file", filetypes=[("LZW Files", "*.lzw")])
    if not filepath:
        return

    try:
        ext, compressed, stored_hash = load_compressed_file(filepath)

        if stored_hash != b'\x00' * 32:
            password = simpledialog.askstring("Password", "Nhập mật khẩu để giải nén:", show="*")
            if password is None:
                return
            input_hash = hashlib.sha256(password.encode()).digest()
            if input_hash != stored_hash:
                messagebox.showerror("Sai mật khẩu", "❌ Mật khẩu không chính xác. Không thể giải nén.")
                return

        decompressed = lzw_decompress(compressed)

        save_path = filedialog.asksaveasfilename(
            title="Save decompressed file as",
            defaultextension=ext,
            filetypes=[("Recovered file", "*" + ext)]
        )
        if not save_path:
            return

        write_binary_file(save_path, decompressed)

        msg = (f"✅ Decompressed: {os.path.basename(filepath)}\n"
               f"Compressed codes: {len(compressed)}\n"
               f"Decompressed size: {len(decompressed)} bytes\n"
               f"Saved to: {save_path}")
        log(msg)
        write_log_file("Decompress", msg)
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

def write_log_file(action, content):
    with open("log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {action}\n{content}\n{'-'*60}\n")

# === GUI setup ===
root = tk.Tk()
root.title("🌀 LZW Compression & Decompression Tool")
root.geometry("580x400")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

title_label = tk.Label(root, text="LZW Compressor", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="steelblue")
title_label.pack(pady=10)

btn_frame = tk.Frame(root, bg="#f5f5f5")
btn_frame.pack(pady=10)

btn_compress = tk.Button(btn_frame, text="📦 Compress File", command=compress_file,
                         width=20, height=2, bg="steelblue", fg="white", font=("Consolas", 11))
btn_compress.grid(row=0, column=0, padx=10)

btn_decompress = tk.Button(btn_frame, text="📂 Decompress File", command=decompress_file,
                           width=20, height=2, bg="seagreen", fg="white", font=("Consolas", 11))
btn_decompress.grid(row=0, column=1, padx=10)

btn_batch = tk.Button(btn_frame, text="📚 Batch Compress", command=batch_compress,
                      width=20, height=2, bg="orange", fg="white", font=("Consolas", 11))
btn_batch.grid(row=0, column=2, padx=10)

btn_clear = tk.Button(root, text="🩹 Clear Log", command=clear_log,
                      bg="gray", fg="white", font=("Consolas", 10), width=15)
btn_clear.pack(pady=3)

btn_chart = tk.Button(root, text="📊 Show Chart", command=show_ratio_chart,
                      bg="purple", fg="white", font=("Consolas", 10), width=15)
btn_chart.pack(pady=3)

btn_export_csv = tk.Button(root, text="📄 Export CSV", command=export_csv_report,
                           bg="darkorange", fg="white", font=("Consolas", 10), width=15)
btn_export_csv.pack(pady=3)

log_text = tk.Text(root, wrap="word", height=10, width=68, font=("Consolas", 10), state="disabled", bg="#ffffff")
log_text.pack(pady=10)

root.mainloop()
