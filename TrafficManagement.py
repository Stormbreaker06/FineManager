import tkinter as tk
from tkinter import messagebox
import csv
import pandas as pd

#Defining the database file path as a constant
DATABASE_FILE_PATH = 'database1.csv'

#Defining offences globally
OFFENCES = [
    "Speeding",
    "Reckless Driving",
    "Parking Violation",
    "Running a Red Light",
    "Driving Without a License",
    "Driving Under Influence",
    "Using Mobile While Driving",
    "Not Wearing a Seatbelt",
    "Driving an Uninsured Vehicle",
    "Failure to Stop for Pedestrians"
]
#creating POLICE as a class and using it for username and password
class Police:
    def __init__(self, username, password):#constructors
        self.username = username
        self.password = password

    def dashboard(self):#for ploce dashboard
        open_police_dashboard()

#defining a function for verifying the login credentials
def validate_login(role):
    if role == "police":
        username = police_username_entry.get()
        password = police_password_entry.get()
        if validate_police_credentials(username, password):
            police = Police(username, password)#creates an instance of the class
            police.dashboard()
        else:
            messagebox.showerror("Error", "Invalid police credentials.")
    else:
        vehicle_number = vehicle_number_entry.get()
        if vehicle_number:
            if check_vehicle_exists(vehicle_number):
                open_user_dashboard(vehicle_number)
            else:
                ask_vehicle_info(vehicle_number)
        else:
            messagebox.showerror("Error", "Please enter vehicle number.")
