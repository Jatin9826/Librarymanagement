import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, scrolledtext
import issue_return
import random
import datetime
from tkinter.font import Font

# Custom color scheme
BG_COLOR = "#f0f8ff"  # Alice Blue
BUTTON_COLOR = "#4682b4"  # Steel Blue
BUTTON_ACTIVE_COLOR = "#5f9ea0"  # Cadet Blue
TEXT_COLOR = "#2f4f4f"  # Dark Slate Gray
HEADER_COLOR = "#2e8b57"  # Sea Green

books = []
issued_books = []

issue_return.set_shared_data(books, issued_books)

root = tk.Tk()
root.title("Library Management System")
root.geometry("800x650")
root.resizable(True, True)
root.configure(bg=BG_COLOR)

# Custom fonts
title_font = Font(family="Helvetica", size=16, weight="bold")
button_font = Font(family="Arial", size=10, weight="bold")
text_font = Font(family="Courier New", size=10)

# Header Frame
header_frame = tk.Frame(root, bg=HEADER_COLOR, padx=10, pady=10)
header_frame.pack(fill=tk.X)

tk.Label(
    header_frame, 
    text="📚 Library Management System", 
    font=title_font, 
    bg=HEADER_COLOR, 
    fg="white"
).pack(side=tk.LEFT)

# Main Content Frame
main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Function to display output in a scrollable text area
output_area = scrolledtext.ScrolledText(
    main_frame, 
    wrap=tk.WORD, 
    width=80, 
    height=20,
    font=text_font,
    bg="white",
    fg=TEXT_COLOR,
    padx=10,
    pady=10,
    relief=tk.GROOVE,
    bd=2
)
output_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

def display_output(text):
    output_area.config(state=tk.NORMAL)
    output_area.delete(1.0, tk.END)
    output_area.insert(tk.END, text)
    output_area.config(state=tk.DISABLED)

# Auto-generate sample books
def generate_sample_books(n):
    sample_titles = [
        "Python Crash Course", "Clean Code", "Data Structures", "AI Basics",
        "Computer Networks", "OS Concepts", "C Programming", "Java Essentials",
        "Deep Learning", "Web Dev 101", "JavaScript Guide", "React Quickstart",
        "Node.js Basics", "SQL Essentials", "Pragmatic Programmer",
        "Git Handbook", "Algo Mastery", "System Design", "Cloud Computing", "Ethical Hacking"
    ]
    sample_authors = [
        "Eric Matthes", "Robert Martin", "Narasimha K", "Stuart Russell",
        "A. Tanenbaum", "Silberschatz", "B. Kernighan", "Kathy Sierra",
        "Ian Goodfellow", "Jon Duckett", "D. Crockford", "Mark Thomas",
        "M. Casciaro", "Ben Forta", "Andrew Hunt",
        "R. Silverman", "T. Cormen", "D. Patterson", "J. Rhoton", "Rafay Baloch"
    ]
    books_data = []
    for i in range(n):
        book_id = f"B{100 + i}"
        title = random.choice(sample_titles)
        author = random.choice(sample_authors)
        books_data.append({
            "id": book_id,
            "title": title,
            "author": author,
            "available": True
        })
    return books_data

# Add Books
def add_books_gui():
    try:
        count = simpledialog.askinteger("Add Books", "How many books?", parent=root)
        if count is None:  # User clicked cancel
            return
            
        mode = simpledialog.askstring("Mode", "Type 'manual' or 'auto'", parent=root)
        if mode is None:  # User clicked cancel
            return
            
        mode = mode.lower()

        if mode == 'auto':
            new_books = generate_sample_books(count)
            added = 0
            for book in new_books:
                if any(b["id"] == book["id"] for b in books):
                    continue
                books.append(book)
                added += 1
            messagebox.showinfo("Success", f"{added} books added automatically.")
        elif mode == 'manual':
            for i in range(count):
                book_id = simpledialog.askstring("Manual Entry", "Enter Book ID:", parent=root)
                if book_id is None:  # User clicked cancel
                    continue
                    
                title = simpledialog.askstring("Manual Entry", "Enter Title:", parent=root)
                if title is None:  # User clicked cancel
                    continue
                    
                author = simpledialog.askstring("Manual Entry", "Enter Author:", parent=root)
                if author is None:  # User clicked cancel
                    continue
                    
                if any(b["id"] == book_id for b in books):
                    messagebox.showwarning("Duplicate", f"Book ID {book_id} already exists.")
                    continue
                books.append({
                    "id": book_id,
                    "title": title,
                    "author": author,
                    "available": True
                })
            messagebox.showinfo("Done", f"{count} books added.")
        else:
            messagebox.showerror("Error", "Invalid mode")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Remove Book
