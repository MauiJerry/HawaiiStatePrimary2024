import subprocess
import os
import shutil

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

# Run the command
subprocess.run(command, check=True)

# Move the executable to a desired location (optional)
dist_dir = 'dist'
exe_filename = os.path.splitext(script_file)[0] + '.exe'
exe_file = os.path.join(dist_dir, exe_filename )

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
