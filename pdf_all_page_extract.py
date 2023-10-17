import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import zipfile

def extract_and_zip_pages():
    pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_file:
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP Files", "*.zip")])
    if not save_path:
        return

    try:
        with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            pdf = PyPDF2.PdfReader(pdf_file)

            if pdf.is_encrypted:
                pdf.decrypt("")  # You might need to provide the password if the PDF is encrypted.

            num_pages = len(pdf.pages)

            for page_num in range(num_pages):
                page = pdf.pages[page_num]
                pdf_writer = PyPDF2.PdfWriter()
                pdf_writer.add_page(page)

                output_file = f'page_{page_num + 1}.pdf'
                pdf_writer.write(open(output_file, 'wb'))
                zipf.write(output_file)
                os.remove(output_file)

        messagebox.showinfo("Extraction Complete", f"{num_pages} pages extracted and saved to {save_path} successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the GUI window
window = tk.Tk()
window.title("Semih PDF All Page Extraction")

# Create an "Extract Pages" button
extract_button = tk.Button(window, text="Extract Pages", command=extract_and_zip_pages)
extract_button.pack(pady=20)

window.mainloop()
