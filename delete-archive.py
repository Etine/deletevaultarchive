import json
import subprocess

# Load the JSON file containing archive IDs
with open('output.json', 'r') as json_file:
    data = json.load(json_file)

# Extract the list of Archive IDs from the JSON data
archive_list = data['ArchiveList']

# Create a log file to track processed Archive IDs
log_file_path = 'deletion_log.txt'
processed_archive_ids = set()

# Check if a log file already exists and load processed Archive IDs
if os.path.exists(log_file_path):
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if line.startswith("Deleted Archive ID: "):
                archive_id = line[len("Deleted Archive ID: "):].strip()
                processed_archive_ids.add(archive_id)

# Loop over each Archive ID and delete it if not processed
for archive in archive_list:
    archive_id = archive['ArchiveId']
    
    # Check if this Archive ID has already been processed
    if archive_id in processed_archive_ids:
        print(f"Skipping Archive ID: {archive_id} (already deleted)")
        continue
    
    # Construct the AWS Glacier delete-archive command
    command = f"aws glacier delete-archive --vault-name awsexamplevault --account-id 111122223333 --archive-id '{archive_id}'"
    
    # Execute the command using subprocess
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Deleted Archive ID: {archive_id}")
        
        # Log the processed Archive ID
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"Deleted Archive ID: {archive_id}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting Archive ID: {archive_id}, Error: {e}")

print("Deletion process completed.")
