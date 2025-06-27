# File Backup Logger

## Description
This program is a GUI that backs up files and directories with versioning and logs the operations locally with their status.

## Functionalities Implemented
- User can either back up the file/folder zipped or plain, depending on what they select in the user interface.
- *If a file/folder already exists in the backup location, user is asked if they'd like to overwrite it or create a copy of it, appending the copy number to the name 
- User can select more than one file and/or folder each time for backing up, and can enter the destination path either manually or through the file dialog
- History log showing the backed up files/folders, the time of backup, source & destination, as well as the status of the backup.
- A status label that updates the user on the status of the operation (Not Started Yet, Backing up, Done)
- Popup notifications that guide the user when using the application (e.g. "Please Select the Backup Source First", "Please Select the Backup Destination First", "The entered destination path does not exist!", "Backup Successful", ...)
- Error handling: the application includes try-except blocks to handle potential errors during file operations and displays user-friendly error messages when something goes wrong.

## Instructions
- Upon running the application, the user interface is shown in ApplicationScreenshots/GUI.png
- First, select the file(s) and/or folder(s) you want to organize, by clicking on the "Select File(s)" and "Select Folder(s)" buttons.
- Then, select one of the two modes of backup, Plain or Zipped.
- If you would like to reset the selected data, press the "Reset" button.
- Lastly, press the "Start" button to start backing up the selected files/folders.
- To see the backed up files/folders history, click on the "History Log" button at the top right corner. There you can see the source path, destination path, the time the backup was made, and the status of the operation. It is shown in ApplicationScreenshots/HistoryLog.png

- See ApplicationScreenshots/PlainFilesAndFoldersSelection.png, ApplicationScreenshots/backup_2025-06-27_v3.12.6(1)
- See ApplicationScreenshots/ZippedFilesAndFoldersSelection.png, ApplicationScreenshots/backup_2025-06-27_v3.12.6(2)
- *See ApplicationScreenshots/OverwriteMessage.png, ApplicationScreenshots/backup_2025-06-27_v3.12.6(3)

## Unimplemented
- Add file count and backup duration: due to time constraint.
- Add config file (e.g., .json) to store user preferences (folders, backup interval): did not understand