def remove_book_gui():
    book_id = simpledialog.askstring("Remove Book", "Enter Book ID to remove:", parent=root)
    if book_id is None:  # User clicked cancel
        return
        
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            messagebox.showinfo("Removed", f"Book {book_id} removed.")
            return
    messagebox.showwarning("Not Found", "Book not found.")

# List Books
def list_books_gui():
    if not books:
        display_output("📂 No books in the library.")
        return
    output = "\n📚 Library Books:\n\n"
    for book in books:
        status = "✅ Available" if book["available"] else "❌ Issued"
        output += f"📖 ID: {book['id']}\nTitle: {book['title']}\nAuthor: {book['author']}\nStatus: {status}\n{'─'*50}\n"
    display_output(output)

# Issue Book GUI
def issue_book_gui():
    book_id = simpledialog.askstring("Issue Book", "Enter Book ID:", parent=root)
    if book_id is None:  # User clicked cancel
        return
        
    student_name = simpledialog.askstring("Issue Book", "Enter Student Name:", parent=root)
    if student_name is None:  # User clicked cancel
        return
        
    for book in books:
        if book["id"] == book_id:
            if not book["available"]:
                messagebox.showwarning("Unavailable", "Book is already issued.")
                return
            book["available"] = False
            issue_date = datetime.date.today().strftime("%d-%m-%Y")
            issued_books.append({
                "book_id": book_id,
                "student_name": student_name,
                "issue_date": issue_date
            })
            messagebox.showinfo("Issued", f"Book {book_id} issued to {student_name} on {issue_date}.")
            return
    messagebox.showerror("Not Found", "Book ID not found.")

# Return Book GUI
def return_book_gui():
    book_id = simpledialog.askstring("Return Book", "Enter Book ID to return:", parent=root)
    if book_id is None:  # User clicked cancel
        return
        
    for record in issued_books:
        if record["book_id"] == book_id:
            issued_books.remove(record)
            for book in books:
                if book["id"] == book_id:
                    book["available"] = True
                    break
            messagebox.showinfo("Returned", f"Book {book_id} returned successfully.")
            return
    messagebox.showerror("Not Found", "Book not found in issued list.")

# View Issued Books
def list_issued_books_gui():
    if not issued_books:
        display_output("📂 No books are currently issued.")
        return
    output = "\n📖 Currently Issued Books:\n\n"
    for record in issued_books:
        output += f"📚 Book ID: {record['book_id']}\n👤 Student: {record['student_name']}\n📅 Issue Date: {record['issue_date']}\n{'─'*50}\n"
    display_output(output)

# Button Frame
button_frame = tk.Frame(main_frame, bg=BG_COLOR)
button_frame.pack(fill=tk.X, pady=(0, 10))

# Style for buttons
style = ttk.Style()
style.configure('TButton', font=button_font, padding=5)

# First row of buttons
btn_add = ttk.Button(
    button_frame, 
    text="➕ Add Books", 
    command=add_books_gui, 
    style='TButton'
)
btn_add.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

btn_remove = ttk.Button(
    button_frame, 
    text="➖ Remove Book", 
    command=remove_book_gui, 
    style='TButton'
)
btn_remove.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

btn_list = ttk.Button(
    button_frame, 
    text="📋 List Books", 
    command=list_books_gui, 
    style='TButton'
)
btn_list.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

# Second row of buttons
btn_issue = ttk.Button(
    button_frame, 
    text="📥 Issue Book", 
    command=issue_book_gui, 
    style='TButton'
)
btn_issue.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

btn_return = ttk.Button(
    button_frame, 
    text="📤 Return Book", 
    command=return_book_gui, 
    style='TButton'
)
btn_return.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

btn_issued = ttk.Button(
    button_frame, 
    text="📑 Issued Books", 
    command=list_issued_books_gui, 
    style='TButton'
)
btn_issued.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# Configure grid weights
for i in range(3):
    button_frame.grid_columnconfigure(i, weight=1)

# Status Bar
status_bar = tk.Label(
    root, 
    text="Ready", 
    bd=1, 
    relief=tk.SUNKEN, 
    anchor=tk.W,
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

def update_status(message):
    status_bar.config(text=message)

# Set initial status
update_status("Library Management System - Ready")

# Make the window responsive
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()