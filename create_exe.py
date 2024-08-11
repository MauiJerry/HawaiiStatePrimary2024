import subprocess
import os
import shutil
import logging


# Configure local logger
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


# Define your main script file and additional options
script_file = 'runHIStatePrimary.py'
icon_file = 'icon_for_runHIStatePrimary.ico'  # Optional, if you have an icon file

# Build the PyInstaller command
command = [
    'pyinstaller',
    '--onefile',
    '--icon=' + icon_file,
    script_file
]

exe_filename = os.path.splitext(script_file)[0] + '.exe'

# Run the command
res = subprocess.run(command, check=True)

# Move the executable to a desired location (optional)
dist_dir = './dist'
exe_file = os.path.join(dist_dir, exe_filename )
print(f"Result of pyinstaller {res} \n\tshould be at {exe_file}")
if os.path.isfile(exe_file):
    print ("Exe file exists")
else:
    print("WARNING: exe file does not seem to exist")
    logger.error(f"Failed to create exe {exe_file}")
    raise ValueError(f"Failed to create exe {exe_file}")

data_folder = "data"
dist_data_folder = os.path.join(dist_dir, data_folder)
os.makedirs(dist_data_folder, exist_ok=True)

contest_file_name = "ContestKey.csv"
candidate_file_name = "CandidateKey.csv"
contest_file_path = os.path.join(data_folder, contest_file_name)
candidate_file_path = os.path.join(data_folder, candidate_file_name)

config_file = "config.env"
dist_config = os.path.join(dist_dir, config_file)
shutil.copy2(config_file, dist_config)

# Copy all files from source to destination
for filename in os.listdir(data_folder):
    source_file = os.path.join(data_folder, filename)
    destination_file = os.path.join(dist_data_folder, filename)
    if os.path.isfile(source_file):
        shutil.copy2(source_file, destination_file)


#contest_file_name = "ContestKey.csv"
#candidate_file_name = "CandidateKey.csv"
#contest_file_path = os.path.join(data_folder, contest_file_name)
#candidate_file_path = os.path.join(data_folder, candidate_file_name)
#shutil.copy(f"{data_folder}/*",dist_dir)
# shutil.copy(contest_file_path,dist_dir+"/"+data_folder+"/"+contest_file_name)
# shutil.copy(candidate_file_path,dist_dir+"/"+data_folder+"/"+candidate_file_name)
# shutil.copy(config_file,dist_dir+"/"+config_file)


print(f"Executable created at: {exe_file}")
