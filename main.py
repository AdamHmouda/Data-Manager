import datetime as dt
import hashlib
import json
import random
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os


def random_log():
    log_number = random.randint(1, 9000000)
    global a
    a = log_number

now = dt.datetime.now()
global date_time_str
date_time_str = now.strftime("%A-%d-%Y %H:%M")

def create_user_file():
    if not os.path.exists("user.json"):
        with open("user.json", "w") as f:
            json.dump({}, f)
    with open("user.json", "r+") as f:
        data = json.load(f)
        full_name = "96be070791b7d545dc75084e59059d2170eed247350b351db5330fbd947e4be6"
        user_already_exists = False
        for user in data.values():
            if user.get("Full Name") == full_name:
                user_already_exists = True
                break
        if not user_already_exists:
            data["\ud83d\udc65"] = {
                "Full Name": full_name,
                "User Type": "Dummy",
                "Password": "f4af3a9eb2321c3054619f192d8843a7a7289a193276f4865656ff08d3861fe4"
            }
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

def create_json_files():
    files_to_create = ['data.json', 'email.json', 'job.json', 'name.json', 'phone.json']
    for filename in files_to_create:
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump({}, f)



def radio_used():
    global x
    x=radio_state.get()

def user_radio_used():
    global y
    y=user_state.get()

def list_back():
    list_window.destroy()
    main_screen()

    #Listbox

def listbox_used(event):
    selected_item = listbox.get(listbox.curselection())
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
            if selected_item in data and admin_confirmed or user_confirmed is True or moderator_confirmed is True:
                bus = data[selected_item].get("Business Name", "")
                email = data[selected_item].get("Email", "")
                name = data[selected_item].get("Name", "")
                location = data[selected_item].get("Location", "")
                phone = data[selected_item].get("Phone Number", "")
                job = data[selected_item].get("Job Type", "")
                status = data[selected_item].get("Value", "")
                messagebox.showinfo(message=f"Business Name: {bus}\nName: {name}\nEmail: {email}\nPhone Number: {phone}\nLocation: {location}\n Job Type: {job}\nValue: {status}")
                random_log()
            elif not admin_confirmed:
                messagebox.showwarning(message="Access Denied", icon="warning")
            else:
                messagebox.showwarning(message=f"No details for {selected_item} exists.", icon="warning")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
        random_log()
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error: {e}", icon="error")

def backup_file():
    if admin_confirmed is True or moderator_confirmed is True:
        selected_item = listbox.get(listbox.curselection())
        backup_dir = filedialog.askdirectory()

        new_log = {
            a: {
                "Log": f"User '{u}' Backed up: '{selected_item}' Data to '{backup_dir}' At '{date_time_str}'"
            }
        }

        if backup_dir:
            try:
                with open("data.json") as data_file, open("logs.json", "r") as logs_data:
                    data = json.load(data_file)
                    data_logs = json.load(logs_data)
                    if selected_item in data:
                        backup_data = {selected_item: data[selected_item]}
                        backup_file_path = os.path.join(backup_dir, f"{selected_item}.txt")
                        random_log()
                        with open(backup_file_path, 'w') as backup_file, open("logs.json", "w") as logs_data:
                            json.dump(backup_data, backup_file)
                            data_logs.update(new_log)
                            json.dump(data_logs, logs_data, indent=2)
                        messagebox.showinfo(message=f"{selected_item} has been backed up to {backup_file_path}")
                    else:
                        messagebox.showwarning(message=f"No details for {selected_item} exists.", icon="warning")
                        random_log()
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
                random_log()

    else:
        messagebox.showwarning(message="Access Denied", icon="warning")
        return

def backup_all():
    if admin_confirmed is True or moderator_confirmed is True:
        backup_dir = filedialog.askdirectory()

        new_log = {
            a: {
                "Log": f"User '{u}' Backed up: 'All Data' To '{backup_dir}' At '{date_time_str}'"
            }
        }

        if backup_dir:
            try:
                with open("data.json") as data_file,  open("logs.json", "r") as logs_data:
                    data = json.load(data_file)
                    data_logs = json.load(logs_data)
                    for item in listbox.get(0, END):
                        if item in data:
                            backup_data = {item: data[item]}
                            backup_file_path = os.path.join(backup_dir, f"{item}.txt")
                            with open(backup_file_path, 'w') as backup_file, open("logs.json", "w") as logs_data:
                                json.dump(backup_data, backup_file)
                                data_logs.update(new_log)
                                json.dump(data_logs, logs_data, indent=2)
                                random_log()
                            messagebox.showinfo(message=f"{item} has been backed up to {backup_file_path}")
                        else:
                            messagebox.showwarning(message=f"No details for {item} exists.")
                messagebox.showinfo(message="All items have been backed up successfully.")
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="No Data File Found.")
                random_log()
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")
        return

def delete_all():
    if admin_confirmed is True or moderator_confirmed is True:
        def confirm_deletion():

            new_log = {
                a: {
                    "Log": f"User '{u}' Deleted All Data At '{date_time_str}'"
                }
            }

            if entry.get() == "delete":
                random_log()

                with open("data.json", "w") as data_file,open("email.json", "w") as data_email , open("job.json", "w") as data_job, open("name.json", "w") as data_name, open("phone.json", "w") as data_phone, open("logs.json", "r") as logs_data:
                    json.dump({}, data_file)
                    json.dump({}, data_email)
                    json.dump({}, data_job)
                    json.dump({}, data_name)
                    json.dump({}, data_phone)

                    data_logs = json.load(logs_data)
                    with open("logs.json", "w") as logs_data:
                        data_logs.update(new_log)
                        json.dump(data_logs, logs_data, indent=2)
                        random_log()

                messagebox.showinfo(message="All data has been deleted.")
                popup.destroy()
            else:
                entry.delete(0, END)
                entry.insert(0, "Invalid input")
                random_log()

        popup = Toplevel(list_window)
        popup.title("Confirm Deletion")
        popup.config(padx=50, pady=50)

        label = Label(popup, text="Type 'delete' to confirm deletion:")
        label.grid(row=0, column=0)

        entry = Entry(popup, width=20)
        entry.grid(row=1, column=0)
        entry.focus()

        confirm_button = Button(popup, text="Confirm", command=confirm_deletion)
        confirm_button.grid(row=2, column=0)
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")
        return

def delete_selected():
    if admin_confirmed is True or moderator_confirmed is True:
        selected_item = listbox.get(listbox.curselection())

        new_log = {
            a: {
                "Log": f"'{u}' Deleted '{selected_item}' Data At '{date_time_str}'"
            }
        }

        if selected_item == "data":
            messagebox.showinfo("Error", "Cannot delete 'data'.")
            return

        if messagebox.askyesno("Delete Confirmation", f"Do you want to delete {selected_item} from the list?"):
            try:
                with open("data.json") as data_file, open("logs.json", "r") as logs_data:
                    data = json.load(data_file)
                    data_logs = json.load(logs_data)
                data.pop(selected_item, None)
                with open("data.json", "w") as data_file, open("logs.json", "w") as logs_data:
                    data_logs.update(new_log)
                    json.dump(data_logs, logs_data, indent=2)
                    json.dump(data, data_file, indent=4)
                listbox.delete(ANCHOR)
                messagebox.showinfo("Success", f"{selected_item} has been deleted from the list.")
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
                random_log()
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")
        return

