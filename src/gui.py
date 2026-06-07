import tkinter as tk
from tkinter import filedialog, messagebox
from src.compress import compress_file
from src.verify import decompress_file
from src.strategy import explain_strategy

selected_file = ""


class CompressionGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Dynamic File Compression Utility")
        self.root.geometry("850x600")
        self.root.configure(bg="#f0f0f0")

        title = tk.Label(
            root,
            text="Dynamic File Compression Utility",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0"
        )
        title.pack(pady=15)

        self.file_label = tk.Label(
            root,
            text="No file selected",
            font=("Arial", 10),
            wraplength=800,
            bg="#f0f0f0"
        )
        self.file_label.pack(pady=10)

        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        browse_btn = tk.Button(
            button_frame,
            text="Browse File",
            width=20,
            command=self.browse_file
        )
        browse_btn.grid(row=0, column=0, padx=10)

        compress_btn = tk.Button(
            button_frame,
            text="Compress",
            width=20,
            command=self.compress_selected
        )
        compress_btn.grid(row=0, column=1, padx=10)

        decompress_btn = tk.Button(
            button_frame,
            text="Decompress",
            width=20,
            command=self.decompress_selected
        )
        decompress_btn.grid(row=0, column=2, padx=10)

        self.output = tk.Text(
            root,
            width=100,
            height=25,
            font=("Consolas", 10)
        )
        self.output.pack(pady=20)

    def browse_file(self):

        global selected_file

        selected_file = filedialog.askopenfilename()

        if selected_file:
            self.file_label.config(text=selected_file)

    def compress_selected(self):

        global selected_file

        if not selected_file:
            messagebox.showwarning(
                "Warning",
                "Please select a file first."
            )
            return

        try:

            report = explain_strategy(selected_file)

            result = compress_file(selected_file)

            self.output.delete(1.0, tk.END)

            self.output.insert(
                tk.END,
                "========== COMPRESSION REPORT ==========\n\n"
            )

            self.output.insert(
                tk.END,
                f"File Type       : {report['mime']}\n"
            )

            self.output.insert(
                tk.END,
                f"Entropy         : {report['entropy']}\n"
            )

            self.output.insert(
                tk.END,
                f"Text Ratio      : {report['text_ratio']}\n"
            )

            self.output.insert(
                tk.END,
                f"Selected Codec  : {report['codec']}\n"
            )

            self.output.insert(
                tk.END,
                f"Reason          : {report['reason']}\n"
            )

            self.output.insert(
                tk.END,
                f"Compression Lvl : {report['level']}\n\n"
            )

            self.output.insert(
                tk.END,
                f"Output File     : {result['output']}\n"
            )

            self.output.insert(
                tk.END,
                f"Original Size   : {result['original_size']} bytes\n"
            )

            self.output.insert(
                tk.END,
                f"Compressed Size : {result['compressed_size']} bytes\n"
            )

            self.output.insert(
                tk.END,
                f"Space Saved     : {result['ratio']}%\n"
            )

            self.output.insert(
                tk.END,
                "\n✓ Compression Successful"
            )

        except Exception as e:

            messagebox.showerror(
                "Compression Error",
                str(e)
            )

    def decompress_selected(self):

        global selected_file

        if not selected_file:
            messagebox.showwarning(
                "Warning",
                "Please select a compressed file."
            )
            return

        try:

            output_file = decompress_file(selected_file)

            self.output.delete(1.0, tk.END)

            self.output.insert(
                tk.END,
                "========== DECOMPRESSION REPORT ==========\n\n"
            )

            self.output.insert(
                tk.END,
                f"Recovered File:\n\n{output_file}\n\n"
            )

            self.output.insert(
                tk.END,
                "✓ Decompression Successful"
            )

        except Exception as e:

            messagebox.showerror(
                "Decompression Error",
                str(e)
            )


def launch_gui():

    root = tk.Tk()

    app = CompressionGUI(root)

    root.mainloop()