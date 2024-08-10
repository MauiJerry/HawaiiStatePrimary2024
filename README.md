# Hawaii 2024 State Primary Processing 

This tool generates Tricaster DataLink and Word DOCX files from a csv text file downloaded from the state website,
It periodically (every 10min) checks to see if there is a new release from state, if so, it downloads
and creates the datalink and word files.

Built with PyCharm using an anaconda environment. 
The create_exe.py will package everything into the dist folder
which can then be moved to other system on the stations network.

Tool will automagically print the word docx file to default printer

It would put tricaster datalink.csv file in proper place if that (network) folder
is connected to the PC and mounted as the datalink folder.

## Configuration

There are several key files that are loaded to configure the system.
* config.env: holds values for variables that alter execution

Two spreadsheet files define the mapping from Contest and Candidate in the State summary file
to Tricaster data files. Most columns match the column names in summary file. 
The DATALINK_ID and DATALINK_VALUE are the names (or prefix of names) used by the Tricaster.  The .ods are OpenOffice spreadsheets as the source, while the .csv are exported with "quote all string fields". 
This insures the string values are actually loaded as strings

* data/ContestKey.ods (.csv): Contests of interest; display names are set here
* data/CandidateKey.ods (.csv): Candidates of interest. display names are set here

## Usage

Test the tool within pyCharm environment.
The config.env file holds several keys that control how the runtime works.
These can be modified on the installation machine

## Contributing and using

If interested in using this, drop me a note, then fork and edit.

## License

This project is public domain, free open source