#Cross Checking Police Credentials with Credentials present in CSV
def validate_police_credentials(username, password):
    with open('police_credentials.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False
#POLICE DASHBOARD
def open_police_dashboard():
    def print_receipt():
        vehicle_number = vehicle_entry_var.get()
        df = read_data(DATABASE_FILE_PATH)
        vehicle_data = df[df['Vehicle'] == vehicle_number]
        if not vehicle_data.empty:
            info = vehicle_data.iloc[0].to_dict()#This line converts the first row of the filtered DataFrame vehicle_data into a dictionary
            new_receipt_text +=  "Vehicle Number: %s\n" % (info['Vehicle'])
            new_receipt_text += "Owner: %s\n" % (info['Owner'])
            new_receipt_text +="Date: %s\n" % (info['Date'])
            new_receipt_text += "Total Fines: Rs. %s\n\n" % (info['Total'])
            new_receipt_text += "Offenses:\n"
            for offence in OFFENCES:
                new_receipt_text += f"{offence}: {info[offence]}\n"
        else:
            new_receipt_text = "Vehicle number not found."
#RECEIPT WINDOW GUI
        receipt_window = tk.Toplevel(root)
        receipt_window.title("Receipt")
        receipt_window.geometry("600x600")

        receipt_frame = tk.Frame(receipt_window, bg="white", bd=2, relief="sunken")
        receipt_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        receipt_label = tk.Label(receipt_frame, text="Receipt", font=("Garamond", 20, "bold"), bg="white")
        receipt_label.pack(pady=10)

        receipt_content = tk.Label(receipt_frame, text=new_receipt_text, font=("Garamond", 18), bg="white", justify=tk.LEFT)
        receipt_content.pack(pady=10, padx=10)
#MAKING THE BUTTON WORK 
    def enable_print_button(*args):
        if fine_entry_var.get().strip():
            print_button.config(state=tk.NORMAL)
        else:
            print_button.config(state=tk.DISABLED)
#ASKING FOR VEHICLE INFo
    def search_vehicle():
        vehicle_number = vehicle_entry_var.get()
        if check_vehicle_exists(vehicle_number):
            display_vehicle_info(vehicle_number)
        else:
            ask_vehicle_info(vehicle_number)
#displaying vehicle info 
    def display_vehicle_info(vehicle_number):
        df = read_data(DATABASE_FILE_PATH)
        vehicle_data = df[df['Vehicle'] == vehicle_number]
        if not vehicle_data.empty:
            info = vehicle_data.iloc[0].to_dict()
            info_text = f"Vehicle: {info['Vehicle']}\nOwner: {info['Owner']}\nDate: {info['Date']}\nTotal Fines: {info['Total']}"#formatting it to string
            vehicle_info_label.config(text=info_text)
        else:
            messagebox.showerror("Error", "Vehicle number not found.")
#adding fine
    def add_fine():
        vehicle_number = vehicle_entry_var.get()
        fine_amount = fine_entry_var.get()
        offence = offence_var.get()

        if vehicle_number and fine_amount and offence != "Select Offence":
            df = read_data(DATABASE_FILE_PATH)
            if vehicle_number in df['Vehicle'].values:
                df.loc[df['Vehicle'] == vehicle_number, offence] += int(fine_amount)
                df.loc[df['Vehicle'] == vehicle_number, 'Total'] += int(fine_amount)
                df.to_csv(DATABASE_FILE_PATH, index=False)
                messagebox.showinfo("Success", "Fine added successfully.")
                display_vehicle_info(vehicle_number)
            else:
                messagebox.showerror("Error", "Vehicle number not found.")
        else:
            messagebox.showerror("Error", "Please fill all fields correctly.")
#police dashboard
    police_window = tk.Toplevel(root)
    police_window.title("Police Dashboard")
    police_window.geometry("1000x1000")
    police_window.resizable(False, False)
    police_frame = tk.Frame(police_window, bg="#add8e6")
    police_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    tk.Label(police_frame, text="Police Dashboard", font=("Garamond", 30, "bold"), bg="#add8e6").pack(pady=10)

    form_frame = tk.Frame(police_frame, bg="#add8e6")
    form_frame.pack(pady=10)
#vehicle number entry button
    tk.Label(form_frame, text="Enter Vehicle Number:", font=("Garamond", 20, "bold"), bg="#add8e6").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    vehicle_entry_var = tk.StringVar()
    vehicle_entry = tk.Entry(form_frame, font=("Garamond", 18), width=20, textvariable=vehicle_entry_var)
    vehicle_entry.grid(row=0, column=1, padx=10, pady=10)
    vehicle_entry_var.trace("w", lambda name, index, mode, sv=vehicle_entry_var: sv.set(sv.get().upper()))
#search button
    tk.Button(form_frame, text="Search", font=("Garamond", 18, "bold"), width=10, command=search_vehicle).grid(row=0, column=2, padx=10, pady=10)

    vehicle_info_label = tk.Label(form_frame, text="", font=("Garamond", 18), bg="#add8e6", justify=tk.LEFT)
    vehicle_info_label.grid(row=1, columnspan=3, padx=10, pady=10)
#fine button
    tk.Label(form_frame, text="Add Fine:", font=("Garamond", 20, "bold"), bg="#add8e6").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    fine_entry_var = tk.StringVar()
    fine_entry = tk.Entry(form_frame, font=("Garamond", 18), width=10, textvariable=fine_entry_var)
    fine_entry.grid(row=2, column=1, padx=10, pady=10)
    fine_entry_var.trace("w", enable_print_button)

    validate_numeric = police_window.register(lambda P: P.isdigit() or P == "")
    fine_entry.config(validate="key", validatecommand=(validate_numeric, '%P'))

    tk.Label(form_frame, text="Rs.", font=("Garamond", 18), bg="#add8e6").grid(row=2, column=2, padx=10, pady=10, sticky='w')
#offence option menu
    tk.Label(form_frame, text="Offence:", font=("Garamond", 20, "bold"), bg="#add8e6").grid(row=3, column=0, padx=10, pady=10, sticky='e')
    offence_var = tk.StringVar()
    offence_var.set("Select Offence")
    offences = [
        "Speeding",
        "Reckless Driving",
        "Parking Violation",
        "Running a Red Light",
        "Driving Without a License",
        "Driving Under Influence",
        "Using Mobile While Driving",
        "Not Wearing a Seatbelt",
        "Driving an Uninsured Vehicle",
        "Failure to Stop for Pedestrians"
    ]
    offence_menu = tk.OptionMenu(form_frame, offence_var, *offences)
    offence_menu.config(font=("Garamond", 18))
    offence_menu.grid(row=3, column=1, padx=10, pady=10, sticky='w')
#print button
    print_button = tk.Button(form_frame, text="Print", font=("Garamond", 18, "bold"), width=10, command=print_receipt, state=tk.DISABLED)
    print_button.grid(row=5, columnspan=3, pady=20)

    tk.Button(form_frame, text="Add Fine", font=("Garamond", 18, "bold"), width=15, command=add_fine).grid(row=4, columnspan=3, pady=20)

    enable_print_button()
#user dashboard
def open_user_dashboard(vehicle_number):
    user_window = tk.Toplevel(root)
    user_window.title("USER DETIALS")
    user_window.geometry("800x800")
    user_window.resizable(False, False)
    
    def display_vehicle_info(vehicle_number):
        df = read_data(DATABASE_FILE_PATH)
        vehicle_data = df[df['Vehicle'] == vehicle_number]
        if not vehicle_data.empty:
            info = vehicle_data.iloc[0].to_dict()
            info_text = f"Vehicle: {info['Vehicle']}\nOwner: {info['Owner']}\nDate: {info['Date']}\nTotal Fines: Rs. {info['Total']}\n\n"
            info_text += "Offenses:\n"
            for offence in OFFENCES:
                info_text += f"{offence}: {info[offence]}\n"
            vehicle_info_label.config(text=info_text)
        else:
            messagebox.showerror("Error", "Vehicle number not found.")
    #user details button
    tk.Label(user_window, text="USER DETAILS", font=("Garamond", 30, "bold")).pack(pady=10)
    vehicle_info_label = tk.Label(user_window, text="", font=("Garamond", 18), justify=tk.LEFT)
    vehicle_info_label.pack(pady=10, padx=10)
    
    display_vehicle_info(vehicle_number)
#Reading all the Offenses and Needed data into a DataFrame
def read_data(file_name):
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Vehicle', 'Owner', 'Date', 'Speeding', 'Reckless Driving', 'Parking Violation', 
                                   'Running a Red Light', 'Driving Without a License', 'Driving Under Influence', 
                                   'Using Mobile While Driving', 'Not Wearing a Seatbelt', 'Driving an Uninsured Vehicle', 
                                   'Failure to Stop for Pedestrians', 'Total'])
    return df
