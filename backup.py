import os
import shutil
from datetime import date, datetime
from tkinter import messagebox
import sys
import zipfile

#create a backup folder with current date and puthon version
#return the path to the new backup folder
def create_backup_folder(destination_path):
    backup_date = date.today().strftime("%Y-%m-%d")
    backup_folder = f"backup_{backup_date}_v{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
    new_path = os.path.join(destination_path, backup_folder)
    os.makedirs(new_path, exist_ok=True)
    return new_path

#backup a single file or folder to the destination path, either zipped or plain
#return true if successful, false otherwise
def backup_item(source_path, destination_path, history_log=None, mode="plain"):
    try:
        base_name = os.path.basename(source_path)
        if mode == "zipped":
            zip_name = os.path.splitext(base_name)[0] + ".zip"
            zip_path = os.path.join(destination_path, zip_name)
            zip_path = check_overwrite(zip_path, zip_name)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isdir(source_path):
                    for root, dirs, files in os.walk(source_path):
                        for file in files:
                            abs_path = os.path.join(root, file)
                            rel_path = os.path.relpath(abs_path, start=source_path)
                            zipf.write(abs_path, arcname=os.path.join(base_name, rel_path))
                else:
                    zipf.write(source_path, arcname=base_name)
        else:           
            if os.path.isdir(source_path):
                folder_name = os.path.basename(source_path)
                final_dst = os.path.join(destination_path, folder_name)
                final_dst = check_overwrite(final_dst, folder_name)
                shutil.copytree(source_path, final_dst, dirs_exist_ok=True)
            else:
                file_name = os.path.basename(source_path)
                final_dst = os.path.join(destination_path, file_name)
                final_dst = check_overwrite(final_dst, file_name)
                shutil.copy2(source_path, final_dst)
            
        if history_log is not None:
            move_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_log.append({
                "src": source_path,
                "dest": destination_path,
                "time": move_time,
                "status": "Complete"
            })
        return True
        
    except Exception as e:
        if history_log is not None:
            move_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_log.append({
                "src": source_path,
                "dest": destination_path,
                "time": move_time,
                "status": f"Failed: {str(e)}"
            })
        return False

#check if file/folder already exists at the path and prompts user to overwrite or get a unique name
#return final path to use
def check_overwrite(path, name):
    if os.path.exists(path):
        if os.path.isdir(path):
            answer = messagebox.askquestion(
                "Folder Already Exists",
                f'Folder "{name}" already exists in this directory.\n\nDo you want to overwrite it?',
                icon='warning'
            )
        else:
            answer = messagebox.askquestion(
                "File Already Exists",
                f'File "{name}" already exists in this directory.\n\nDo you want to overwrite it?',
                icon='warning'
            )
        if answer == 'no':
            path = get_unique_name(path) #to append (1), (2), ...
    return path

#return a unique path by appending (1), (2), ... instead of overwriting (user's choice)
def get_unique_name(path):
    base, ext = os.path.splitext(path)
    counter = 1
    new_path = f"{base} ({counter}){ext}"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base} ({counter}){ext}"
    return new_path


#original backup function before moving it to backup.py, and before implementing zip option:
# def backup(self):
#     if not self.browsedSource and not self.Source_Listbox: #if no source is chosen
#         messagebox.showwarning("No folders are chosen", "Please Select the Backup Source First")
#         return

#     if not self.browsedDestination and not self.Destination_Entry.get():
#         messagebox.showwarning("No folders are chosen", "Please Select the Backup Destination First")
#         return

#     if not self.browsedDestination and self.Destination_Entry.get():
#         self.selected_dest_dir = self.Destination_Entry.get()
#         if not os.path.exists(self.selected_dest_dir):
#             messagebox.showerror("Invalid Path", "The entered destination path does not exist!")
#             return
        
#     try:
#         self.Status_Label.config(text="Backing up...")
#         self.Dest_Path = self.selected_dest_dir
#         self.is_running = True #process started running
#         self.flag = False

#         self.backupDate = date.today().strftime("%Y-%m-%d")
#         self.backupFolder = "backup_"+self.backupDate+"_v"+str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])

#         self.new_path = os.path.join(self.Dest_Path, self.backupFolder)
#         os.makedirs(self.new_path, exist_ok=True)

#         #this code is for choosing one file/folder each time for backup!
#         # if (os.path.isdir(self.Source_Path)):
#         #     #get the parent directory name from the path
#         #     folderName = os.path.basename(self.Source_Path)
#         #     #to include the parent directory not only its children in the backup folder
#         #     final_dst = os.path.join(self.new_path, folderName)

#         #     shutil.copytree(self.Source_Path, final_dst, dirs_exist_ok=True) #dirs_exist_ok=True if the destination directory already exists, copy into it (don't overwrite)
#         #     self.flag=True
#         # else:
#         #     shutil.copy2(self.Source_Path, self.new_path)
#         #     self.flag=True

#         #go through each file/folder the user wants to backup
#         for source in self.selected_sources:
#             try:
#                 if os.path.isdir(source):
#                     folder_name = os.path.basename(source)
#                     final_dst = os.path.join(self.new_path, folder_name)
#                     final_dst = self.checkOverwrite(final_dst, folder_name)
#                     shutil.copytree(source, final_dst, dirs_exist_ok=True)
#                     move_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     self.history_log.append({
#                         "src": source,
#                         "dest": final_dst,
#                         "time": move_time,
#                         "status": "Complete"
#                     })
#                 else:
#                     print(self.new_path)
#                     print(source)
#                     file_name = os.path.basename(source)
#                     final_dst = os.path.join(self.new_path, file_name)
#                     final_dst = self.checkOverwrite(final_dst, file_name)
#                     print(final_dst)
#                     shutil.copy2(source, final_dst)
#                     move_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     self.history_log.append({
#                         "src": source,
#                         "dest": self.new_path,
#                         "time": move_time,
#                         "status": "Complete"
#                     })
#                 self.flag = True
#             except Exception as e:
#                 self.Status_Label.config(text="Error")
#                 messagebox.showwarning("Warning", f"Failed to backup {source}.\nReason: {str(e)}")
#                 move_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 self.history_log.append({
#                         "src": source,
#                         "dest": self.new_path,
#                         "time": move_time,
#                         "status": "Failed"
#                     })
            
#         if self.flag: #the program backed up selected files/folders
#             self.Status_Label.config(text="Done!")
#             messagebox.showinfo("Done!", "Backup Successful!")

#         self.reset() #automatically

#     except Exception as es:  #if any error occurs
#         messagebox.showerror("Error!", f"Error due to {str(es)}")
#     finally:
#         self.is_running = False #mark process as stopped
    