import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
from modules.SQLiteManager import SQLiteManager

class MeasurementApp:
    """
    GUI application for entering measurement data and interacting with SQLite.
    """

    def __init__(self, db_manager: SQLiteManager):
        """
        Initialize the GUI application.

        @param db_manager: SQLiteManager instance for database interactions
        """
        self.root = tk.Tk()
        self.root.title("ISP Performance Tracking")
        self.root.geometry("650x500")  
        self.root.configure(bg="#f0f0f0")  

        self.db_manager = db_manager
        self.asn_var = tk.StringVar()
        self.measurement_id_var = tk.StringVar()
        self.retention_policy_var = tk.StringVar()
        self.measurement_type_var = tk.StringVar()

        self.retention_policies = ["24 hours", "7 days", "14 days"]
        # self.measurement_types = ["Ping", "Traceroute", "Packetloss"] currently outcommented, because functionality of visulizing traceroute data is not given -> future developement
        self.measurement_types = ["Ping", "Packetloss"]

        self.create_widgets()

    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # main frame for content layout
        frame = ttk.Frame(self.root, padding=15)
        frame.pack(pady=20)

        self.load_logo()
        ttk.Label(self.root, text="", background="#f0f0f0").pack(pady=3)  # spacing under the logo

        # frame for input fields 
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack()

        # as number field
        ttk.Label(input_frame, text="ASN Number:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.asn_var, width=35).grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # measurement id field
        ttk.Label(input_frame, text="Measurement ID:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.measurement_id_var, width=35).grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # retention policy dropdown
        ttk.Label(input_frame, text="Retention Policy:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Combobox(input_frame, textvariable=self.retention_policy_var, values=self.retention_policies, state="readonly", width=33).grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # measurement type dropdown
        ttk.Label(input_frame, text="Measurement Type:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Combobox(input_frame, textvariable=self.measurement_type_var, values=self.measurement_types, state="readonly", width=33).grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        # buttons
        ttk.Button(input_frame, text="Add Measurement", command=self.on_add_measurement).grid(row=4, column=0, columnspan=2, pady=15)
        ttk.Button(input_frame, text="Exit", command=self.on_exit).grid(row=5, column=0, columnspan=2, pady=5)

        # info button
        info_button = ttk.Button(self.root, text="ℹ Info", command=self.show_info, width=6)
        info_button.place(x=590, y=10)  

        # watermark credits 
        credits_label = tk.Label(self.root, text="OTH Regensburg Bachelorthesis - Michael Faltermeier, 2025", font=("Arial", 9), fg="gray", bg="#f0f0f0")
        credits_label.pack(side="bottom", pady=10)  

    def load_logo(self):
        """
        Load and display the logo centered at the top.

        The logo must be located at 'config/logo.png'. If not found, no error is displayed.
        """
        logo_path = "config/logo.png"

        if os.path.exists(logo_path):
            try:
                image = Image.open(logo_path)
                image = image.resize((260, 110), Image.LANCZOS)  
                self.logo = ImageTk.PhotoImage(image)

                logo_label = tk.Label(self.root, image=self.logo, bg="#f0f0f0")
                logo_label.pack(pady=(3, 8), anchor="center")  # ensures logo is at the top
            except Exception as e:
                print(f"Error loading logo: {e}")
        else:
            print("No logo found at 'config/logo.png'.")

    def show_info(self):
        """Show information about the input fields."""
        info_text = (
            "🔹 ASN Number: The Autonomous System Number for the measurement.\n"
            "🔹 Measurement ID: The unique ID of the measurement from RIPE Atlas.\n"
            "🔹 Retention Policy: The time period data will be stored.\n"
            "🔹 Measurement Type: The type of network measurement (Ping, Packetloss)."
        )
        messagebox.showinfo("Input Field Information", info_text)

    def on_add_measurement(self):
        """Add a new measurement to the database."""
        asn = self.asn_var.get().strip()
        measurement_id = self.measurement_id_var.get().strip()
        retention_policy = self.retention_policy_var.get()
        measurement_type = self.measurement_type_var.get()

        if not asn or not measurement_id or not retention_policy or not measurement_type:
            messagebox.showerror("Input Error", "All fields must be filled!")
            return

        if not asn.isdigit() or not measurement_id.isdigit():
            messagebox.showerror("Input Error", "ASN and Measurement ID must be numeric!")
            return

        try:
            self.db_manager.add_measurement(
                measurement_id=measurement_id,
                asn=asn,
                bucket_name=f"AS_{asn}",
                retention_policy=retention_policy,
                interval=60,
                measurement_type=measurement_type
            )
            messagebox.showinfo("Success", f"Measurement ID {measurement_id} added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add measurement: {e}")

    def on_exit(self):
        """Exit the application."""
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Run the GUI application."""
        self.root.mainloop()