#Checking for Vehicle No. already existing in Database
def check_vehicle_exists(vehicle_number):
    df = read_data(DATABASE_FILE_PATH)
    return vehicle_number in df['Vehicle'].values

def vehicle_info(vehicle_number):
    df = read_data(DATABASE_FILE_PATH)
    vehicle_data = df[df['Vehicle'] == vehicle_number]
    if not vehicle_data.empty:
        info = vehicle_data.iloc[0].to_dict()
        messagebox.showinfo("Vehicle Info", f"Vehicle: {info['Vehicle']}\nOwner: {info['Owner']}\nDate: {info['Date']}\nTotal Fines: {info['Total']}")
    else:
        messagebox.showerror("Error", "Vehicle number not found.")

def ask_vehicle_info(vehicle_number):
    def save_vehicle_info():
        owner = owner_entry_var.get()
        date = date_entry_var.get()
        offences = [0] * 10
        new_data = {#using dictionaries
            'Vehicle': vehicle_number,
            'Owner': owner,
            'Date': date,
            'Speeding': offences[0],
            'Reckless Driving': offences[1],
            'Parking Violation': offences[2],
            'Running a Red Light': offences[3],
            'Driving Without a License': offences[4],
            'Driving Under Influence': offences[5],
            'Using Mobile While Driving': offences[6],
            'Not Wearing a Seatbelt': offences[7],
            'Driving an Uninsured Vehicle': offences[8],
            'Failure to Stop for Pedestrians': offences[9],
            'Total': sum(offences),
        }
        df = read_data(DATABASE_FILE_PATH)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(DATABASE_FILE_PATH, index=False)
        messagebox.showinfo("Success", "Vehicle information added successfully.")
        add_vehicle_window.destroy()
