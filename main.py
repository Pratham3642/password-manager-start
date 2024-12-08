from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    if not website or not password:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        return

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        with open("passwords.json", "w") as file:
            json.dump(new_data, file, indent=4)

    except json.JSONDecodeError:
        with open("passwords.json", "w") as file:
            json.dump(new_data, file, indent=4)

    else:
        data.update(new_data)
        with open("passwords.json", "w") as file:
            json.dump(data, file, indent=4)
    finally:
        messagebox.showinfo(title="Success", message="Password saved successfully.")
        email_entry.delete(0, END)
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        website_entry.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().strip()
    email = email_entry.get().strip()

    if not website:
        messagebox.showinfo(title="Error", message="Please enter the website name.")
        return

    if not email:
        messagebox.showinfo(title="Error", message="Please enter the email.")
        return

    try:
        with open("passwords.json") as file:
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
        return

    except json.JSONDecodeError:
        messagebox.showerror(title="Error", message="Data file is corrupted.")
        return

    # Check if the website is in the data
    if website in data:
        stored_email = data[website]["email"]
        stored_password = data[website]["password"]
        if email == stored_email:
            messagebox.showinfo(title=website, message=f"Email: {stored_email}\nPassword: {stored_password}")
        else:
            messagebox.showinfo(title="Error", message="No details for this website with the provided email.")
    else:
        messagebox.showinfo(title="Error", message=f"No details for {website} exist.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg='#e0f7fa')  # Light blue background for the window

# Logo
canvas = Canvas(window, height=200, width=200, bg='#e0f7fa', highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, pady=20)

# Labels
website_label = Label(text="Website:", bg='#e0f7fa', font=("Arial", 12))
website_label.grid(row=1, column=0, pady=5, sticky=W)
email_label = Label(text="Email/Username:", bg='#e0f7fa', font=("Arial", 12))
email_label.grid(row=2, column=0, pady=5, sticky=W)
password_label = Label(text="Password:", bg='#e0f7fa', font=("Arial", 12))
password_label.grid(row=3, column=0, pady=5, sticky=W)

# Entries
website_entry = Entry(width=33, font=("Arial", 12))
website_entry.grid(row=1, column=1, pady=5)
website_entry.focus()

email_entry = Entry(width=52, font=("Arial", 12))
email_entry.grid(row=2, column=1, columnspan=2, pady=5)

password_entry = Entry(width=31, font=("Arial", 12))
password_entry.grid(row=3, column=1, pady=5)

# Buttons
search_button = Button(text="Search", width=14, command=find_password, font=("Arial", 12, "bold"), bg='#1e90ff',
                       fg='white', padx=10, pady=5, relief="flat")
search_button.grid(row=1, column=2, pady=5)

generate_password_button = Button(text="Generate Password", command=generate_password, font=("Arial", 12, "bold"),
                                  bg='#1e90ff', fg='white', padx=10, pady=5, relief="flat")
generate_password_button.grid(row=3, column=2, pady=5)

add_button = Button(text="Add", width=44, command=save, font=("Arial", 12, "bold"), bg='#32cd32', fg='white', padx=10,
                    pady=5, relief="flat")
add_button.grid(row=4, column=1, columnspan=2, pady=20)

window.mainloop()
