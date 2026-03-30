# ZipCracker

A lightweight Python utility for CTF challenges, focusing on ZIP file analysis and recovery.

## Features
- **Fake ZIP Encryption Fix**: Automatically detects and unlocks ZIP files with pseudo-encryption by modifying the general purpose bit flag.
- **CRC32 Collision**: Brute-force search for printable strings matching a target CRC32 value, used for checksum bypass.
- **Numeric Password Brute-force**: Recovers simple 4-6 digit passwords for encrypted ZIP archives.

## Usage
```bash
python zip-cracker.py