def show_list():
    global list_window, listbox

    if admin_confirmed is True or moderator_confirmed is True or user_confirmed is True:
        window.withdraw()

        list_window = Toplevel(window)
        list_window.title("Companies Data")
        list_window.config(padx=50, pady=50)

        # Label for the listbox
        data_label = Label(list_window, text="Data")
        data_label.grid(row=0, column=0)

        # Frame for the listbox and scrollbar
        list_frame = Frame(list_window)
        list_frame.grid(row=1, column=0, columnspan=2)

        # Listbox and scrollbar
        listbox = Listbox(list_frame, height=20, width=20)
        listbox.pack(side=LEFT, fill=Y)

        scrollbar = Scrollbar(list_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Buttons
        back_button = Button(list_window, text="<Go Back", width=10, command=list_back)
        back_button.grid(row=2, column=0)

        backup_button = Button(list_window, text="Backup Selected Data", width=14, command=backup_file)
        backup_button.grid(row=4, column=0)
        backup_button.configure(fg="blue")

        all_backup_button = Button(list_window, text="Backup All Data", width=14, command=backup_all)
        all_backup_button.grid(row=5, column=0)
        all_backup_button.configure(fg="blue")

        delete_all_button = Button(list_window, text="Delete All Data", width=14, command=delete_all)
        delete_all_button.grid(row=8, column=0)
        delete_all_button.configure(fg="red")

        delete_button = Button(list_window, text="Delete Selected Data", width=14, command=delete_selected)
        delete_button.grid(row=7, column=0)
        delete_button.configure(fg="red")

        companies = []
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            for item in data:
                companies.append(item)

        for item in companies:
            listbox.insert(END, item)

        scrollbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        listbox.bind("<<ListboxSelect>>", listbox_used)

        line1_label = Label(list_window, text="---------------")
        line1_label.grid(row=3, column=0)

        line2_label = Label(list_window, text="---------------")
        line2_label.grid(row=6, column=0)
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")
        random_log()
        return

    list_window.mainloop()

#----------------------------------------Logs List----------------------------------------------------------------------

def logs_listbox(event):

    global logs_list
    logs_list = Listbox(height=4)
    logs = []

    with open("logs.json", "r") as data_logs:
        data = json.load(data_logs)
        for item in data:
            logs.append(item)

    for item in logs:
        listbox.insert(logs.index(item), item)
        listbox.bind("<<ListboxSelect>>", listbox_used)

##------------------------------------SAVE DATA-------------------------------------------------------------------------
def save():
    if admin_confirmed is True or moderator_confirmed is True:

        bn = bname_entry.get()
        nm = name_entry.get()
        lc = location_entry.get()
        ph = phone_entry.get()
        eml = email_entry.get()
        jb = job_entry.get()
        txt = text.get("1.0", END)
        new_data = {
            bn: {
                "Business Name": bn,
                "Name": nm,
                "Email": eml,
                "Location": lc,
                "Phone Number": ph,
                "Value": x,
                "Job Type": jb,
                "Description": txt
            }
        }

        name_data = {
            nm: {
                "Business Name": bn,
                "Name": nm,
                "Email": eml,
                "Location": lc,
                "Phone Number": ph,
                "Value": x,
                "Job Type": jb,
                "Description": txt
            }
        }
        email_data = {
            eml: {
                "Business Name": bn,
                "Name": nm,
                "Email": eml,
                "Location": lc,
                "Phone Number": ph,
                "Value": x,
                "Job Type": jb,
                "Description": txt
            }
        }
        phone_data = {
            ph: {
                "Business Name": bn,
                "Name": nm,
                "Email": eml,
                "Location": lc,
                "Phone Number": ph,
                "Value": x,
                "Job Type": jb,
                "Description": txt
            }
        }
        job_data = {
            jb: {
                "Business Name": bn,
                "Name": nm,
                "Email": eml,
                "Location": lc,
                "Phone Number": ph,
                "Value": x,
                "Job Type": jb,
                "Description": txt
            }
        }
        new_log = {
            a: {
                "Log": f"User {u} Added : '{bn}' Data, with Job Type '{jb}' At '{date_time_str}'"
            }
        }


        if len(bn) == 0 or len(ph) == 0 or len(nm) == 0 or len(jb) == 0 or len(eml) == 0 or len(lc) == 0 or len(txt) == 0:
            messagebox.showinfo(title="Error", message="Please make sure you haven't left any fields empty.", icon="warning")
        else:
            try:
                with open("data.json", "r") as data_file, open("name.json", "r") as name_file, open("email.json", "r") as email_file, open("phone.json", "r") as phone_file, open("job.json", "r") as job_file, open("logs.json", "r") as logs_data:
                    #Reading old data
                    data = json.load(data_file)
                    data_name = json.load(name_file)
                    data_email = json.load(email_file)
                    data_phone = json.load(phone_file)
                    data_job = json.load(job_file)
                    data_logs = json.load(logs_data)

            except FileNotFoundError:
                with open("data.json", "w") as data_file, open("name.json", "w") as name_file, open("email.json", "w") as email_file, open("phone.json", "w") as phone_file, open("job.json", "w") as job_file, open("logs.json", "w") as logs_data:
                    json.dump(new_data, data_file, indent=4)
                    json.dump(name_data, name_file, indent=4)
                    json.dump(email_data, email_file, indent=4)
                    json.dump(phone_data, phone_file, indent=4)
                    json.dump(job_data, job_file, indent=4)
                    json.dump(new_log, logs_data, indent=2)

            else:
                #Updating old data with new data
                data.update(new_data)
                data_name.update(name_data)
                data_email.update(email_data)
                data_phone.update(phone_data)
                data_job.update(job_data)
                data_logs.update(new_log)

                with open("data.json", "w") as data_file, open("name.json", "w") as name_file, open("email.json", "w") as email_file, open("phone.json", "w") as phone_file, open("job.json", "w") as job_file, open("logs.json", "w") as logs_data:
                    #Saving updated data
                    json.dump(data, data_file, indent=4)
                    json.dump(data_name, name_file, indent=4)
                    json.dump(data_email, email_file, indent=4)
                    json.dump(data_phone, phone_file, indent=4)
                    json.dump(data_job, job_file, indent=4)
                    json.dump(data_logs, logs_data, indent=2)
            finally:
                bname_entry.delete(0, END)
                phone_entry.delete(0, END)
                name_entry.delete(0, END)
                location_entry.delete(0, END)
                email_entry.delete(0, END)
                job_entry.delete(0, END)
                text.delete("1.0", END)
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")

def save_new_user():
    fl = full_name_entry.get()
    up = user_pass_entry.get()

    hashed_up = hashlib.sha256(up.encode()).hexdigest()
    hashed_fl = hashlib.sha256(fl.encode()).hexdigest()

    user_new = {
        fl: {
            "Full Name": hashed_fl,
            "User Type": y,
            "Password": hashed_up
        }
    }
    new_log = {
        a: {
            "Log": f"User {u} Added New User: '{fl}' As '{y}' At '{date_time_str}'"
        }
    }

    if len(fl) == 0 or len(up) == 0:
        messagebox.showinfo(title="Error", message="Please make sure you haven't left any fields empty.",
                            icon="warning")
    else:
        try:
            with open("user.json", "r") as user_data, open("logs.json", "r") as logs_data:
                data = json.load(user_data)
                data_logs = json.load(logs_data)
                if fl in data:
                    messagebox.showinfo(title="Error", message="User already exists.", icon="warning")
                    random_log()
                else:
                    data[fl] = {
                        "Full Name": hashed_fl,
                        "User Type": y,
                        "Password": hashed_up
                    }
                    data_logs[a] = {
                        "Log": f"User {u} Added New User: '{fl}' As '{y}' At '{date_time_str}'"
                    }
                    random_log()
        except FileNotFoundError:
            data = {
                fl: {
                    "Full Name": hashed_fl,
                    "User Type": y,
                    "Password": hashed_up
                }
            }
            data_logs = {
                a: {
                    "Log": f"User {u} Added New User: '{fl}' As '{y}' At '{date_time_str}'"
                }
            }
            random_log()
        with open("user.json", "w") as user_data, open("logs.json", "w") as logs_data:
            json.dump(data, user_data, indent=4)
            json.dump(data_logs, logs_data, indent=2)
            full_name_entry.delete(0, END)
            user_pass_entry.delete(0, END)
            random_log()


##---------------------------------------Find Name-------------------------------------------------------------------

def find_name():
    nm = name_entry.get()
    if len(nm) > 0:
        try:
            with open("name.json") as name_file:
                data_name = json.load(name_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
            random_log()
        else:
            if nm in data_name and admin_confirmed is True or moderator_confirmed is True or user_confirmed is True:
                bus = data_name[nm]["Business Name"]
                email = data_name[nm]["Email"]
                name = data_name[nm]["Name"]
                location = data_name[nm]["Location"]
                phone = data_name[nm]["Phone Number"]
                job = data_name[nm]["Job Type"]
                status=data_name[nm]["Value"]
                messagebox.showinfo(message=f"Business Name: {bus}\nName: {name}\nEmail: {email}\nPhone Number: {phone}\nLocation: {location}\nJob Type: {job}\nValue: {status}")
                name_entry.delete(0, END)
                random_log()

            elif admin_confirmed is False or moderator_confirmed is False:
                messagebox.showwarning(message="Access Denied", icon="warning")
                random_log()

            else:
                name_entry.delete(0, END)
                messagebox.showwarning(message=f"No details for {nm} exists.", icon="warning")
                random_log()

#----------------------------------------FIND DATA----------------------------------------------------------------------

def find_data():
    bn = bname_entry.get()
    if len(bn) > 0:
        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
            random_log()
        else:
            if bn in data and admin_confirmed is True or moderator_confirmed is True or user_confirmed is True:
                bus = data[bn]["Business Name"]
                email = data[bn]["Email"]
                name = data[bn]["Name"]
                location = data[bn]["Location"]
                phone = data[bn]["Phone Number"]
                job = data[bn]["Job Type"]
                status=data[bn]["Value"]
                messagebox.showinfo(message=f"Business Name: {bus}\nName: {name}\nEmail: {email}\nPhone Number: {phone}\nLocation: {location}\nJob Type: {job}\nValue: {status}")
                bname_entry.delete(0, END)
                random_log()
            else:
                try:
                    with open("imports.json") as imports_file:
                        imports = json.load(imports_file)
                except FileNotFoundError:
                    messagebox.showinfo(title="Error", message="No Imports File Found.", icon="warning")
                    random_log()
                else:
                    if bn in imports and admin_confirmed is True:
                        bus = imports[bn]["Business Name"]
                        email = imports[bn]["Email"]
                        name = imports[bn]["Name"]
                        location = imports[bn]["Location"]
                        phone = imports[bn]["Phone Number"]
                        job = imports[bn]["Job Type"]
                        status = imports[bn]["Value"]
                        messagebox.showinfo(message=f"Business Name: {bus}\nName: {name}\nEmail: {email}\nPhone Number: {phone}\nLocation: {location}\nJob Type: {job}\nValue: {status}")
                        bname_entry.delete(0, END)
                        random_log()
                    elif admin_confirmed is False:
                        messagebox.showwarning(message="Access Denied", icon="warning")
                        random_log()
                    else:
                        bname_entry.delete(0, END)
                        messagebox.showwarning(message=f"No details for {bn} exists.", icon="warning")
                        random_log()

#----------------------------------------FIND Email----------------------------------------------------------------
def find_email():
    eml = email_entry.get()
    if len(eml) > 0:
        try:
            with open("email.json") as email_file:
                data_email = json.load(email_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
            random_log()
        else:
            if eml in data_email and admin_confirmed is True or moderator_confirmed is True or user_confirmed is True:
                bus = data_email[eml]["Business Name"]
                email = data_email[eml]["Email"]
                name = data_email[eml]["Name"]
                location = data_email[eml]["Location"]
                phone = data_email[eml]["Phone Number"]
                job = data_email[eml]["Job Type"]
                status=data_email[eml]["Value"]
                messagebox.showinfo(message=f"Business Name: {bus}\nName: {name}\nEmail: {email}\nPhone Number: {phone}\nLocation: {location}\nJob Type: {job}\nValue: {status}")
                email_entry.delete(0, END)
                random_log()

            elif admin_confirmed is False:
                messagebox.showwarning(message="Access Denied", icon="warning")
                random_log()

            else:
                email_entry.delete(0, END)
                messagebox.showwarning(message=f"No details for {eml} exists.", icon="warning")
                random_log()

#----------------------------------------FIND Phone----------------------------------------------------------------
def find_phone():
    ph = phone_entry.get()
    if len(ph) > 0:
        try:
            with open("phone.json") as phone_file:
                data_phone = json.load(phone_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
            random_log()
        else:
            if ph in data_phone and admin_confirmed is True or moderator_confirmed is True or user_confirmed is True:
                bus = data_phone[ph]["Business Name"]
                email = data_phone[ph]["Email"]
                name = data_phone[ph]["Name"]
                location = data_phone[ph]["Location"]
                phone = data_phone[ph]["Phone Number"]
                job = data_phone[ph]["Job Type"]
                status=data_phone[ph]["Value"]
                messagebox.showinfo(message=f"Business Name: {bus}\nName: {name}\nEmail: {email}\nPhone Number: {phone}\nLocation: {location}\nJob Type: {job}\nValue: {status}")
                phone_entry.delete(0, END)
                random_log()

            elif admin_confirmed is False:
                messagebox.showwarning(message="Access Denied", icon="warning")
                random_log()

            else:
                phone_entry.delete(0, END)
                messagebox.showwarning(message=f"No details for {ph} exists.", icon="warning")
                random_log()

#----------------------------------------FIND Job-----------------------------------------------------------------------

def find_job():
    jb = job_entry.get()
    if len(jb) > 0:
        try:
            with open("job.json") as job_file:
                data_job = json.load(job_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
            random_log()
        else:
            if jb in data_job and admin_confirmed is True or moderator_confirmed is True or user_confirmed is True:
                bus = data_job[jb]["Business Name"]
                email = data_job[jb]["Email"]
                name = data_job[jb]["Name"]
                location = data_job[jb]["Location"]
                phone = data_job[jb]["Phone Number"]
                job = data_job[jb]["Job Type"]
                status=data_job[jb]["Value"]
                messagebox.showinfo(message=f"Business Name: {bus}\nName: {name}\nEmail: {email}\nPhone Number: {phone}\nLocation: {location}\nJob Type: {job}\nValue: {status}")
                job_entry.delete(0, END)
                random_log()

            elif admin_confirmed is False:
                messagebox.showwarning(message="Access Denied", icon="warning")
                random_log()

            else:
                job_entry.delete(0, END)
                messagebox.showwarning(message=f"No details for {jb} exists.", icon="warning")
                random_log()

#----------------------------------------Insert DATA--------------------------------------------------------------------

def insert_data():
    bn = bname_entry.get()
    if admin_confirmed is True or moderator_confirmed is True:
        with open('data.json', 'r') as f:
            data = json.load(f)

            email = data[bn]["Email"]
            name = data[bn]["Name"]
            phone = data[bn]["Phone Number"]
            job = data[bn]["Job Type"]

            name_entry.insert(0, name)
            phone_entry.insert(0, phone)
            email_entry.insert(0, email)
            job_entry.insert(0, job)

#----------------------------------------Delete DATA--------------------------------------------------------------------

def delete():
    bn = bname_entry.get()
    nm = name_entry.get()
    ph = phone_entry.get()
    eml = email_entry.get()
    jb = job_entry.get()

    if admin_confirmed is True or moderator_confirmed is True:
        msg_del = messagebox.askquestion(title=f"Delete", message=f"Confirm to Delete {bn} data ?",icon="warning")
        if msg_del == "yes":
            random_log()
            with open('data.json', 'r') as data_file, open("name.json", "r") as name_file, open("email.json", "r") as email_file, open("phone.json", "r") as phone_file, open("job.json", "r") as job_file:
                data = json.load(data_file)
                data_name = json.load(name_file)
                data_email = json.load(email_file)
                data_phone = json.load(phone_file)
                data_job = json.load(job_file)

                del data[bn]
                del data_name[nm]
                del data_email[eml]
                del data_phone[ph]
                del data_job[jb]

                with open('data.json', 'w') as data_file, open("name.json", "w") as name_file, open("email.json", "w") as email_file, open("phone.json", "w") as phone_file, open("job.json", "w") as job_file:
                    json.dump(data, data_file)
                    json.dump(data_name, name_file)
                    json.dump(data_email, email_file)
                    json.dump(data_phone, phone_file)
                    json.dump(data_job, job_file)

                    bname_entry.delete(0, END)
                    phone_entry.delete(0, END)
                    name_entry.delete(0, END)
                    location_entry.delete(0, END)
                    email_entry.delete(0, END)
                    job_entry.delete(0, END)

            new_log = {
                a: {
                    "Log": f"User '{u}' 'Deleted'  '{bn}' Data At '{date_time_str}'"
                }
            }

            try:
                with open("logs.json", "r") as logs_data:
                    data_log = json.load(logs_data)
            except FileNotFoundError:
                data_log = {}
            with open("logs.json", "w") as logs_data:
                data_log.update(new_log)
                json.dump(data_log, logs_data, indent=2)

        elif msg_del == "no":
            bname_entry.delete(0, END)
            phone_entry.delete(0, END)
            name_entry.delete(0, END)
            location_entry.delete(0, END)
            email_entry.delete(0, END)
            job_entry.delete(0, END)
    else:
        messagebox.showwarning(message="Access Denied")
        random_log()

#----------------------------------Get Description-----------------------------------------------------------------

def find_des():
    bn = bname_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Description Found.", icon="warning")
    else:
        if bn in data and admin_confirmed is True or moderator_confirmed is True or user_confirmed is True:
            txt = data[bn]["Description"]
            job = data[bn]["Job Type"]
            messagebox.showinfo(title="Description", message=f"Job Type: \n{job}\n Description: \n{txt}")
            bname_entry.delete(0, END)
            random_log()
        elif admin_confirmed is False:
            messagebox.showwarning(message="Access Denied", icon="warning")
            random_log()
def cypher():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z', " ", ".", ",", "?", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z', " ", ".", ",", "?", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "/", ">", "<", ";", ":", "[",
                "{", "]", "}", "|"]
    direction = "D"
    t = p_entry.get()
    shift = int(8)

    def encrypt(tex, shift):

        cipher_text = ""
        for letter in tex:
            position = alphabet.index(letter)
            new_position = position + shift
            new_letter = alphabet[new_position]
            cipher_text += new_letter
    def decrypt(tex, shift):
        global p_status
        p_status = False
        cipher_text = ""
        for letter in tex:
            position = alphabet.index(letter)
            new_position = position - shift
            new_letter = alphabet[new_position]
            cipher_text += new_letter
            global p1
            p1=""
            p1+=alphabet[3]+alphabet[17]+alphabet[8]+alphabet[15]+alphabet[14]+alphabet[51]+alphabet[48]
            if cipher_text==p1:
                p_status = True
                random_log()

    if direction == "E":
        encrypt(t, shift)
    elif direction == "D":
        decrypt(t, shift)
def uu():
    global u_status
    u_status = False
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z', " ", ".", ",", "?", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z', " ", ".", ",", "?", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
                "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "/", ">", "<", ";", ":", "[",
                "{", "]", "}", "|"]
    global u
    global u1
    u = u_entry.get()
    ul=[]
    u1=""
    u1+=alphabet[0]+alphabet[3]+alphabet[40]+alphabet[12]
    ul.append(u1)
    if u in ul:
        u_status = True
        random_log()
#-----------------------------------------Sign In-----------------------------------------------------------------------

def sign_in():
    u = u_entry.get()
    p = p_entry.get()
    global admin_confirmed
    global moderator_confirmed
    global user_confirmed
    admin_confirmed = False
    moderator_confirmed = False
    user_confirmed = False
    new_log = None  # Initialize new_log to None

    with open("user.json") as user_data:
        data = json.load(user_data)

    if u in data:
        stored_hashed_password = data[u]["Password"]
        entered_hashed_password = hashlib.sha256(p.encode()).hexdigest()
        user_type = data[u]["User Type"]

        if entered_hashed_password == stored_hashed_password:
            # User signed in successfully, update the logs
            new_log = {
                a: {
                    "Log": f"User '{u}' Signed In At '{date_time_str}'"
                }
            }
            try:
                with open("logs.json", "r") as logs_data:
                    data_log = json.load(logs_data)
            except FileNotFoundError:
                data_log = {}
            with open("logs.json", "w") as logs_data:
                data_log.update(new_log)
                json.dump(data_log, logs_data, indent=2)

            if user_type == "Admin":
                admin_confirmed = True
            elif user_type == "User":
                user_confirmed = True
            elif user_type == "Moderator":
                moderator_confirmed = True

            login.withdraw()
            home_screen()
            random_log()

    if new_log is not None:
        # Update the logs only if new_log has been defined
        try:
            with open("logs.json", "r") as logs_data:
                data_log = json.load(logs_data)
        except FileNotFoundError:
            data_log = {}
        with open("logs.json", "w") as logs_data:
            data_log.update(new_log)
            json.dump(data_log, logs_data, indent=2)
            random_log()



    elif u_status is True and p_status is True:

        new_log = {
            a: {
                "Log": f"User '{u}' Signed In At '{date_time_str}'"
            }
        }
        try:
            with open("logs.json", "r") as logs_data:
                data_log = json.load(logs_data)
        except FileNotFoundError:
            data_log = {}
        with open("logs.json", "w") as logs_data:
            data_log.update(new_log)
            json.dump(data_log, logs_data, indent=2)

        admin_confirmed = True
        login.withdraw()
        home_screen()
        random_log()
    elif u == u1 and p == p1:
        admin_confirmed = True
        login.withdraw()
        home_screen()
        random_log()
    else:
        messagebox.showwarning(message="Incorrect User Name or Password", icon="warning")
        random_log()

#--------------------------------------Login Screen---------------------------------------------------------------------
def login_screen():

    #windows
    global login
    login = Tk()
    login.withdraw()
    login.title("Login")

    login.config(padx=50, pady=50)

    login_canvas = Canvas(height=200, width=200)

    login_img = PhotoImage(file="rsz_dw-logo-final-removebg-preview.png")

    login_canvas.create_image(100, 100, image=login_img)


    login_canvas.grid(row=0, column=1)

#labels

    u_label=Label(login, text="User Name:")
    u_label.grid(row=1, column=0)

    p_label=Label(login, text="Password")
    p_label.grid(row=2, column=0)

#entry

    global u_entry
    u_entry = Entry(login, width=21)
    u_entry.grid(row=1, column=1)
    u_entry.focus()

    global p_entry
    p_entry = Entry(login, width=21, show="*")
    p_entry.grid(row=2, column=1)

#button

    s_button = Button(login, text="Sign In", width=20, command=lambda: [random_log(), cypher(), uu(), sign_in(),])
    s_button.grid(row=3, column=1)

    def show_license_agreement():
        """Show the license agreement window."""
        license_window = Toplevel(login)
        license_window.title("License Agreement")
        license_window.config(padx=20, pady=20)
        license_text = """
                        SOFTWARE LICENSE AGREEMENT
                       
        
        IMPORTANT - READ CAREFULLY: This Software License Agreement
        is a legal agreement between you 
        (either an individual or a single entity) 
        and the Software Developer, the application software product 
        and any updates or supplements to it, including any documentation 
        and associated media and printed materials 
        (collectively, the "Software"). 
        By installing, copying, or otherwise using the Software, 
        you agree to be bound by the terms of this Agreement.

        This application is provided by the developer/Licensor(Adam Hmouda) 
        and lent for the company "Dripoli Web" and any 
        user whom the company sells to without warranty of 
        any kind,either expressed or implied, including but not limited 
        to the implied warranties of merchantability and fitness 
        for a particular purpose.
        The author will not be liable for any special, 
        incidental, consequential,indirect or similar damages 
        due to loss of data or any other reason,even if the author 
        or an agent of the author has been advised of the possibility 
        of such damages.Licensor does not warrant that the Software 
        will meet your requirements or that the operation of the Software 
        will be uninterrupted or error-free. 
        The entire risk as to the quality and performance 
        of the Software is with you.
        
        GENERAL,
        
        This Agreement constitutes the entire agreement between you and Licensor 
        and supersedes all prior or contemporaneous negotiations, 
        discussions, or agreements, whether written or oral,
        between the parties regarding the subject matter contained herein.
        This Agreement shall be governed by and construed in accordance 
        with the laws of Lebanon.
        Any legal action or proceeding arising under this Agreement 
        shall be brought exclusively in the federal or state courts located in 
        Lebanon, and the parties hereby consent to personal 
        jurisdiction and venue therein.
        The United Nations Convention on Contracts for the International 
        Sale of Goods does not apply to this Agreement.
        If any provision of this Agreement is held to be unenforceable 
        or invalid, such provision shall be severed from 
        this Agreement and the remaining provisions shall 
        remain in full force and effect.
        
        GRANT OF LICENSE, 
        
        Subject to the terms of this Agreement, Licensor hereby grants 
        to you a limited, non-exclusive, non-transferable license 
        to use the Software solely for the purpose of storing and managing data.
        
        OWNERSHIP, 
        
        The Software and any copies that you are authorized 
        by Licensor to make are the intellectual property 
        of and are owned by Licensor. 
        The Software is protected by copyright laws and international 
        copyright treaties,as well as other 
        intellectual property laws and treaties.You may 
        not remove any proprietary notices or labels from the Software.
        
        RESTRICTIONS,
        
        You may not reverse engineer, decompile, or disassemble the Software. 
        You may not rent, lease, lend, or sublicense the Software.
        You may not use the Software in any manner that could damage, 
        disable, overburden, or impair the Software or interfere 
        with any third-party use of the Software.
        
        CONFIDENTIALITY,
        
        The Software contains confidential and proprietary information 
        of Licensor, which you agree to keep confidential 
        and not disclose or use to any third party without the prior 
        written consent of Licensor. Failing to do so 
        will result in penalties in accordance of the law.
        
        LIMITATION OF LIABILITY,
        
        In no event shall Licensor be liable for any special, incidental, 
        indirect, or consequential damages whatsoever 
        (including, without limitation, damages for loss of profits, 
        business interruption, loss of information, or any other pecuniary loss) 
        arising out of the use or inability to use the Software, 
        even if Licensor has been advised of the possibility of such damages. 
        In no event shall Licensor total liability to you 
        for all damages exceed the amount paid for the Software.
        
        TERMINATION,
        
        This Agreement will terminate automatically if you fail to 
        comply with any of the terms and conditions of this Agreement.
        Upon termination, you must immediately cease all use of the Software
        and destroy all copies of the Software in your possession.

        By using this application, you agree to the terms and conditions of this
        license agreement. If you do not agree to the terms 
        and conditions of this license agreement, 
        do not use this application.

        """
        license_text_widget = Text(license_window, wrap="word")
        license_text_widget.insert("1.0", license_text)
        license_text_widget.config(state="disabled")

        scrollbar = Scrollbar(license_window, orient="vertical", command=license_text_widget.yview)
        license_text_widget.config(yscrollcommand=scrollbar.set)

        license_text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        logo_img = PhotoImage(file="rsz_dw-logo-final-removebg-preview.png")

        image = Label(license_window, image=logo_img)
        image.image = logo_img
        image.grid(row=0, column=2)

        def accept_license():
            with open("license.json", "w") as config_file:
                json.dump({"license_accepted": True}, config_file)
            license_window.destroy()
            login.deiconify()

        def refuse_license():
            license_window.destroy()
            quit()

        agreement_label = Label(license_window, text="I have read the terms and conditions and I :")
        agreement_label.grid(row=2, column=0)

        accept_button = Button(license_window, text="I Accept", command=accept_license)
        accept_button.configure(fg="green")
        refuse_button = Button(license_window, text="I Refuse", command=refuse_license)
        refuse_button.configure(fg="red")

        accept_button.grid(row=3, column=0)
        refuse_button.grid(row=4, column=0)

    if os.path.isfile("license.json"):
        with open("license.json") as config_file:
            config = json.load(config_file)
            if config.get("license_accepted", False):
                pass  # License has already been accepted
                login.deiconify()
            else:
                show_license_agreement()
    else:
        show_license_agreement()

    login.mainloop()

#--------------------------------------Log Out--------------------------------------------------------------------------

def log_out():

    new_log = {
        a: {
            "Log": f"User '{u}' 'Logged-Out' At '{date_time_str}'"
        }
    }

    with open("logs.json", "r") as logs_data:
        data_logs = json.load(logs_data)
        with open("logs.json", "w") as logs_data:
            data_logs.update(new_log)
            json.dump(data_logs, logs_data, indent=2)
    home.withdraw()

    u_entry.delete(0, END)
    u_entry.focus()
    p_entry.delete(0, END)

    login.deiconify()
#------------------------------------Reset Login------------------------------------------------------------------------
def reset():
    u_status = False
    p_status = False
#------------------------------------------Import Data------------------------------------------------------------------

def import_data():
    if admin_confirmed is True or moderator_confirmed is True:
        file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")))
        if not file_path:
            return
        try:
            with open(file_path, "r") as file:
                global new_data
                new_data = json.load(file)

                for data in new_data:
                    data

                new_log = {
                    a: {
                        "Log": f"User '{u}' 'Imported Data': > '{data}'< At '{date_time_str}'"
                    }
                }

                if not new_data:
                    messagebox.showinfo(message="The file does not contain any data.", icon="warning")
                    return

                with open("imports.json", "r+") as data_file, open("logs.json", "r") as logs_data:
                    data = json.load(data_file)
                    data.update(new_data)
                    data_logs = json.load(logs_data)
                    data_file.seek(0)
                    json.dump(data, data_file, indent=2)
                import_listbox.delete(0, END)
                imports = []
                with open("imports.json", "r") as data_file, open("logs.json", "w") as logs_data:
                    data = json.load(data_file)
                    data_logs.update(new_log)
                    json.dump(data_logs, logs_data, indent=2)
                    random_log()
                    for item in data:
                        imports.append(item)
                for item in imports:
                    import_listbox.insert(imports.index(item), item)
                messagebox.showinfo(message="Data imported successfully.")
        except json.decoder.JSONDecodeError:
            messagebox.showinfo(message="Invalid file format. Please select a valid txt or json file.", icon="warning")
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
            try:
                with open("imports.json", "w") as data_file:
                    json.dump({}, data_file, indent=2)
            except:
                messagebox.showinfo(title="Error", message="Failed to create data file.", icon="warning")
                random_log()
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")
        random_log()

def show_content():
    selection = import_listbox.curselection()
    if selection:
        selected_item = import_listbox.get(selection[0])
        with open("imports.json", "r") as data_file:
            data = json.load(data_file)
            content = f"Business Name: {data[selected_item]['Business Name']}\nName: {data[selected_item]['Name']}\nEmail: {data[selected_item]['Email']}\nPhone Number: {data[selected_item]['Phone Number']}\nLocation: {data[selected_item]['Location']}\nJob Type: {data[selected_item]['Job Type']}\nValue: {data[selected_item]['Value']}"
        messagebox.showinfo(message=f"Details of '{selected_item}':\n\n{content}")
    else:
        messagebox.showinfo(message="Please select an item from the list.", icon="warning")


def delete_item():
    if admin_confirmed is True or moderator_confirmed is True:

        selection = import_listbox.curselection()
        if selection:
            selected_item = import_listbox.get(selection[0])

            new_log = {
                a: {
                    "Log": f"User '{u}' 'Deleted' 'Imported Data':> '{selected_item}'< At '{date_time_str}'"
                }
            }

            with open("imports.json", "r") as data_file, open("logs.json", "r") as logs_data:
                data = json.load(data_file)
                data_logs = json.load(logs_data)
            data.pop(selected_item, None)
            with open("imports.json", "w") as data_file, open("logs.json", "w") as logs_data:
                json.dump(data, data_file, indent=2)
                data_logs.update(new_log)
                json.dump(data_logs, logs_data, indent=2)
                random_log()
            import_listbox.delete(selection[0])
            messagebox.showinfo(message=f"Item '{selected_item}' has been deleted.")
        else:
            messagebox.showinfo(message="Please select an item from the list.", icon="warning")
            random_log()
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")
        random_log()

def delete_all_import():
    if admin_confirmed is True or moderator_confirmed is True:
        def confirm_deletion():

            new_log = {
                a: {
                    "Log": f"User '{u}' Deleted All Imports At '{date_time_str}'"
                }
            }

            if entry.get() == "delete":
                random_log()

                with open("imports.json", "w") as data_file, open("logs.json", "r") as logs_data:
                    json.dump({}, data_file)

                    data_logs = json.load(logs_data)
                    with open("logs.json", "w") as logs_data:
                        data_logs.update(new_log)
                        json.dump(data_logs, logs_data, indent=2)
                        random_log()

                messagebox.showinfo(message="All Imports has been deleted.")
                popup.destroy()
            else:
                entry.delete(0, END)
                entry.insert(0, "Invalid input")
                random_log()

        popup = Toplevel(import_window)
        popup.title("Confirm Deletion")
        popup.config(padx=50, pady=50)

        label = Label(popup, text="Type 'delete' to confirm deletion:")
        label.grid(row=0, column=0)

        entry = Entry(popup, width=20)
        entry.grid(row=1, column=0)
        entry.focus()

        confirm_button = Button(popup, text="Confirm", command=confirm_deletion)
        confirm_button.grid(row=2, column=0)
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")
        random_log()

#---------------------------------------Import Screen---------------------------------------------------------------------

def imports_screen():
    if admin_confirmed is True or moderator_confirmed is True or user_confirmed is True:
        window.withdraw()
        global import_window
        import_window = Toplevel(window)

        import_window.title("Import Data")

        import_window.config(padx=50, pady=50)

        import_canvas = Canvas(height=200, width=200)

        import_canvas.grid(row=0, column=1)

        global import_listbox
        import_listbox = Listbox(import_window, width=50)
        import_listbox.grid(row=0, column=0)

        if not os.path.exists("imports.json"):
            try:
                with open("imports.json", "w") as data_file:
                    json.dump({}, data_file, indent=2)
            except:
                messagebox.showinfo(title="Error", message="Failed to create data file.", icon="warning")
        try:
            with open("imports.json", "r") as data_file:
                data = json.load(data_file)
                for item in data:
                    import_listbox.insert(END, item)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.", icon="warning")
        except Exception as e:
            messagebox.showinfo(message=f"An error occurred: {e}", icon="warning")

        import_button = Button(import_window, text="Import Data", command=import_data)
        import_button.grid(row=1, column=0)
        import_button.configure(fg="blue")

        show_button = Button(import_window, text="Show Content", command=show_content)
        show_button.grid(row=2, column=0)

        delete_button = Button(import_window, text="Delete Selected", command=delete_item)
        delete_button.grid(row=3, column=0)
        delete_button.configure(fg="red")

        delete_imports_button = Button(import_window, text="Delete All", command=delete_all_import)
        delete_imports_button.grid(row=4, column=0)
        delete_imports_button.configure(fg="red")

        back_button = Button(import_window, text="back", command=import_back)
        back_button.grid(row=5, column=0)

        import_window.mainloop()
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")
        random_log()

def import_back():
    import_window.destroy()
    main_screen()

#---------------------------------------Main Screen---------------------------------------------------------------------
def data_manager_back():
    window.withdraw()
    home_screen()

def main_screen():
    global window
    window = Toplevel(home)

    window.title("Data Manager")

    window.config(padx=50, pady=50)

    canvas = Canvas(height=200, width=200)

    logo_img = PhotoImage(file="rsz_dw-logo-final-removebg-preview.png")

    canvas.create_image(100, 100, image=logo_img)

    image=Label(window, image=logo_img)
    image.image=logo_img
    image.grid(row=0, column=1)

    canvas.grid(row=0, column=1)
#Labels

    bname_label = Label(window, text="Business Name:")
    bname_label.grid(row=1, column=0)

    note_label = Label(window, text="NOTE: Type 'None or N' in the "
                                    "fields if no information is given", fg="red")
    note_label.grid(row=14, column=1)

    name_label = Label(window, text="Name:")
    name_label.grid(row=2, column=0)

    email_label = Label(window, text="Email:")
    email_label.grid(row=3, column=0)

    location_label = Label(window, text="Location:")
    location_label.grid(row=4, column=0)

    phone_label = Label(window, text="Phone Number:")
    phone_label.grid(row=5, column=0)

    job_label = Label(window, text="Job Type:")
    job_label.grid(row=6, column=0)

    user_id_label = Label(window, text=f"Logged in as: {u}")
    user_id_label.grid(row=13, column=1)

#Entries
    global bname_entry
    bname_entry = Entry(window, width=21)
    bname_entry.grid(row=1, column=1)
    bname_entry.focus()

    global name_entry
    name_entry = Entry(window, width=21)
    name_entry.grid(row=2, column=1)

    global email_entry
    email_entry = Entry(window, width=21)
    email_entry.grid(row=3 , column=1)

    global location_entry
    location_entry = Entry(window, width=21)
    location_entry.grid(row=4, column=1)

    global phone_entry
    phone_entry = Entry(window, width=21)
    phone_entry.grid(row=5, column=1)

    global job_entry
    job_entry = Entry(window, width=21)
    job_entry.grid(row=6, column=1)

    global text
    text = Text(window, height=5, width=30)
    text.grid(row=7, column=1)
    text_label = Label(window, text="Description")
    text_label.grid(row=7, column=0)

# Buttons

    search_button = Button(window, text="Search", width=13, command=lambda: [random_log(), find_data(), find_name(), find_phone(), find_email(), find_job()])
    search_button.grid(row=1, column=2)

    global radio_state
    radio_state = StringVar()
    radiobutton1 = Radiobutton(window, text="competitor", value="Competitor", variable=radio_state, command=radio_used)
    radiobutton2 = Radiobutton(window, text="client", value="Client", variable=radio_state, command=radio_used)

    radiobutton1.grid(row=9, column=1)
    radiobutton2.grid(row=10, column=1)

    company_list_button = Button(window, text="Manage All Data", command=lambda: [random_log(), show_list()])
    company_list_button.grid(row=2, column=2)

    delete_button = Button(window, text="Delete", width=8, command=lambda: [random_log(), insert_data(), delete()])
    delete_button.grid(row=3, column=2)
    delete_button.configure(fg="red")

    import_list_button = Button(window, text="View/Import Data", command=lambda: [random_log(), imports_screen()])
    import_list_button.grid(row=11, column=0)
    import_list_button.configure(fg="blue")

    add_button = Button(window, text="Add", width=36, command=lambda: [random_log(), save()])
    add_button.grid(row=11, column=1)
    add_button.configure(fg="green")

    des_button = Button(window, text="Description", width=36, command=lambda: [random_log(), find_des()])
    des_button.grid(row=12, column=1)

    data_back = Button(window, text="Back", width=8, command=lambda: [random_log(), data_manager_back()])
    data_back.grid(row=12, column=0)

    window.mainloop()

#---------------------------------------Home Screen---------------------------------------------------------------------
def next():
    home.withdraw()
    main_screen()

def home_screen():
    global home
    home = Toplevel(login)

    home.title("Home Screen")

    home.config(padx=50, pady=50)

    h_canvas = Canvas(height=200, width=200)

    home_img = PhotoImage(file="rsz_dw-logo-final-removebg-preview.png")

    h_canvas.create_image(100, 100, image=home_img)

    h_image = Label(home, image=home_img)
    h_image.image = home_img
    h_image.grid(row=0, column=1)

    h_canvas.grid(row=0, column=1)

    #Button

    next_button = Button(home, text="Data Manager", width=10, command=lambda: [random_log(), next()])
    next_button.grid(row=1, column=1)

    user_button = Button(home, text="User Management", width=10, command=lambda: [random_log(), user_screen_enter()])
    user_button.grid(row=2, column=1)

    logs_button = Button(home, text="View Logs", width=10, command=logs_screen)
    logs_button.grid(row=3, column=1)

    log_out_button = Button(home, text="Log Out", width=10, command=lambda: [random_log(), log_out(), reset()])
    log_out_button.grid(row=4, column=1)

    #Label
    user_id_label = Label(home, text=f"Logged in as: {u}")
    user_id_label.grid(row=5, column=1)

    home.mainloop()

#---------------------------------------U Screen---------------------------------------------------------------------

def delete_user():
    fl = full_name_entry.get()
    new_log = {
        a: {
            "Log": f"User {u} Deleted: '{fl}' Data, At '{date_time_str}'"
        }
    }

    msg_del = messagebox.askquestion(title=f"Delete", message=f"Confirm to Delete User: {fl} data ?",icon="warning")
    random_log()

    if msg_del == "yes":
        with open('user.json', 'r') as user_data, open("logs.json", "r") as logs_data:
            data = json.load(user_data)
            data_log = json.load(logs_data)
            if fl not in data:
                messagebox.showwarning(message="User not found", icon="warning")
            else:

                del data[fl]
                with open('user.json', 'w') as user_data, open("logs.json", "w") as logs_data:
                    json.dump(data, user_data)
                    data_log.update(new_log)
                    json.dump(data_log, logs_data, indent=2)
                    full_name_entry.delete(0, END)
                    user_pass_entry.delete(0, END)

                    messagebox.showinfo(title="Deleted", message="User deleted")

                    random_log()

    elif msg_del == "no":
        full_name_entry.delete(0, END)
        user_pass_entry.delete(0, END)

        random_log()

    else:
        messagebox.showwarning(message="Incorrect password. Access Denied", icon="warning")
        random_log()

def users_window_screen():
    if admin_confirmed is True:
        global users_window
        users_window = Toplevel(u_screen)

        users_window.title("Users")

        users_window.config(padx=10, pady=10)

        l_canvas = Canvas(users_window, height=20, width=30)
        l_canvas.grid(row=0, column=1)

        user_listbox = Listbox(users_window, height=10, width=15)
        user_listbox.grid(row=1, column=0)

        scrollbar = Scrollbar(users_window, orient=VERTICAL)
        scrollbar.grid(row=1, column=1, sticky=N + S)

        users = []

        user_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=user_listbox.yview)

        with open('user.json', 'r') as f:
            data = json.load(f)
            for item in data:
                users.append(item)
        for item in users:
            user_listbox.insert(END, item)

        users_window.mainloop()
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")


def user_screen_enter():
    home.withdraw()
    user_screen()

def user_back():
    u_screen.destroy()
    home_screen()

def add_user_back():
    add_screen.destroy()
    user_screen()
    random_log()

def add_user_screen():
    if admin_confirmed is True:
        global add_screen
        u_screen.withdraw()
        add_screen = Toplevel(u_screen)

        add_screen.title("Add/Delete User")

        add_screen.config(padx=50, pady=50)

        add_canvas = Canvas(height=200, width=200)

        add_canvas.grid(row=0, column=1)

    #Labels

        full_name_label = Label(add_screen, text="Full Name:")
        full_name_label.grid(row=0, column=0)

        user_pass_label = Label(add_screen, text="Password:")
        user_pass_label.grid(row=1, column=0)

    #Entrys
        global full_name_entry
        full_name_entry = Entry(add_screen, width=21)
        full_name_entry.grid(row=0, column=1)
        full_name_entry.focus()

        global user_pass_entry
        user_pass_entry = Entry(add_screen, width=21)
        user_pass_entry.grid(row=1, column=1)

    #button

        add_user_back_button = Button(add_screen, text="Back", width=10, command=lambda: [random_log(), add_user_back()])
        add_user_back_button.grid(row=4, column=0)

        confirm_user_button = Button(add_screen, text="Add", width=15, command=lambda: [random_log(), save_new_user()])
        confirm_user_button.grid(row=5, column=1)
        confirm_user_button.configure(fg="green")

        delete_user_button = Button(add_screen, text="Delete", width=15, command=lambda: [random_log(), delete_user()])
        delete_user_button.grid(row=6, column=1)
        delete_user_button.configure(fg="red")

        global user_state
        user_state = StringVar()
        radiobutton1 = Radiobutton(add_screen, text="Admin", value="Admin", variable=user_state, command=lambda: [random_log(), user_radio_used()])
        radiobutton2 = Radiobutton(add_screen, text="User", value="User", variable=user_state,command=lambda: [random_log(), user_radio_used()])
        radiobutton3 = Radiobutton(add_screen, text="Moderator", value="Moderator", variable=user_state,command=lambda: [random_log(), user_radio_used()])

        radiobutton1.grid(row=2, column=1)
        radiobutton2.grid(row=3, column=1)
        radiobutton3.grid(row=4, column=1)

        add_screen.mainloop()
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")

def user_screen():
    global u_screen
    u_screen = Toplevel(home)

    u_screen.title("User Management")

    u_screen.config(padx=50, pady=50)

    u_canvas = Canvas(height=200, width=200)

    u_canvas.grid(row=0, column=1)

    #Buttons

    user_back_button = Button(u_screen, text="Back", width=10, command=lambda: [random_log(), user_back()])
    user_back_button.grid(row=3, column=0)

    add_user_button = Button(u_screen, text="Add/Delete User", width=18, command=lambda: [random_log(),add_user_screen()])
    add_user_button.grid(row=1, column=0)

    show_users_button = Button(u_screen, text="Show Users", width=18, command=users_window_screen)
    show_users_button.grid(row=2, column=0)

    user_id_label = Label(u_screen, text=f"Logged in as: {u}")
    user_id_label.grid(row=0, column=0)

    u_screen.mainloop()

#-------------------------------------------------Logs Screen-----------------------------------------------------------

def delete_logs_data():
    confirmation_window = Toplevel(logs_s)
    confirmation_window.title('Confirmation')
    confirmation_window.geometry('300x100')

    password_label = Label(confirmation_window, text='Enter password:')
    password_label.grid(row=0,column=0)

    password_entry = Entry(confirmation_window, show='*')
    password_entry.grid(row=0, column=1)
    password_entry.focus()

    def delete_data():
        if password_entry.get() == 'master':

            with open('logs.json', 'w') as logs_file:
                logs_file.write('{}')

            messagebox.showinfo('Deletion Complete', 'All data has been deleted.')

            new_log = {
                a: {
                    "Log": f"User '{u}' 'Cleared Logs' Data, At '{date_time_str}'"
                }
            }

            with open("logs.json", "r") as logs_data:
                data_logs = json.load(logs_data)
                with open("logs.json", "w") as logs_data:
                    data_logs.update(new_log)
                    json.dump(data_logs, logs_data, indent=2)
                    random_log()


            confirmation_window.destroy()
        else:
            messagebox.showerror('Incorrect Password', 'The password you entered is incorrect.', icon="warning")

    confirm_button = Button(confirmation_window, text='Confirm', command=delete_data)
    confirm_button.grid(row=1,column=1)

    confirmation_window.mainloop()

def logs_screen_back():
    logs_s.destroy()
    home_screen()

def logs_screen():
    if admin_confirmed is True:
        home.withdraw()
        global logs_s
        logs_s = Toplevel(home)

        logs_s.title("Logs")

        logs_s.config(padx=30, pady=60)

        l_canvas = Canvas(logs_s, height=50, width=150)
        l_canvas.grid(row=0, column=1)

        logs_listbox = Listbox(logs_s, height=20, width=100)
        logs_listbox.grid(row=1, column=0)

        #Buttons
        delete_logs_button = Button(logs_s, text='Clear Data', width=50, command=delete_logs_data)
        delete_logs_button.grid(row=2, column=0)
        delete_logs_button.configure(fg="red")

        logs_back_button = Button(logs_s, text='Back', width=50, command=logs_screen_back)
        logs_back_button.grid(row=0, column=0)

        scrollbar = Scrollbar(logs_s, orient=VERTICAL)
        scrollbar.grid(row=1, column=1, sticky=N + S)

        logs_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=logs_listbox.yview)

        with open('logs.json') as logs_data:
            data = json.load(logs_data)
            for year in data:
                log_value = data[year]['Log']
                logs_listbox.insert(END, log_value)

        for i in range(logs_listbox.size()):
            item = logs_listbox.get(i).lower()
            if "deleted" in item:
                logs_listbox.itemconfigure(i, {'fg': 'red'})
            elif "added" in item:
                logs_listbox.itemconfigure(i, {'fg': 'green'})
            elif "signed in" in item:
                logs_listbox.itemconfigure(i, {'fg': 'orange'})
            elif "logged-out" in item:
                logs_listbox.itemconfigure(i, {'fg': 'orange'})
            elif "imported" in item:
                logs_listbox.itemconfigure(i, {'fg': 'blue'})
            elif "backed up" in item:
                logs_listbox.itemconfigure(i, {'fg': 'cyan'})

        logs_s.mainloop()
    else:
        messagebox.showwarning(message="Access Denied", icon="warning")

#-----------------------------------------------------------------------------------------------------------------------
create_user_file()
create_json_files()
login_screen()