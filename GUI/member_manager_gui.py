import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, Text
import sqlite3
from members.manage_members import MemberManager
from members.validate_member_details import *

class MemberManagerGUI:
    def __init__(self, members):

        self.master = members
        self.member_manager = MemberManager()

        self.master.title("Member Manager")
        self.master.geometry("800x300+200+200")

        self.label = tk.Label(members, text="Member Manager options", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.add_member_button = tk.Button(members, text="Add new member", font=("Arial", 16, "bold"),
                                           command=self.add_new_member)
        self.add_member_button.pack(pady=10)

        self.update_member_button = tk.Button(members, text="Update member profile", font=("Arial", 16, "bold"),
                                              command=self.update_member_profile)
        self.update_member_button.pack(pady=10)

        self.renew_membership_button = tk.Button(members, text="Update member profile_backend",
                                                 font=("Arial", 16, "bold"), command=self.update_member_profile_backend)
        self.renew_membership_button.pack(pady=10)

        self.pause_membership_button = tk.Button(members, text="Pause/Renew membership", font=("Arial", 16, "bold"),
                                                 command=self.pause_renew_membership)
        self.pause_membership_button.pack(pady=10)

    def add_new_member(self):
        # Create a new window for adding a member
        add_new_member_window = tk.Toplevel(self.master)
        add_new_member_window.title("Add New Member")
        add_new_member_window.geometry("800x300+200+200")

        # Create labels and entry fields for member information
        name_label = tk.Label(add_new_member_window, text="Name:", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, sticky="w")
        name_entry = tk.Entry(add_new_member_window, width=30)
        name_entry.grid(row=0, column=1)

        address_label = tk.Label(add_new_member_window, text="Address:", font=("Arial", 16, "bold"))
        address_label.grid(row=1, column=0, sticky="w")
        address_entry = tk.Entry(add_new_member_window, width=30)
        address_entry.grid(row=1, column=1)

        phone_label = tk.Label(add_new_member_window, text="Phone Number:", font=("Arial", 16, "bold"))
        phone_label.grid(row=2, column=0, sticky="w")
        phone_entry = tk.Entry(add_new_member_window, width=30)
        phone_entry.grid(row=2, column=1)

        email_label = tk.Label(add_new_member_window, text="Email:", font=("Arial", 16, "bold"))
        email_label.grid(row=3, column=0, sticky="w")
        email_entry = tk.Entry(add_new_member_window, width=30)
        email_entry.grid(row=3, column=1)

        age_label = tk.Label(add_new_member_window, text="Age:", font=("Arial", 16, "bold"))
        age_label.grid(row=4, column=0, sticky="w")
        age_entry = tk.Entry(add_new_member_window, width=30)
        age_entry.grid(row=4, column=1)

        occupation_label = tk.Label(add_new_member_window, text="Occupation:", font=("Arial", 16, "bold"))
        occupation_label.grid(row=5, column=0, sticky="w")
        occupation_entry = tk.Entry(add_new_member_window, width=30)
        occupation_entry.grid(row=5, column=1)

        def save_member():
            # Get the entered information
            name = name_entry.get()
            if not validate_name(name):
                messagebox.showerror("Error",
                                     "Invalid name. Name must contain only valid characters: letters, spaces and dots in case of middle names")
                return

            address = address_entry.get()

            phone_number = phone_entry.get()
            if not validate_phone_number(phone_number):
                messagebox.showerror("Error",
                                     "Invalid Phone Number. Ensure that the phone number consists of digits, spaces, hyphens and optionally a country code (such as +30)")
                return

            email = email_entry.get()
            if not validate_email(email):
                messagebox.showerror("Error",
                                     "Invalid email address  Acceptable mail forms olny such as: \n'name@domain.tld'\n'name-surname@domain.tld'\n'name.surname@domain.tld'\n'name123@domain.tld'")
                return

            age = age_entry.get()
            if not validate_age(age):
                messagebox.showerror("Error", "Invalid age \nAge must be a integer number between 3 and 105")
                return

            occupation = occupation_entry.get()
            if not validate_occupation(occupation):
                messagebox.showerror("Error", "Occupation can`t be empty")
                return

            # Save the new member
            self.member_manager.add_new_member(name, address, phone_number, email, age, occupation)

            # Show a success message
            messagebox.showinfo("Success", "New member added successfully")

            # Close the window
            add_new_member_window.destroy()

        save_button = tk.Button(add_new_member_window, text="Save", font=("Arial", 16, "bold"), command=save_member)
        save_button.grid(row=6, column=1, sticky="w")

    def update_member_profile(self):
        add_new_member_window = tk.Toplevel(self.master)
        add_new_member_window.title("Update Member Profile")
        add_new_member_window.geometry("800x800+200+200")

        member_id_label = tk.Label(add_new_member_window, text="Memebr ID:", font=("Arial", 16, "bold"))
        member_id_label.grid(row=0, column=0, sticky="w")
        member_id_entry = tk.Entry(add_new_member_window, width=30)
        member_id_entry.grid(row=0, column=1)

        def search_member():
            # db connect
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # get member id
            member_id = member_id_entry.get()

            # get rows from database where member_id = member_id
            cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
            rows = cursor.fetchall()

            # check if the member exists
            if rows:
                #
                y_position = 100

                #
                fields = ['name', 'address', 'phone_number', 'email', 'age', 'occupation', 'status']
                text_boxes = []
                for row in rows:
                    for field, value in zip(fields, row[1:]):
                        label_field = Label(add_new_member_window, text=field)
                        label_field.place(x=50, y=y_position)
                        y_position += 30

                        text_box = Text(add_new_member_window, height=2, width=30)
                        text_box.place(x=150, y=y_position)
                        text_box.insert('end', str(value))
                        text_boxes.append(text_box)
                        y_position += 30

                #
                button_save = Button(add_new_member_window, text="Αποθήκευση",
                                     command=lambda: save_changes(rows, text_boxes))
                button_save.place(x=150, y=y_position + 30)

            # Add a message for no members found
            # else:

            # close db
            conn.close()

        def save_changes(rows, text_boxes):
            # db connect
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # update members fileds
            fields = ['name', 'address', 'phone_number', 'email', 'age', 'occupation', 'status']
            for row, text_box in zip(rows, text_boxes):
                member_id = row[0]
                values = [text_box.get("1.0", "end-1c"), row[2], row[7]] + list(row[3:7])

                cursor.execute(
                    "UPDATE members SET {} WHERE member_id = ?".format(','.join(f'{field}=?' for field in fields[0:])),
                    values + [member_id])

            # db commit and close
            conn.commit()
            conn.close()

        search_button = tk.Button(add_new_member_window, text="Search", font=("Arial", 16, "bold"),
                                  command=search_member)
        search_button.grid(row=2, column=1, sticky="w")

    def update_member_profile_backend(self):
        pass
        # member_id = self.get_member_id()
        # if member_id is not None:
        #     try:
        #         self.member_manager.manage_membership(renew=True)
        #         messagebox.showinfo("Success", "Membership successfully renewed!")
        #     except Exception as e:
        #         messagebox.showerror("Error", str(e))

    def pause_renew_membership(self):
        pass
        # member_id = self.get_member_id()
        # if member_id is not None:
        #     try:
        #         self.member_manager.manage_membership(renew=False)
        #         messagebox.showinfo("Success", "Membership paused successfully!")
        #     except Exception as e:
        #         messagebox.showerror("Error", str(e))

    def get_member_id(self):
        pass
        # member_id = simpledialog.askinteger("Member ID", "Please enter Member ID:")
        # return member_id
