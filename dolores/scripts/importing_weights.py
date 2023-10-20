# Define the source file path in Google Drive
DRIVE_DIR = '/content/gdrive/My Drive/ASMC/PentaKey/PentaKey/yolov3-spp_final.weights' # Adjust the path in your Google Drive, or keep it default

# Define the destination directory in the local file system
YOLO_BACKUP = '/content/darknet/backup/' # Adjust the backup file name or keep it default

# Copy the file from Google Drive to the local directory
shutil.copy(DRIVE_DIR, YOLO_BACKUP)

# Print a message indicating the location where the training data was saved
print('Saved training data to the local directory at: ' + YOLO_BACKUP)