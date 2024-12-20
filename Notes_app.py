import tkinter as tk
from tkinter import messagebox
import json

# File to store notes
NOTES_FILE = "notes.json"

# Load notes from the file or return an empty dictionary
def load_notes():
    try:
        with open(NOTES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save notes to the file
def save_notes(notes):
    with open(NOTES_FILE, 'w') as file:
        json.dump(notes, file, indent=4)

# Add a new note
def add_note():
    title = title_entry.get()
    content = content_entry.get("1.0", tk.END).strip()

    if not title or not content:
        messagebox.showwarning("Warning", "Title and content cannot be empty!")
        return

    notes = load_notes()
    if title in notes:
        messagebox.showerror("Error", "A note with this title already exists!")
    else:
        notes[title] = content
        save_notes(notes)
        messagebox.showinfo("Success", "Note added successfully!")
        clear_inputs()

# View all notes
def view_notes():
    notes = load_notes()
    if not notes:
        messagebox.showinfo("Info", "No notes available!")
    else:
        notes_text = "\n".join(f"{title}: {content}" for title, content in notes.items())
        notes_window = tk.Toplevel(app)
        notes_window.title("All Notes")
        notes_label = tk.Text(notes_window, wrap=tk.WORD, width=50, height=20)
        notes_label.insert(tk.END, notes_text)
        notes_label.config(state=tk.DISABLED)
        notes_label.pack()

# Edit an existing note
def edit_note():
    title = title_entry.get()
    content = content_entry.get("1.0", tk.END).strip()

    if not title:
        messagebox.showwarning("Warning", "Enter a title to edit!")
        return

    notes = load_notes()
    if title in notes:
        notes[title] = content
        save_notes(notes)
        messagebox.showinfo("Success", "Note updated successfully!")
        clear_inputs()
    else:
        messagebox.showerror("Error", "Not found!")

# Delete a note
def delete_note():
    title = title_entry.get()
    if not title:
        messagebox.showwarning("Warning", "Enter a title to delete!")
        return

    notes = load_notes()
    if title in notes:
        del notes[title]
        save_notes(notes)
        messagebox.showinfo("Success", "Note deleted successfully!")
        clear_inputs()
    else:
        messagebox.showerror("Error", "Not Found!")

# Clear input fields
def clear_inputs():
    title_entry.delete(0, tk.END)
    content_entry.delete("1.0", tk.END)

# Create main window
app = tk.Tk()
app.title("Notes App")
app.geometry("600x600")

# Title input
title_label = tk.Label(app, text="Title:")
title_label.pack()
title_entry = tk.Entry(app, width=40)
title_entry.pack()

# Content input
content_label = tk.Label(app, text="Content:")
content_label.pack()
content_entry = tk.Text(app, wrap=tk.WORD, width=50, height=20)
content_entry.pack()

# Buttons
add_button = tk.Button(app, text="Add Note", command=add_note)
add_button.pack(pady=5)

view_button = tk.Button(app, text="View Notes", command=view_notes)
view_button.pack(pady=5)

edit_button = tk.Button(app, text="Edit Note", command=edit_note)
edit_button.pack(pady=5)

delete_button = tk.Button(app, text="Delete Note", command=delete_note)
delete_button.pack(pady=5)

# Run the application
app.mainloop()
