import tkinter as tk
from tkinter import ttk, messagebox, filedialog  # Added filedialog import
import random
import string
import os

def password_strength(password):
    """Rates password strength based on length and character types used."""
    strength = 0
    if len(password) >= 8:
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 1

    if strength == 5:
        return "Strong", 5
    elif strength >= 3:
        return "Medium", strength
    else:
        return "Weak", strength

def suggest_password():
    """Generates a strong password suggestion."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(12))

def update_strength_meter(strength_level):
    """Updates the strength meter based on the password strength and changes color dynamically."""
    strength_meter.config(value=strength_level)
    if strength_level == 5:
        strength_meter_label.config(text="Strong", fg="green")
        strength_meter.config(bg="green")
    elif strength_level >= 3:
        strength_meter_label.config(text="Medium", fg="orange")
        strength_meter.config(bg="orange")
    else:
        strength_meter_label.config(text="Weak", fg="red")
        strength_meter.config(bg="red")

def toggle_password_visibility():
    """Toggles between showing and hiding the password."""
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        eye_button.config(text="👁")  # Icon when visible
    else:
        password_entry.config(show='*')
        eye_button.config(text="🙈")  # Icon when hidden

def check_strength(event=None):
    """Checks the strength of the entered password and updates the UI."""
    password = password_entry.get()
    if not password:
        result_label.config(text="Please enter a password.")
        update_strength_meter(0)
        suggestion_label.config(text="")
        return
    
    strength, strength_level = password_strength(password)
    result_label.config(text=f"Your password strength is: {strength}")
    update_strength_meter(strength_level)
    
    if strength != "Strong":
        suggestion_label.config(text="Click 'Suggest Password' for a strong suggestion.")
    else:
        suggestion_label.config(text="")

def generate_and_display_suggestion():
    """Generates and displays a strong password suggestion."""
    suggestion = suggest_password()
    suggestion_label.config(text=f"Suggested Password: {suggestion}")

def save_password():
    """Saves the suggested password to a file."""
    suggestion = suggestion_label.cget("text").replace("Suggested Password: ", "")
    if suggestion:
        # Open a file dialog to get the filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",  # Default file extension
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],  # File types to show
            title="Save Password As"  # Dialog title
        )
        if filename:  # Check if the user didn't cancel the dialog
            try:
                with open(filename, 'w') as file:
                    file.write(f"Suggested Password: {suggestion}\n")
                messagebox.showinfo("Success", f"Password saved to {filename}")
                suggestion_label.config(text="")  # Clear suggestion after saving
            except Exception as e:
                messagebox.showerror("Error", f"Error saving password: {e}")
        else:
            messagebox.showwarning("Warning", "Save operation was cancelled.")
    else:
        messagebox.showerror("Error", "No password suggestion to save.")

def clear_input():
    """Clears the password entry and resets the strength meter."""
    password_entry.delete(0, tk.END)
    result_label.config(text="")
    suggestion_label.config(text="")
    update_strength_meter(0)

def valid_filename(filename):
    """Checks if the filename is valid."""
    return all(c not in filename for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']) and filename.strip() != ""

# Setup GUI
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x400")
root.configure(bg="#f0f0f0")  # Light gray background

# Set up style
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", font=("Arial", 10), padding=5)

# Main Frame
main_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
main_frame.grid(row=0, column=0, sticky="nsew")

# Password Label
password_label = ttk.Label(main_frame, text="Enter your password:", font=("Arial", 12))
password_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

# Password Frame (for password entry and eye icon)
password_frame = ttk.Frame(main_frame)
password_frame.grid(row=1, column=0, sticky="w", padx=5, pady=5)

password_entry = ttk.Entry(password_frame, show="*", width=30, font=("Arial", 12))
password_entry.pack(side="left", padx=5)

# Eye button to toggle password visibility
eye_button = ttk.Button(password_frame, text="🙈", command=toggle_password_visibility, width=3)
eye_button.pack(side="left", padx=5)

# Bind typing event to live validation
password_entry.bind("<KeyRelease>", check_strength)

# Strength Meter
strength_meter = ttk.Scale(main_frame, from_=0, to=5, orient="horizontal", length=200)
strength_meter.grid(row=2, column=0, sticky="w", padx=5, pady=5)

# Strength Label
strength_meter_label = ttk.Label(main_frame, text="", font=("Arial", 12))
strength_meter_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)

# Result Label
result_label = ttk.Label(main_frame, text="", font=("Arial", 12))
result_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

# Suggested Password Label
suggestion_label = ttk.Label(main_frame, text="", font=("Arial", 12))
suggestion_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)

# Suggest Password Button
suggest_password_button = ttk.Button(main_frame, text="Suggest Password", command=generate_and_display_suggestion)
suggest_password_button.grid(row=6, column=0, sticky="w", padx=5, pady=5)

# Save File Entry Label (removed)
# file_label = ttk.Label(main_frame, text="Save suggested password to file:", font=("Arial", 12))
# file_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)

# Save Button
save_button = ttk.Button(main_frame, text="Save Password", command=save_password)
save_button.grid(row=9, column=0, sticky="w", padx=5, pady=5)

# Clear Button
clear_button = ttk.Button(main_frame, text="Clear", command=clear_input)
clear_button.grid(row=10, column=0, sticky="w", padx=5, pady=5)

root.mainloop()
