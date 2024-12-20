import tkinter as tk
from tkinter import messagebox
import pyshorteners


class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Shortener")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")

        # Input Label
        self.label = tk.Label(
            root, text="Enter the URL to shorten:", font=("Helvetica", 12), bg="#2c3e50", fg="white"
        )
        self.label.pack(pady=10)

        # Input Text Field
        self.url_entry = tk.Entry(root, font=("Helvetica", 12), width=40)
        self.url_entry.pack(pady=10)

        # Shorten Button
        self.shorten_button = tk.Button(
            root, text="Shorten URL", font=("Helvetica", 12), bg="#1abc9c", fg="white", command=self.shorten_url
        )
        self.shorten_button.pack(pady=10)

        # Shortened URL Label
        self.shortened_label = tk.Label(
            root, text="Shortened URL will appear here:", font=("Helvetica", 12), bg="#2c3e50", fg="white"
        )
        self.shortened_label.pack(pady=10)

        # Output Text Field (Read-Only)
        self.shortened_url_entry = tk.Entry(
            root, font=("Helvetica", 12), width=40, state="readonly"
        )
        self.shortened_url_entry.pack(pady=10)

        # Copy Button
        self.copy_button = tk.Button(
            root, text="Copy URL", font=("Helvetica", 12), bg="#3498db", fg="white", command=self.copy_url
        )
        self.copy_button.pack(pady=10)

    def shorten_url(self):
        """Shorten the entered URL."""
        long_url = self.url_entry.get()
        if not long_url:
            messagebox.showerror("Error", "Please enter a valid URL!")
            return

        try:
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(long_url)
            self.shortened_url_entry.config(state="normal")
            self.shortened_url_entry.delete(0, tk.END)
            self.shortened_url_entry.insert(0, short_url)
            self.shortened_url_entry.config(state="readonly")
            self.shortened_label.config(text="Shortened URL:")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to shorten URL: {e}")

    def copy_url(self):
        """Copy the shortened URL to the clipboard."""
        short_url = self.shortened_url_entry.get()
        if short_url:
            self.root.clipboard_clear()
            self.root.clipboard_append(short_url)
            self.root.update()
            messagebox.showinfo("Copied", "Shortened URL copied to clipboard!")
        else:
            messagebox.showerror("Error", "No shortened URL to copy!")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()
