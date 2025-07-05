import tkinter as tk
from tkinter import filedialog, messagebox
from huffman import compress_file, decompress_file
import os
import threading

def run_in_thread(func):
    """Run long task in a separate thread."""
    threading.Thread(target=func).start()

def compress():
    input_path = filedialog.askopenfilename(title="Select .txt file", filetypes=[("Text Files", "*.txt")])
    if not input_path:
        return

    output_path = filedialog.asksaveasfilename(
        title="Save compressed file as",
        defaultextension=".huff",
        filetypes=[("Huffman Compressed Files", "*.huff")]
    )
    if not output_path:
        return

    def task():
        try:
            status_label.config(text="Compressing...")
            root.update()

            original, compressed = compress_file(input_path, output_path)
            ratio = 100 * (1 - compressed / original) if original > 0 else 0

            status_label.config(text="Compression completed!")
            messagebox.showinfo(
                "Compression Successful",
                f"📁 Original Size: {original} bytes\n"
                f"📦 Compressed Size: {compressed} bytes\n"
                f"📉 Compression Ratio: {ratio:.2f}%\n\n"
                f"📂 File saved to: {output_path}"
            )
        except Exception as e:
            status_label.config(text="Compression failed.")
            messagebox.showerror("Error", str(e))

    run_in_thread(task)

def decompress():
    input_path = filedialog.askopenfilename(title="Select .huff file", filetypes=[("Huffman Compressed Files", "*.huff")])
    if not input_path:
        return

    output_path = filedialog.asksaveasfilename(
        title="Save decompressed file as",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if not output_path:
        return

    def task():
        try:
            status_label.config(text="Decompressing...")
            root.update()

            decompress_file(input_path, output_path)
            status_label.config(text="Decompression completed!")
            messagebox.showinfo("Decompression Successful", f"File saved to: {output_path}")
        except Exception as e:
            status_label.config(text="Decompression failed.")
            messagebox.showerror("Error", str(e))

    run_in_thread(task)

# ---------------- GUI Setup ---------------- #
root = tk.Tk()
root.title("Huffman File Compressor")
root.geometry("420x310")
root.configure(bg="#f9f9f9")

tk.Label(
    root,
    text="📦 Huffman File Compressor",
    font=("Helvetica", 16, "bold"),
    bg="#f9f9f9"
).pack(pady=20)

tk.Button(
    root,
    text="📤 Compress .txt File",
    font=("Helvetica", 12),
    command=compress,
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5
).pack(pady=10)

tk.Button(
    root,
    text="📥 Decompress .huff File",
    font=("Helvetica", 12),
    command=decompress,
    bg="#2196F3",
    fg="white",
    padx=10,
    pady=5
).pack(pady=10)

status_label = tk.Label(root, text="", font=("Helvetica", 11), bg="#f9f9f9", fg="#444")
status_label.pack(pady=20)

tk.Label(root, text="Built with by Mihir", bg="#f9f9f9", fg="gray").pack(side="bottom", pady=10)

root.mainloop()
