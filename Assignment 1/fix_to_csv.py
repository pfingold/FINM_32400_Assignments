"""
Task: create a program called fix_to_csv.py, 
which will require two parameters: 
    --input_fix_file and --output_csv_file
"""

import argparse
import pandas as pd

#Parse command line arguments:
parser = argparse.ArgumentParser(description = "Convert FIX to CSV")

parser.add_argument("--input_fix_file", type = str, help = "Path to FIX file")
parser.add_argument("--output_csv_file", type = str, help = "Path to CSV file")

args = parser.parse_args()

input_fix_file = args.input_fix_file
output_csv_file = args.output_csv_file

#identifier for SOH character
SEPARATOR = "\x01"

#Output columns in output_csv_file
OUTPUT_COLUMNS = ["OrderID", "OrderTransactTime", "ExecurtionTransactTime",
                  "Symbol", "Side", "OrderQty", "LimitPrice", "AvgPx", "LastMkt"]

RELEVANT_FIELDS = [
    "35=D",
    "35=8",
    "150=2",
    "39=2",
    "40=2"]

output_df = pd.DataFrame(index = OUTPUT_COLUMNS)
#FIX messages look like "key = value" where ach key is a tag number &
# value is the value for the tag, each tag-value pair is seprated by SOH

#split soh by doing .split(\x01) or .split(chr(1))

with open(input_fix_file, "r") as f:
    for line in f: 
        fix_messages = line.strip().split(SEPARATOR)
        #parse each field here
        for message in fix_messages:
            if message in RELEVANT_FIELDS:
                #add the line to the output df
                line.strip(SEPARATOR)
                output_df = pd.concat([output_df, pd.DataFrame([message])],
                                      ignore_index = True) #is this correct?
                break


output_csv_file = output_df.to_csv("output_csv_file", columns = OUTPUT_COLUMNS)

def main():
    ...

if __name__ == "main":
    main()