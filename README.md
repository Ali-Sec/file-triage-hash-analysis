# File Triage & Hash Analysis Tool

COMP H2702 - Scripting for Cybersecurity
Scenario C: File Triage & Hash Analysis
Made by: Ali Mustafawi - B00174691

## About the project

For this project I made a Python script that checks all the files inside a folder
and tells you which ones are already known and which ones are not.

For every file, the script gets the name, extension, size, last modified time
and the SHA-256 hash. Then it compares the hash with the list of known hashes
in `hashes_reference.csv`. If the hash is in the list, the file is marked as KNOWN.
If not, it is marked as UNKNOWN.

The script also finds duplicate files. These are files with different names but
the same content, so they have the same hash. At the end, all the results are
saved into a CSV file called `triage_report.csv`.

I chose this scenario because I think hashing is a very useful skill in
cybersecurity. Analysts use it all the time to check if a file is already known
or if two files are the same.

## What is in this repo

- `triage.py` - the main script
- `hashes_reference.csv` - the list of known hashes (given by the lecturer)
- `samples/` - 5 safe sample files to test the script (given by the lecturer)
- `triage_report.csv` - an example of the report the script makes

## What you need

You only need Python 3. I tested it with Python 3.13.

There is no need to install anything else, because I only used modules that
already come with Python: os, sys, csv, hashlib and datetime.

## How to run it

Open a terminal in the project folder and type:

```
python triage.py samples
```

If you want to check another folder, just put the folder path at the end:

```
python triage.py C:\path\to\other\folder
```

If you don't write any folder, the script will use the `samples` folder by default.

## Output

In the terminal you can see the details of every file, its status
(KNOWN, UNKNOWN or ERROR) and the duplicate check at the end.

The same results are saved in `triage_report.csv`, with these columns:
filename, extension, size_bytes, modified, sha256, status, label.
You can open this file in Excel.

## Error handling

I tried to make sure the script does not crash when something goes wrong.
Instead, it shows a message that explains the problem. For example:

- if the folder does not exist
- if `hashes_reference.csv` is missing, or a line in it is broken
  (a SHA-256 hash should always be 64 characters)
- if a file cannot be read (the file gets the status ERROR)
- if the report cannot be saved, for example because it is open in Excel

You can test it with a wrong folder name:

```
python triage.py wrongfolder
```

## Things to keep in mind

- KNOWN means the file is exactly the same as a file in the known list.
- UNKNOWN does not mean the file is dangerous. It only means we don't know it
  yet, so it should be checked more carefully.
- A hash can show if two files are 100% the same, but it can't tell you what the
  file actually does. Even a very small change (like one full stop in sample_c)
  gives a totally different hash.
- All the sample files are safe teaching files from the lecturer. No real
  malware is used, and no files are uploaded online.