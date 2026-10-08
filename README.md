
# File Integrity Monitor

A Python tool that monitors file integrity using SHA-256 hashes.

## Features

- Calculates SHA-256 hashes
- Creates a baseline of monitored files
- Detects modified files
- Detects added and removed files
- Stores baseline data in JSON format

## Technologies

- Python
- SHA-256
- JSON
- File System Operations

## Usage

1. Create a folder named `monitored_files`.
2. Add files you want to monitor.
3. Run the program:

   ```bash
   python integrity_monitor.py
   ```

4. Select `1` to create a baseline.
5. Select `2` to check file integrity.

## Limitations

The baseline is stored locally in a JSON file. If an attacker can modify both the monitored files and the baseline, the results may no longer be trustworthy.

## Ethical Use

Use this tool only on files you own or are authorized to monitor.