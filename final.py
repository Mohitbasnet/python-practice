import tkinter as tk
from tkinter import messagebox
import pymysql.cursors
from PIL import ImageTk, Image
from datetime import datetime


class Helpdesk():
    def __init__(self, root):
        self.root = root
        self.root.title("Helpdesk System")
        window_width = 1366
        window_height = 768
        bg_image = Image.open("cool-background.png")
        bg_image = bg_image.resize((1366, 768), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=self.background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame to hold the content
        frame = tk.Frame(root)
        frame.pack(pady=50)

        label_font = ("Arial", 12)
        button_font = ("Arial", 12, "bold")
        title_font = ("Arial", 20, "bold")

        tk.Label(frame, text="Add Problem Details Here", font=title_font, bg="Blue", fg="white").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Call ID:", fg="white", bg="#003366", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.id_entry = tk.Entry(frame)
        self.id_entry.grid(row=1, column=1, sticky="w")

        tk.Label(frame, text="Problem Description and Notes:", fg="white", bg="#003366", font=label_font).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.problem_description_entry = tk.Entry(frame, width=30)
        self.problem_description_entry.grid(row=2, column=1, sticky="w")

        tk.Label(frame, text="Problem Type ID:", fg="white", bg="#003366", font=label_font).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.problem_type_id_entry = tk.Entry(frame)
        self.problem_type_id_entry.grid(row=3, column=1, sticky="w")

        tk.Button(frame, text="Show Specialist Details", command=self.show_specialist, bg="blue", fg="white", font=button_font).grid(row=4, column=1, columnspan=2)

        tk.Label(frame, text="Specialist ID:", fg="white", bg="#003366", font=label_font).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.specialist_id_entry = tk.Entry(frame)
        self.specialist_id_entry.grid(row=5, column=1, sticky="w")

        tk.Button(frame, text="Refer Problem to Specialist", command=self.refer_to_specialist, bg="green", fg="white", font=button_font).grid(row=6, column=1, columnspan=8)

        tk.Label(frame, text="Resolution Time:", fg="white", bg="#003366", font=label_font).grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.resolution_time_entry = tk.Entry(frame)
        self.resolution_time_entry.grid(row=7, column=1, sticky="w")

        tk.Label(frame, text="Time Taken to Resolve:", fg="white", bg="#003366", font=label_font).grid(row=8, column=0, padx=10, pady=10, sticky="e")
        self.time_taken_to_resolve_entry = tk.Entry(frame)
        self.time_taken_to_resolve_entry.grid(row=8, column=1, sticky="w")

        tk.Label(frame, text="Resolution Details:", fg="white", bg="#003366", font=label_font).grid(row=9, column=0, padx=10, pady=10, sticky="e")
        self.resolution_details_entry = tk.Entry(frame, width=30)
        self.resolution_details_entry.grid(row=9, column=1, sticky="w")

        tk.Button(frame, text="Save Problem Details", command=self.save_problem_details, bg="purple", fg="white", font=button_font).grid(row=10, column=1, columnspan=1)
        tk.Button(frame, text="Generate Call Report", command=self.generate_call_report, bg="orange", fg="white", font=button_font).grid(row=12, column=1, columnspan=2)
        tk.Button(frame, text="Close", command=self.close, bg="red", fg="white", font=button_font).grid(row=14, column=1, columnspan=1)

        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Loveufather@123",
            database="helpdesk"
        )

    def show_specialist(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM specialist")
        specialists = cursor.fetchall()

        if specialists:
            messagebox.showinfo("Specialists", "Specialist Details:\n\n" +
                                "\n".join([f"Specialist ID: {s[0]}\nName: {s[1]}\nNo of work currently working: {s[2]}\nproblem Expertise: {s[3]}\n" for s in specialists]))
        else:
            messagebox.showinfo("Specialists", "No specialists found!")

    def refer_to_specialist(self):
        specialist_id = self.specialist_id_entry.get()
        # Validate the specialist ID
        if not specialist_id:
            messagebox.showerror("Error", "Please enter the Specialist ID!")
            return
        # Get the name of the specialist from the specialist table
        cursor = self.conn.cursor()
        cursor.execute("SELECT specialist_name FROM specialist WHERE specialist_id = %s", (specialist_id,))
        specialist = cursor.fetchone()

        if specialist:
            specialist_name = specialist[0]
            # Save the problem details with the specialist ID
            self.save_problem_details()

            # Show success message with specialist name
            messagebox.showinfo("Success", f"Problem referred to the specialist '{specialist_name}' successfully!")
        else:
            messagebox.showerror("Error", "Specialist not found!")
    def save_problem_details(self):
        id = self.id_entry.get()
        problem_description = self.problem_description_entry.get()
        problem_type_id = self.problem_type_id_entry.get()
        specialist_id = self.specialist_id_entry.get()
        resolution_time = self.resolution_time_entry.get()
        time_taken_to_resolve = self.time_taken_to_resolve_entry.get()
        resolution_details = self.resolution_details_entry.get()

        if not all([id, problem_description, problem_type_id, specialist_id, resolution_time, time_taken_to_resolve, resolution_details]):
            return

        try:
            resolution_time = datetime.strptime(resolution_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid Resolution Time format. Please use the format 'YYYY-MM-DD HH:MM:SS'!")
            return

        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO problems (id, problem_description, problem_type_id, specialist_id, 
            resolution_time, time_taken_to_resolve, resolution_details) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (id, problem_description, problem_type_id, specialist_id, resolution_time,
            time_taken_to_resolve, resolution_details)
        )

        self.conn.commit()
        messagebox.showinfo("Success", "Problem details saved successfully!")
    def generate_call_report(self):
        call_report_window = tk.Toplevel(self.root)
        call_report_window.title("Helpdesk Operating system")
        call_report_window.geometry("1366x768")
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT problem_id, call_details.call_time,call_details.operator_name,
        problems.resolution_time, problems.time_taken_to_resolve, problems.resolution_details, specialist.specialist_name, specialist.problem_exepertise,problemtype.problem_type
        from problems 
        INNER JOIN call_details on
        problems.id = call_details.id
        INNER JOIN specialist on
        problems.specialist_id = specialist.specialist_id
        Inner JOIN problemtype on
        problems.problem_type_id = problemtype.problem_type_id
            ORDER BY call_details.call_time DESC
    LIMIT 4
    """)
        call_report = cursor.fetchall()
        # bg_image = Image.open("download.png")
        # bg_image = bg_image.resize((1366, 768), Image.LANCZOS)
        # background = ImageTk.PhotoImage(bg_image)
        # bg_label = tk.Label(call_report_window, image=background)
        # bg_label.pack(fill=tk.BOTH, expand=True)
        # bg_label.image = background 

        if call_report:
            report_text = "Call Reports:\n\n"
            for report in call_report:
                report_text += f"Problem ID: {report[0]}\nCall Time: {report[1]}\nOperator: {report[2]}\nResolution Time: {report[3]}\nTime Taken to Resolve: {report[4]}\nResolution Details: {report[5]}\nSpecialist Name: {report[6]}\nProblem Expertise: {report[7]}\nProblem Type: {report[8]}\n\n"

            report_label = tk.Label(call_report_window, text=report_text)
            report_label.pack()
            report_label.pack(anchor="center")

   
        else:
            no_report_label = tk.Label(call_report_window, text="No call report found!")
            no_report_label.pack()
            no_report_label.pack(anchor="center")
                
    def close(self):
        # call_window.destroy()
        self.conn.close()
        self.root.destroy()
        
class Call: 
    def __init__(self, caller_id, operator_name, call_time, computer_serial, software_id, equipment_id):
        self.caller_id = caller_id
        self.operator_name = operator_name
        self.call_time = call_time
        self.computer_serial = computer_serial
        self.software_id = software_id
        self.equipment_id = equipment_id
class HelpdeskGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Helpdesk operating System")

        # Set background image
        bg_image = Image.open("cool-background.png")
        bg_image = bg_image.resize((1366, 768), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=self.background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame to hold the labels and entry fields
        frame = tk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create labels and entry fields
        caller_id_label = tk.Label(frame, text="Caller ID:", font=("Helvetica", 12, "bold"),fg="white", bg="#003366")
        caller_id_label.grid(row=0, column=0, padx=10, pady=5)
        self.caller_id_entry = tk.Entry(frame)
        self.caller_id_entry.grid(row=0, column=1, padx=10, pady=5)

        operator_name_label = tk.Label(frame, text="Operator Name:", font=("Helvetica", 12, "bold"),fg="white", bg="#003366")
        operator_name_label.grid(row=1, column=0, padx=10, pady=5)
        self.operator_name_entry = tk.Entry(frame)
        self.operator_name_entry.grid(row=1, column=1, padx=10, pady=5)

        software_id_label = tk.Label(frame, text="Software ID:", font=("Helvetica", 12, "bold"),fg="white", bg="#003366")
        software_id_label.grid(row=2, column=0, padx=10, pady=5)
        self.software_id_entry = tk.Entry(frame)
        self.software_id_entry.grid(row=2, column=1, padx=10, pady=5)

        equipment_id_label = tk.Label(frame, text="Equipment ID:", font=("Helvetica", 12, "bold"),fg="white", bg="#003366")
        equipment_id_label.grid(row=3, column=0, padx=10, pady=5)
        self.equipment_id_entry = tk.Entry(frame)
        self.equipment_id_entry.grid(row=3, column=1, padx=10, pady=5)

        serial_number_label = tk.Label(frame, text="Serial Number:", font=("Helvetica", 12, "bold"),fg="white", bg="#003366")
        serial_number_label.grid(row=4, column=0, padx=10, pady=5)
        self.serial_number_entry = tk.Entry(frame)
        self.serial_number_entry.grid(row=4, column=1, padx=10, pady=5)

        # Add the "Capture Call Details" button
        capture_button = tk.Button(frame, text="Capture Call Details", command=self.capture_call_details)
        capture_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        capture_button.config(font=("Helvetica", 12, "bold"), fg="white", bg="#4CAF50")

        # Add the "Exit" button
        exit_button = tk.Button(frame, text="Exit", command=root.destroy)
        exit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        exit_button.config(font=("Helvetica", 12, "bold"), fg="white", bg="#FF0000")

        # Modify the title label to be bold and colorful
        title_font = ("Helvetica", 24, "bold")
        title_label = tk.Label(root, text="Add Call Details Here", font=title_font, fg="blue", bg="skyblue")
        title_label.place(x=680, y=222, anchor=tk.CENTER)

    

   
        # Connect to the database
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Loveufather@123",
            database="helpdesk"
        )
    
    def save_call_details(self, call):
        cursor = self.conn.cursor()

        # Save call details
        cursor.execute(
            """INSERT INTO call_details (caller_id, operator_name, call_time, computer_serial, software_id, 
            equipment_id) VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                call.caller_id,
                call.operator_name,
                call.call_time,
                call.computer_serial,
                call.software_id,
                call.equipment_id,
            ),
        )

        self.conn.commit()
   
    
    def display_call_details(self, call):

    # Display the call details in a new window
        call_window = tk.Toplevel(self.root)
        call_window.title("Helpdesk Operating system")
        call_window.geometry("1366x768")
        window_width = 1366
        window_height = 768
    
    # Set background image
        bg_image = Image.open("download.png")
        bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(call_window, image=self.background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        cursor = self.conn.cursor()
        middle_x = window_width // 2
        # Fetch caller details from personnel table
        cursor.execute("SELECT caller_name, job_title, department FROM personnel WHERE caller_id=%s", (call.caller_id,))
        result = cursor.fetchone()
        # Add the title label
        tk.Label(call_window, text="Call Details", font=("Helvetica", 15, "bold"), fg="white", bg="blue").place(x=middle_x - 100, y=20, anchor="center")
        
        if result:
            caller_name, job_title, department = result

        # Calculate the middle x coordinate
            middle_x = window_width // 2
    
            tk.Label(call_window, text="Caller Name:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=50, anchor="e")
            tk.Label(call_window, text=caller_name, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=50, anchor="w")

            tk.Label(call_window, text="Job Title:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=100, anchor="e")
            tk.Label(call_window, text=job_title, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=100, anchor="w")

            tk.Label(call_window, text="Department:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=150, anchor="e")
            tk.Label(call_window, text=department, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=150, anchor="w")

    # Fetch software details from software table
        cursor.execute("SELECT software_name, operating_system FROM software WHERE software_id=%s", (call.software_id,))
        result = cursor.fetchone()
        if result:
            software_name, operating_system = result
        
            tk.Label(call_window, text="Software Name:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=200, anchor="e")
            tk.Label(call_window, text=software_name, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=200, anchor="w")

            tk.Label(call_window, text="Operating System:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=250, anchor="e")
            tk.Label(call_window, text=operating_system, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=250, anchor="w")

    # Fetch equipment details from equipment table
        cursor.execute("SELECT equipment_make, equipment_type FROM equipment WHERE equipment_id=%s", (call.equipment_id,))
        result = cursor.fetchone()
        if result:
            equipment_make, equipment_type = result

            tk.Label(call_window, text="Equipment Make:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=300, anchor="e")
            tk.Label(call_window, text=equipment_make, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=300, anchor="w")

            tk.Label(call_window, text="Equipment Type:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=350, anchor="e")
            tk.Label(call_window, text=equipment_type, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=350, anchor="w")   
    # Display other call details
        tk.Label(call_window, text="Caller ID:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=400, anchor="e")
        tk.Label(call_window, text=call.caller_id, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=400, anchor="w")

        tk.Label(call_window, text="Operator Name:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=450, anchor="e")
        tk.Label(call_window, text=call.operator_name, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=450, anchor="w")

        tk.Label(call_window, text="Call Time:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=500, anchor="e")
        tk.Label(call_window, text=call.call_time, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=500, anchor="w")   
        tk.Label(call_window, text="Computer Serial:", font=("Helvetica", 12, "bold"), fg="white", bg="#003366").place(x=600, y=550, anchor="e")
        tk.Label(call_window, text=call.computer_serial, font=("Helvetica", 12), fg="white", bg="#003366").place(x=620, y=550, anchor="w")

        def add_problem_details():
        # Open the problem details window
            self.root.destroy()
            root = tk.Tk()
            app = Helpdesk(root)
            root.protocol("WM_DELETE_WINDOW")
            root.geometry("1360x768")  # Adjust the size as needed
            root.mainloop()

    # Calculate the middle x coordinate for the buttons
        middle_x = window_width // 2

    # Add the "Add Problem Details" button
        tk.Button(call_window, text="Add Problem Details", command=add_problem_details, font=("Helvetica", 12, "bold"), fg="white", bg="#336699").place(x=middle_x - 100, y=600, anchor="center")

        def close_window():
            call_window.destroy()

    # Add the "Exit" button
        tk.Button(call_window, text="Exit", command=close_window, font=("Helvetica", 12, "bold"), fg="white", bg="#FF0000").place(x=middle_x - 100, y=650, anchor="center")

        self.conn.commit()


    def capture_call_details(self):
        # Get the input values
        caller_id = self.caller_id_entry.get()
        operator_name = self.operator_name_entry.get()
        software_id = self.software_id_entry.get()
        equipment_id = self.equipment_id_entry.get()
        serial_number = self.serial_number_entry.get()
        
        # Check if any field is empty
        if not caller_id or not operator_name or not software_id or not equipment_id or not serial_number:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        # Convert caller ID, software ID, equipment ID, and serial number to integers
        try:
            caller_id = int(caller_id)
            software_id = int(software_id)
            equipment_id = int(equipment_id)
            serial_number = int(serial_number)
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")
            return

        # Get the current date and time
        call_time = datetime.now()

        # Create a Call object
        call = Call(caller_id, operator_name, call_time, serial_number, software_id, equipment_id)

        # Save the call details
        self.save_call_details(call)

        # Display the call details
        self.display_call_details(call)


        # Clear the entry fields
        self.caller_id_entry.delete(0, tk.END)
        self.operator_name_entry.delete(0, tk.END)
        self.software_id_entry.delete(0, tk.END)
        self.equipment_id_entry.delete(0, tk.END)
        self.serial_number_entry.delete(0, tk.END)



class LoginGUI:
    def __init__(self, root, db):
        self.root = root
        self.root.title("Helpdesk system")
        self.db = db

        # Load and set the background image
        bg_image = Image.open("cool-background.png")
        bg_image = bg_image.resize((1366, 768), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=self.background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create labels and entry fields for username and password
        entry_font = ("Helvetica", 12)
        entry_fg = "white"
        entry_bg = "black"

        title_font = ("Helvetica", 24, "bold")  # Bold and larger font for the title
        title_label = tk.Label(root, text="Helpdesk Login ", font=title_font, bg="sky blue",)
        title_label.place(x=615, y=230)
        title_label.place(x=615, y=230)

        username_label = tk.Label(root, text="Username:", font=entry_font,bg=entry_bg,fg=entry_fg,  anchor="center")
        username_label.place(x=600, y=300)

        password_label = tk.Label(root, text="Password:", font=entry_font,  bg=entry_bg, fg=entry_fg,anchor="center")
        password_label.place(x=600, y=350)

        self.entry_username = tk.Entry(root, font=entry_font, fg=entry_fg, bg=entry_bg)
        self.entry_username.place(x=700, y=300)

        self.entry_password = tk.Entry(root, show="*", font=entry_font, fg=entry_fg, bg=entry_bg)
        self.entry_password.place(x=700, y=350)

        # Create a login button
        button_font = ("Helvetica", 12, "bold")
        button_bg = "#336699"
        button_fg = "white"

        self.button_login = tk.Button(root, text="Login", command=self.login, bg=button_bg, fg=button_fg, font=button_font)
        self.button_login.place(x=755, y=400)

    def login(self):
        # Get the username and password from the entry fields
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if the username and password are correct
        cursor = self.db.cursor()
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Login", "Login Successful")
            self.root.destroy()
            root = tk.Tk()
            app = HelpdeskGUI(root)
            root.geometry("1366x768")
            root.mainloop()
        else:
            messagebox.showerror("Login", "Invalid username or password")

# Create the main window
root = tk.Tk()
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Loveufather@123",
    database="helpdesk"
)

# Create an instance of the LoginGUI class
app = LoginGUI(root, db)
root.geometry("1366x768")
# Start the main event loop
root.mainloop()
