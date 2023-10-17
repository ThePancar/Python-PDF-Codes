import PyPDF2
import tkinter as tk
from tkinter import filedialog

# Function to open a file dialog and get a list of PDF files to merge
def browse_pdf_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    pdf_files_text.delete(1.0, tk.END)
    for file in files:
        pdf_files_text.insert(tk.END, file + '\n')

# Function to merge selected PDF files into a single PDF
def merge_pdfs():
    merged_pdf = PyPDF2.PdfMerger()
    pdf_files = pdf_files_text.get(1.0, tk.END).split('\n')
    for file in pdf_files:
        if file.strip():  # Ignore empty lines
            merged_pdf.append(file)
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    merged_pdf.write(output_path)
    merged_pdf.close()
    status_label.config(text="PDFs merged successfully!")

# Create the main window
root = tk.Tk()
root.title("Semih PDF Merger")  # Set the title

# Create a Text widget to display selected PDF files
pdf_files_text = tk.Text(root, wrap=tk.WORD)
pdf_files_text.pack()
pdf_files_text.config(height=10, width=40)  # You can adjust the height and width as needed

# Create a scrollbar for the Text widget
scrollbar = tk.Scrollbar(root, command=pdf_files_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
pdf_files_text.config(yscrollcommand=scrollbar.set)

# Create buttons for file selection and merging
browse_button = tk.Button(root, text="Browse PDF Files", command=browse_pdf_files)
browse_button.pack()
merge_button = tk.Button(root, text="Merge PDFs", command=merge_pdfs)
merge_button.pack()

# Create a label for displaying status messages
status_label = tk.Label(root, text="")
status_label.pack()

# Start the main loop
root.mainloop()