#adding vehicel deatials if not present earlier
    add_vehicle_window = tk.Toplevel(root)
    add_vehicle_window.title("Add Vehicle Information")
    add_vehicle_window.geometry("500x400")
    add_vehicle_window.resizable(False, False)

    tk.Label(add_vehicle_window, text="Enter Vehicle Information", font=("Garamond", 20, "bold")).pack(pady=10)

    form_frame = tk.Frame(add_vehicle_window)
    form_frame.pack(pady=10, padx=10)
#owenre name enry
    tk.Label(form_frame, text="Owner Name:", font=("Garamond", 18)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    owner_entry_var = tk.StringVar()
    owner_entry = tk.Entry(form_frame, font=("Garamond", 18), width=20, textvariable=owner_entry_var)
    owner_entry.grid(row=0, column=1, padx=10, pady=10)
#date entry
    tk.Label(form_frame, text="Date of Registration(dd/mm/yyyy):", font=("Garamond", 18)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    date_entry_var = tk.StringVar()
    date_entry = tk.Entry(form_frame, font=("Garamond", 18), width=20, textvariable=date_entry_var)
    date_entry.grid(row=1, column=1, padx=10, pady=10)
#save button
    tk.Button(form_frame, text="Save", font=("Garamond", 18, "bold"), width=10, command=save_vehicle_info).grid(row=2, columnspan=2, pady=20)

def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.title("Traffic Challan Management System")
root.geometry("998x668")
root.resizable(False, False)

main_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1, bg="#62b9e9")
police_login_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1, bg="#add8e6")
driver_login_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1, bg="#add8e6")
#setting 3 frames 
for frame in (main_frame, police_login_frame, driver_login_frame):
    frame.place(x=0, y=0, width=998, height=668)
    frame.configure(relief="flat")

# Main heading and buttons
tk.Label(main_frame, text="TRAFFIC CHALLAN MANAGEMENT SYSTEM", font=("Garamond", 30, "bold"), bg="#62b9e9").pack(pady=50)
tk.Button(main_frame, text="Police Login", command=lambda: show_frame(police_login_frame), font=("Garamond", 18, "bold"), width=15).pack(pady=10)
tk.Button(main_frame, text="Driver Login", command=lambda: show_frame(driver_login_frame), font=("Garamond", 18, "bold"), width=15).pack(pady=10)

# Police login
tk.Label(police_login_frame, text="POLICE LOGIN", font=("Garamond", 30, "bold"), bg="#add8e6").pack(pady=50)
tk.Label(police_login_frame, text="Username:", font=("Garamond", 18), bg="#add8e6").pack()
police_username_entry = tk.Entry(police_login_frame, font=("Garamond", 18))
police_username_entry.pack()
tk.Label(police_login_frame, text="Password:", font=("Garamond", 18), bg="#add8e6").pack()
police_password_entry = tk.Entry(police_login_frame, show="*", font=("Garamond", 18))
police_password_entry.pack()
tk.Button(police_login_frame, text="Login", command=lambda: validate_login("police"), font=("Garamond", 18, "bold"), width=10).pack(pady=10)
tk.Button(police_login_frame, text="Back", command=lambda: show_frame(main_frame), font=("Garamond", 18, "bold"), width=10).pack(pady=10)

# Driver login
tk.Label(driver_login_frame, text="DRIVER LOGIN", font=("Garamond", 30, "bold"), bg="#add8e6").pack(pady=50)
tk.Label(driver_login_frame, text="Vehicle Number:", font=("Garamond", 18), bg="#add8e6").pack()
vehicle_number_entry = tk.Entry(driver_login_frame, font=("Garamond", 18))
vehicle_number_entry.pack()
tk.Button(driver_login_frame, text="View Details", command=lambda: validate_login("driver"), font=("Garamond", 18, "bold"), width=10).pack(pady=10)
tk.Button(driver_login_frame, text="Back", command=lambda: show_frame(main_frame), font=("Garamond", 18, "bold"), width=10).pack(pady=10)

show_frame(main_frame)

root.mainloop()
