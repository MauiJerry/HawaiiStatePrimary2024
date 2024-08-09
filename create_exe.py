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
#shutil.copy(exe_file, "run_primaryResultsTool.exe")

data_folder = "data"
contest_file_name = "ContestKey.csv"
candidate_file_name = "CandidateKey.csv"
contest_file_path = os.path.join(data_folder, contest_file_name)
candidate_file_path = os.path.join(data_folder, candidate_file_name)
shutil.copy(contest_file_path,dist_dir+"/"+data_folder+"/"+contest_file_name)
shutil.copy(candidate_file_path,dist_dir+"/"+data_folder+"/"+candidate_file_name)


print(f"Executable created at: {exe_file}")
