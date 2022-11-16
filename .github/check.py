"""
Script that checks that no .bin/.hex files are missing and that these files 
have matching content.
"""
from pathlib import Path
import sys

bin_files = []
hex_files = []
for filename in Path(".").iterdir():
    if filename.suffix == ".bin":
        bin_files.append(filename.stem)
    elif filename.suffix == ".hex":
        hex_files.append(filename.stem)


error = False
bin_files.sort()
hex_files.sort()

if bin_files != hex_files:
    # check for .bin files without corresponding .hex files
    for bin_file in bin_files:
        if bin_file not in hex_files:
            print("Missing .hex file for `{}`.".format(bin_file+".bin"), file=sys.stderr)
            error = True
    # check for .hex files without corresponding .bin files
    for hex_file in hex_files:
        if hex_file not in bin_files:
            print("Missing .bin file for `{}`.".format(hex_file+".hex"), file=sys.stderr)
            error = True

# check that hex and bin files contain matching 
for filename in bin_files:
    if filename not in hex_files:
        continue
    bin_bytes = Path(filename+".bin").read_bytes()
    hex_bytes = bytes.fromhex(Path(filename+".hex").read_text())
    if bin_bytes != hex_bytes:
        print(f"Content mismatch for {filename}.[hex/bin]:\n    bin: {bin_bytes.hex()}\n    hex: {hex_bytes.hex()}", file=sys.stderr)
        error = True

if error:
    sys.exit(1)
