import os
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from threading import *
from backup import create_backup_folder, backup_item

class Main:
    def __init__(self, root):
        self.window = root
        self.window.geometry("720x400")
        self.window.title("File Backup Logger")
        self.window.resizable(width = False, height = False)
        self.window.configure(bg="gray90")
        #initialize variables to track:
        self.selected_sources = [] #user can select as many files/folders to backup as they wish
        self.selected_dest_dir = "" #to store the path selected by the user
        self.browsedSource = False #to check if the user selected a valid source path
        self.browsedDestination = False #to check if the user selected a valid destination path
        self.history_log = [] #to store backed up folders/files history

        #GUI components:
        #frame 1: logo, logging & exit button
        self.frame_1 = Frame(self.window,bg="gray90", width=100, height=100)
        self.frame_1.place(x=20, y=20)
        self.display_logo()
        #exit button to close the application
        Exit_Btn = Button(self.window, text="Exit", font=("Arial", 10, "bold"), fg="red", width=5, command=self.exit_window)
        Exit_Btn.place(x=640, y=20)
        #logging history button
        History_Btn = Button(self.window, text="History Log", font=("Arial", 11, "bold"), fg="black", width=5, command=self.showHistory)
        History_Btn.place(x=638, y=50)

        #frame 2: main page widgets
        self.frame_2 = Frame(self.window, bg="white", width=720, height=480)
        self.frame_2.place(x=0, y=110)
        self.main_window()
        self.history_window = None #to track the open history window

    #application logo and title
    def display_logo(self):
        image = Image.open("Images/file_backup_logo.png")
        resized_image = image.resize((80, 80))
        self.logo = ImageTk.PhotoImage(resized_image)
        label = Label(self.frame_1, bg="gray90",image=self.logo)
        label.pack(side=LEFT, padx=5)
        title_label = Label(self.frame_1, text="File Backup Logger", font=("Arial", 20, "bold"), bg="gray90", fg="black")
        title_label.pack(side=LEFT, padx=10)

    def main_window(self):
        Heading_Label = Label(self.frame_2, text="Please Choose the Source and Destination of the Backup", font=("Arial", 16, "bold"), bg="white", fg="black")
        Heading_Label.place(x=120, y=20)

        Source_Files_Button = Button(self.frame_2, text="Select File(s)", font=("Arial", 10, "bold"), width=10, bg="white", fg="black", command=self.add_files)
        Source_Files_Button.place(x=155, y=70)

        Source_Folders_Button = Button(self.frame_2, text="Select Folder(s)", font=("Arial", 10, "bold"), width=10, bg="white", fg="black", command=self.add_folders)
        Source_Folders_Button.place(x=155, y=95)

        self.Source_Listbox = Listbox(self.frame_2, font=("Arial", 10), bg="white", fg="black", width=39, height=4)
        self.Source_Listbox.place(x=270, y=70)

        Destination_Button = Button(self.frame_2, text="Select Destination", font=("Arial", 10, "bold"), width=10, bg="white", fg="black", command=self.select_destination_directory)
        Destination_Button.place(x=155, y=130)
        self.Destination_Entry = Entry(self.frame_2, font=("Arial", 12), width=32, bg="white", fg="black", insertbackground="black") 
        self.Destination_Entry.place(x=270, y=129)

        self.backup_mode = StringVar(value="plain") #default value
        Label(self.window, text="Select Backup Mode:", font=("Arial", 12, "bold"), bg="white", fg="black").place(x=145, y=275)
        Radiobutton(self.window, text="Plain", font=("Arial", 11), bg="white", fg="black", variable=self.backup_mode, value="plain").place(x=285, y=275)
        Radiobutton(self.window, text="Zipped", font=("Arial", 11), bg="white", fg="black", variable=self.backup_mode, value="zipped").place(x=355, y=275)
        
        Start_Button = Button(self.frame_2, text="Start Backup", font=("Arial", 13, "bold"), bg="white", fg="black", width=8, command=self._threading) #when the "Start" button is clicked, the _threading method starts the organizer in a separate thread to keep the GUI responsive
        Start_Button.place(x=220, y=200)
        Reset_Button = Button(self.frame_2, text="Reset", font=("Arial", 13, "bold"), bg="white", fg="black", width=8, command=self.reset)
        Reset_Button.place(x=350, y=200)

        Status = Label(self.frame_2, text="Backup Status: ", font=("Arial", 12, "bold"), bg="white", fg="black")
        Status.place(x=225, y=235)
        self.Status_Label = Label(self.frame_2, text="Not Started Yet", font=("Arial", 12), bg="white", fg="red")
        self.Status_Label.place(x=325, y=235)

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select file(s)")
        for f in files:
            if f not in self.selected_sources:
                self.selected_sources.append(f)
                self.Source_Listbox.insert(END, f)

    def add_folders(self):
        folder = filedialog.askdirectory(title="Select folder(s)")
        if folder and folder not in self.selected_sources:
            self.selected_sources.append(folder)
            self.Source_Listbox.insert(END, folder)


    def select_destination_directory(self):
        self.selected_dest_dir = filedialog.askdirectory(title = "Select a location") #open a file dialog to let the user choose a folder
        self.Destination_Entry.insert(0, self.selected_dest_dir) #update the entry field with the selected path
        self.selected_dest_dir = str(self.selected_dest_dir)
        #check if the folder path exists or not
        if os.path.exists(self.selected_dest_dir):
            self.browsedDestination = True

    def _threading(self):
        self.x = Thread(target=self.backup, daemon=True)
        self.x.start()

    def reset(self):
        self.Status_Label.config(text="Not Started Yet")
        self.Destination_Entry.delete(0, END)
        self.Source_Listbox.delete(0, END)
        self.selected_sources = []
        self.selected_dest_dir = ""
        self.backup_mode.set("plain")
        self.browsedSource = False
        self.browsedDestination = False
        self.is_running = False

    def backup(self):
        if not self.browsedSource and not self.Source_Listbox:
            messagebox.showwarning("No folders are chosen", "Please Select the Backup Source First")
            return
    
        if not self.browsedDestination and not self.Destination_Entry.get():
            messagebox.showwarning("No folders are chosen", "Please Select the Backup Destination First")
            return
    
        if not self.browsedDestination and self.Destination_Entry.get():
            self.selected_dest_dir = self.Destination_Entry.get()
            if not os.path.exists(self.selected_dest_dir):
                messagebox.showerror("Invalid Path", "The entered destination path does not exist!")
                return
            
        try:
            self.Status_Label.config(text=" s up...")
            self.is_running = True
            self.flag = False

            #use the function from backup.py
            self.new_path = create_backup_folder(self.selected_dest_dir)

            for source in self.selected_sources:
                mode = self.backup_mode.get() #plain or zipped
                success = backup_item(source, self.new_path, self.history_log, mode)
                if success:
                    self.flag = True
                else:
                    self.Status_Label.config(text="Error")
                
            if self.flag:
                self.Status_Label.config(text="Done!")
                messagebox.showinfo("Done!", "Backup Successful!")

            self.reset()
    
        except Exception as es:
            messagebox.showerror("Error!", f"Error due to {str(es)}")
        finally:
            self.is_running = False

    def showHistory(self):
        #if a history window is already open, destroy it before displaying the new one
        if self.history_window is not None and self.history_window.winfo_exists():
            self.history_window.destroy()

        self.history_window = Toplevel(self.window)
        self.history_window.title("History Log")
        self.history_window.geometry("800x500")
        Label(self.history_window, text="Backup History", font=("Arial", 14, "bold")).pack(pady=10)

        text_box = Text(self.history_window, wrap="word", font=("Courier", 12))
        text_box.pack(expand=True, fill="both", padx=10, pady=10)

        if self.history_log:
            for entry in self.history_log:
                text_box.insert(END, "Source: " + entry["src"] + "\n" + "Destination: " + entry["dest"] + "\n" + "Backup Time: " + entry["time"] + "\n" + "Status: " + entry["status"] + "\n\n")
        else:
            text_box.insert(END, "No Backups logged yet.")

        text_box.config(state="disabled")  #read-only

    def exit_window(self):
        self.window.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = Main(root)
    root.mainloop()