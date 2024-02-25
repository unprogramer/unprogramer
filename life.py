import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import time
import csv
import os
from datetime import datetime

class AgeCalculator:
    """
    A class to calculate remaining time based on current age and life expectancy.

    Attributes:
    - birth_date (str): The birth date of the user in the format dd-mm-yyyy.
    - life_expectancy (int): The potential expected years the user can live.

    Methods:
    - calculate_remaining_time(): Calculates the remaining years, months, weeks, days, hours, and seconds.
    """

    def __init__(self, birth_date, life_expectancy):
        """
        Initializes an AgeCalculator object with the birth date and life expectancy.
        
        Parameters:
        - birth_date (str): The birth date of the user in the format dd-mm-yyyy.
        - life_expectancy (int): The potential expected years the user can live.
        """
        self.birth_date = birth_date
        self.life_expectancy = life_expectancy
    
    def calculate_remaining_time(self):
        """
        Calculates the remaining years, months, weeks, days, hours, and seconds based on the life expectancy and birth date.

        Returns:
        - Tuple containing remaining years, months, weeks, days, hours, and seconds.
        """
        birth_date_obj = datetime.strptime(self.birth_date, "%d-%m-%Y")
        current_date_obj = datetime.now()
        age = current_date_obj.year - birth_date_obj.year - ((current_date_obj.month, current_date_obj.day) < (birth_date_obj.month, birth_date_obj.day))
        remaining_years = self.life_expectancy - age
        remaining_days = remaining_years * 365
        remaining_weeks = remaining_days / 7
        remaining_months = remaining_years * 12
        remaining_hours = remaining_days * 24
        remaining_seconds = remaining_hours * 3600
        return remaining_years, remaining_months, remaining_weeks, remaining_days, remaining_hours, remaining_seconds

