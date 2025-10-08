"""
Task: create a program called fix_to_csv.py, 
which will require two parameters: 
    --input_fix_file and --output_csv_file
"""

import argparse
import sys

#Check that both inputs are provided:
if len(sys.argv) < 2:
    print("Error: Missing file. Please include both --input_fix_file and --output_csv_file.")
    sys.exit(1)

#Parse command line arguments:
parser = argparse.ArgumentParser(description = "Convert FIX to CSV")

parser.add_argument("--input_fix_file", type = str, help = "Path to FIX file")
parser.add_argument("--output_csv_file", type = str, help = "Path to CSV file")

args = parser.parse_args()

input_fix_file = args.input_fix_file
output_csv_file = args.output_csv_file




