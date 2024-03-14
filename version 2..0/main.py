import tkinter as tk
from tkinter import filedialog
import pandas as pd

class myGUI:
    def __init__(self, master):
        self.master = master
        master.title("Welcome to Damocles!\nSelect your action:")

        self.import_button = tk.Button(master, text="Import Data", command=self.import_data)
        self.import_button.pack()

        self.run_tests_button = tk.Button(master, text="Run Tests", command=self.run_tests)
        self.run_tests_button.pack()
        
        self.run_tests_button = tk.Button(master, text="Create Database", command=self.run_tests)
        self.run_tests_button.pack()

    def import_data(self):
         
        odbc.importData()

    def run_tests(self):
        
        Tests.mainTests()
        
    def create_database(self):
        
        odbc.createDatabase

if __name__ == "__main__":
    root = tk.Tk()
    gui = myGUI(root)
    root.mainloop()