class GUI:
    """
    A class to create the graphical user interface for the life countdown application.

    Attributes:
    - master (Tk): The root Tkinter window.
    - emotions_file_path (str): The file path to save emotions data.

    Methods:
    - calculate(): Calculates the remaining time based on user input.
    - calculate_remaining_time(): Calculates the remaining time based on the life expectancy and current age.
    - update_time(): Updates the remaining time in real-time.
    - update_life_score_joyful(): Updates the life score when the joyful button is clicked.
    - update_life_score_sad(): Updates the life score when the sad button is clicked.
    - update_life_score_peaceful(): Updates the life score when the peaceful button is clicked.
    - calculate_life_score(): Calculates the life score based on the button clicked.
    - save_emotions_data(): Saves emotions data to a CSV file.
    - load_emotions_data(): Loads emotions data from a CSV file.
    """

    def __init__(self, master):
        """
        Initializes a GUI object with the root Tkinter window.

        Parameters:
        - master (Tk): The root Tkinter window.
        """
        self.master = master
        self.master.title("Life Countdown")
        
        # Labels
        self.age_label = ttk.Label(master, text="Enter your birth date (dd-mm-yyyy):")
        self.age_label.grid(row=0, column=0, padx=10, pady=5)
        self.age_entry = ttk.Entry(master)
        self.age_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.life_label = ttk.Label(master, text="Enter your potential expected years you can live:")
        self.life_label.grid(row=1, column=0, padx=10, pady=5)
        self.life_entry = ttk.Entry(master)
        self.life_entry.grid(row=1, column=1, padx=10, pady=5)
        
        self.years_label = ttk.Label(master, text="")
        self.years_label.grid(row=2, columnspan=2, padx=10, pady=5)
        
        self.months_label = ttk.Label(master, text="")
        self.months_label.grid(row=3, columnspan=2, padx=10, pady=5)
        
        self.weeks_label = ttk.Label(master, text="")
        self.weeks_label.grid(row=4, columnspan=2, padx=10, pady=5)
        
        self.days_label = ttk.Label(master, text="")
        self.days_label.grid(row=5, columnspan=2, padx=10, pady=5)
        
        self.hours_label = ttk.Label(master, text="")
        self.hours_label.grid(row=6, columnspan=2, padx=10, pady=5)
        
        self.seconds_label = ttk.Label(master, text="")
        self.seconds_label.grid(row=7, columnspan=2, padx=10, pady=5)
        
        self.current_life_score_label = ttk.Label(master, text="Your current life score: 0")
        self.current_life_score_label.grid(row=8, columnspan=2, padx=10, pady=5)
        
        self.today_life_score_label = ttk.Label(master, text="Today's life score: 0")
        self.today_life_score_label.grid(row=9, columnspan=2, padx=10, pady=5)
        
        # Buttons
        self.time_left_button = ttk.Button(master, text="Calculate Time Left", command=self.calculate)
        self.time_left_button.grid(row=10, columnspan=2, padx=10, pady=5)
        
        self.joyful_button = ttk.Button(master, text="Are you joyful today?", command=self.update_life_score_joyful)
        self.joyful_button.grid(row=11, column=0, padx=10, pady=5)
        
        self.sad_button = ttk.Button(master, text="Are you sad today?", command=self.update_life_score_sad)
        self.sad_button.grid(row=11, column=1, padx=10, pady=5)
        
        self.peaceful_button = ttk.Button(master, text="Are you peaceful today?", command=self.update_life_score_peaceful)
        self.peaceful_button.grid(row=12, columnspan=2, padx=10, pady=5)
        
        self.save_button = ttk.Button(master, text="Save Emotions Data", command=self.save_emotions_data)
        self.save_button.grid(row=13, columnspan=2, padx=10, pady=5)
        
        # Initialize emotions data
        self.emotions_data = []
        self.emotions_file_path = ""
        self.load_emotions_data()
        
        # Button state
        self.joyful_clicked = False
        self.sad_clicked = False
        self.peaceful_clicked = False
    
    def calculate(self):
        """
        Calculates the remaining time based on user input and displays it on the GUI.
        """
        try:
            birth_date = self.age_entry.get().strip()
            life_expectancy = int(self.life_entry.get())
            current_date = datetime.now().strftime("%d-%m-%Y")
            
            birth_date_obj = datetime.strptime(birth_date, "%d-%m-%Y")
            current_date_obj = datetime.strptime(current_date, "%d-%m-%Y")
            
            if current_date_obj < birth_date_obj:
                messagebox.showerror("Error", "Birth date cannot be in the future.")
                return
            
            age_calc = AgeCalculator(birth_date, life_expectancy)
            _, remaining_months, remaining_weeks, remaining_days, remaining_hours, remaining_seconds = age_calc.calculate_remaining_time()
            self.calculate_remaining_time(remaining_months, remaining_weeks, remaining_days, remaining_hours, remaining_seconds)
            
            # Display remaining time
            self.years_label.configure(text=f"Remaining Years: {self.remaining_years:.2f}")
            self.months_label.configure(text=f"Remaining Months: {self.remaining_months:.2f}")
            self.weeks_label.configure(text=f"Remaining Weeks: {self.remaining_weeks:.2f}")
            self.days_label.configure(text=f"Remaining Days: {self.remaining_days:.2f}")
            self.hours_label.configure(text=f"Remaining Hours: {self.remaining_hours:.2f}")
            self.seconds_label.configure(text=f"Remaining Seconds: {self.remaining_seconds:.2f}")
            
            # Start the time calculation after button click
            self.start_time = time.time()
            self.update_time()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid birth date and life expectancy.")
    
    def calculate_remaining_time(self, remaining_months, remaining_weeks, remaining_days, remaining_hours, remaining_seconds):
        """
        Calculates the remaining time based on the life expectancy and birth date.

        Parameters:
        - remaining_months (float): Remaining months.
        - remaining_weeks (float): Remaining weeks.
        - remaining_days (float): Remaining days.
        - remaining_hours (float): Remaining hours.
        - remaining_seconds (float): Remaining seconds.
        """
        self.remaining_years = remaining_months / 12
        self.remaining_months = remaining_months
        self.remaining_weeks = remaining_weeks
        self.remaining_days = remaining_days
        self.remaining_hours = remaining_hours
        self.remaining_seconds = remaining_seconds
    
    def update_time(self):
        """
        Updates the remaining time in real-time.
        """
        if hasattr(self, 'start_time'):
            # Calculate elapsed time since start
            elapsed_time = time.time() - self.start_time
            
            # Update remaining seconds based on elapsed time
            self.remaining_seconds -= elapsed_time
            
            # Recalculate remaining time
            self.remaining_years = self.remaining_seconds / (365 * 24 * 3600)
            self.remaining_months = self.remaining_years * 12
            self.remaining_weeks = self.remaining_days / 7
            self.remaining_days = self.remaining_seconds / (24 * 3600)
            self.remaining_hours = self.remaining_seconds / 3600
            
            # Update labels with remaining time
            self.years_label.configure(text=f"Remaining Years: {self.remaining_years:.2f}")
            self.months_label.configure(text=f"Remaining Months: {self.remaining_months:.2f}")
            self.weeks_label.configure(text=f"Remaining Weeks: {self.remaining_weeks:.2f}")
            self.days_label.configure(text=f"Remaining Days: {self.remaining_days:.2f}")
            self.hours_label.configure(text=f"Remaining Hours: {self.remaining_hours:.2f}")
            self.seconds_label.configure(text=f"Remaining Seconds: {self.remaining_seconds:.2f}")
            
            # Call update_time after 1000ms (1 second)
            self.master.after(1000, self.update_time)
    
    def update_life_score_joyful(self):
        """
        Updates the life score when the joyful button is clicked.
        """
        if not self.joyful_clicked:
            self.joyful_clicked = True
            self.sad_button.configure(state="disabled")
            self.peaceful_button.configure(state="disabled")
            self.calculate_life_score(11)
        else:
            messagebox.showinfo("Already clicked", "You have already clicked the joyful button today.")
    
    def update_life_score_sad(self):
        """
        Updates the life score when the sad button is clicked.
        """
        if not self.sad_clicked:
            self.sad_clicked = True
            self.joyful_button.configure(state="disabled")
            self.peaceful_button.configure(state="disabled")
            self.calculate_life_score(-10)
        else:
            messagebox.showinfo("Already clicked", "You have already clicked the sad button today.")
    
    def update_life_score_peaceful(self):
        """
        Updates the life score when the peaceful button is clicked.
        """
        if not self.peaceful_clicked:
            self.peaceful_clicked = True
            self.joyful_button.configure(state="disabled")
            self.sad_button.configure(state="disabled")
            self.calculate_life_score(5)
        else:
            messagebox.showinfo("Already clicked", "You have already clicked the peaceful button today.")
            
    def calculate_life_score(self, score):
        """
        Calculates the life score based on the button clicked.

        Parameters:
        - score (int): The score to be added to the life score.
        """
        current_score = int(self.current_life_score_label.cget("text").split()[-1])
        new_score = current_score + score
        self.current_life_score_label.configure(text=f"Your current life score: {new_score}")
        today_score = int(self.today_life_score_label.cget("text").split()[-1]) + score
        self.today_life_score_label.configure(text=f"Today's life score: {today_score}")
        self.emotions_data.append([datetime.now().strftime("%Y-%m-%d"), score])
    
    def save_emotions_data(self):
        """
        Saves emotions data to a CSV file.
        """
        if not self.emotions_data:
            messagebox.showinfo("No data", "No emotions data to save.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Date', 'Emotion', 'Points'])
                for entry in self.emotions_data:
                    csvwriter.writerow([entry[0], "Joyful" if entry[1] > 0 else "Sad" if entry[1] < 0 else "Peaceful", entry[1]])
            self.emotions_file_path = file_path
            messagebox.showinfo("Emotions Data Saved", f"Emotions data saved successfully at {file_path}")
        else:
            messagebox.showinfo("Save Cancelled", "Saving emotions data cancelled.")

    def load_emotions_data(self):
        """
        Loads emotions data from a CSV file.
        """
        if os.path.exists(self.emotions_file_path):
            with open(self.emotions_file_path, 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip header row
                for row in csvreader:
                    self.emotions_data.append([row[0], int(row[2])])

def main():
    """
    Main function to create and run the GUI.
    """
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

