import tkinter as tk
from tkinter import messagebox, Text, simpledialog

from members.manage_members import MemberManager
from members.validate_member_details import *
from members.member_storage import MemberStorage
import sqlite3


class MemberManagerGUI:
    def __init__(self, members):

        self.members_window = members
        self.member_manager = MemberManager()

        self.members_window.title("Member Manager")
        self.members_window.geometry("700x500+100+100")

        self.label = tk.Label(members, text="Member Manager options", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        button_width = 25

        self.add_member_button = tk.Button(members, text="Add new member", font=("Arial", 16, "bold"),
                                           width=button_width, command=self.add_new_member)
        self.add_member_button.pack(pady=10)

        self.update_member_button = tk.Button(members, text="Update member profile", font=("Arial", 16, "bold"),
                                              width=button_width, command=self.update_member_profile)
        self.update_member_button.pack(pady=10)

        self.pause_membership_button = tk.Button(members, text="Pause/Renew membership", font=("Arial", 16, "bold"),
                                                 width=button_width, command=self.pause_renew_membership)
        self.pause_membership_button.pack(pady=10)

        self.show_member_id_button = tk.Button(members, text="Show Member ID", font=("Arial", 16, "bold"), width=button_width, command=self.show_member_id)
        self.show_member_id_button.pack(pady=10)

        self.member_storage = MemberStorage()

        self.member_details_text = Text(members, height=10, width=40)
        self.member_details_text.pack()

    def add_new_member(self): # Σε νεο παράθυρο κάνουμε add member
        add_new_member_window = tk.Toplevel(self.members_window)
        add_new_member_window.title("Add New Member")
        add_new_member_window.geometry("700x300+100+100")

        # Ta labels και το data entry του κάθε πεδίου που απαιτείτε για το add member
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
            # Οταν γίνει το data entry των πεδίων γίνετε έλεγχος σε κάθε πεδίο αν δεν βγάλει error κάνει την αποθήκευση
            # Αν βρεί error ενημερώνει για το που έιναι το κάθε error
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

            # Στέλνω τα data entry στο backend γαι το save new member
            self.member_manager.add_new_member(name, address, phone_number, email, age, occupation)

            messagebox.showinfo("Success", "New member added successfully")

            add_new_member_window.destroy()

        save_button = tk.Button(add_new_member_window, text="Save", font=("Arial", 16, "bold"), command=save_member)
        save_button.grid(row=6, column=1, sticky="w")

    def update_member_profile(self):
        member_id = simpledialog.askinteger("ID", "Please enter the member ID:")

        # Φόρτωση του μέλους από τη βάση δεδομένων
        member = self.member_storage.load_member_by_id(member_id)

        if member is None:
            messagebox.showinfo("Error", f"Member with ID {member_id} was not found.")
            return

        # Εμφάνιση των πεδίων του μέλους
        self.member_details_text.delete("1.0", "end")  # Καθαρίζει το περιεχόμενο του παραθύρου κειμένου
        self.member_details_text.insert("1.0", f"Name: {member.get_name()}\n")
        self.member_details_text.insert("end", f"Address: {member.get_address()}\n")
        self.member_details_text.insert("end", f"Phone Number: {member.get_phone_number()}\n")
        self.member_details_text.insert("end", f"Email: {member.get_email()}\n")
        self.member_details_text.insert("end", f"Age: {member.get_age()}\n")
        self.member_details_text.insert("end", f"Occupation: {member.get_occupation()}\n")

        # Ερητήσεις για το πεδίο και την νες τιμή που ΄θέλουμε.Αν δεν δώσουμε τιμή ρωτάει συνέχεια
        field_name = simpledialog.askstring("Field Name", "Please enter the name of the field to update:")
        while field_name is None or field_name == "":
            field_name = simpledialog.askstring("Field Name", "Please enter the name of the field to update:")

        new_value = simpledialog.askstring("New Value", f"Enter the new value for {field_name}:")
        while new_value is None or new_value == "":
            new_value = simpledialog.askstring("New Value", f"Enter the new value for {field_name}:")

        # Αλλαγή του πεδίου μέλους
        setattr(member, field_name.lower(), new_value)

        # Αποθήκευση των αλλαγών στη library.db
        self.member_storage.update_member_entry(member)

        messagebox.showinfo("Success", "Member entry has been updated.")

        # Εμφάνιζει τις νεες Values που δώθηκαν
        self.member_details_text.insert("end",
                                        f"New Value\n{field_name.capitalize()}: {getattr(member, field_name.lower())}\n")

    def pause_renew_membership(self):
        user_id = simpledialog.askstring("ID", "Please enter the User ID:")
        if user_id is None or user_id == "":
            messagebox.showinfo("Error", "User ID cannot be empty.")
            return

        member = self.member_storage.load_member_by_id(user_id)
        if member is None:
            messagebox.showinfo("Error", f"Member with User ID {user_id} was not found.")
            return

        self.member_details_text.delete("1.0", "end")  # Καθαρίζει το περιεχόμενο του κειμένου στο παράθυρο
        self.member_details_text.insert("1.0", f"Name: {member.get_name()}\n")
        self.member_details_text.insert("end", f"Status: {member.get_status()}\n")

        change_status = messagebox.askyesno("Change Status", "Do you want to change the status?")
        if change_status:
            new_status = ""

            def set_status_to_pause():
                nonlocal new_status
                new_status = "Pause"
                change_status_window.destroy()

            def set_status_to_renew():
                nonlocal new_status
                new_status = "Active"
                change_status_window.destroy()

            change_status_window = tk.Toplevel(self.members_window)
            change_status_window.title("New Status")
            change_status_window.geometry("250x200+500+300")

            pause_button = tk.Button(change_status_window, text="Pause", font=("Arial", 16, "bold"),
                                     command=set_status_to_pause)
            pause_button.pack(pady=10)

            renew_button = tk.Button(change_status_window, text="Renew", font=("Arial", 16, "bold"),
                                     command=set_status_to_renew)
            renew_button.pack(pady=10)

            change_status_window.wait_window()

            member.set_status(new_status)
            self.member_storage.update_member_entry(member)

            self.member_details_text.delete("1.0", "end")  # Καθαρίζει το περιεχόμενο του κειμένου στο παράθυρο
            self.member_details_text.insert("1.0", f"Name: {member.get_name()}\n")
            self.member_details_text.insert("end", f"Status: {member.get_status()}\n")
            messagebox.showinfo("Success", "Member status has been updated.")

    def show_member_id(self):
        #Αναζήτηση στην βάση με το ονομα του user ωστε να εμφανίσει το ID του
        self.member_name = simpledialog.askstring("Name", "Please enter the Name:")
        self.name_to_search()

    def name_to_search(self):
        search_by_name = self.member_name

        conn = sqlite3.connect('./library.db')
        cursor = conn.cursor()
        query = "SELECT name, member_id FROM members WHERE name = ?"
        cursor.execute(query, (search_by_name,))
        results = cursor.fetchall()

        if not results:
            messagebox.showinfo("No Results", f"No member with the name '{search_by_name}' was found.")
        else:
            result_text = ""
            for row in results:
                result_text += "Name: " + row[0] + "\n"
                result_text += "Member ID: " + str(row[1]) + "\n"
                result_text += "--------------------\n"

            self.member_details_text.delete("1.0", "end")
            self.member_details_text.insert("1.0", result_text)

        conn.close()
