"""
Please create a program called calc_execution_metrics.py, 
which will require two parameters: --input_csv_file and 
--output_metrics_file

This program will do the following:

Read csv file as pandas
Calculate per exchange average execution speed in seconds. 
    Note that the LastMkt column contains exchange (or broker) IDs
Calculate per exchange, the average savings by comparing limit price 
    vs average execution price (there should be no negative values)

"""

import argparse
import pandas as pd

OUTPUT_COLUMNS = ["LastMkt", "AvgPriceImprovement", "AvgExecSpeedSecs"]

#Parse command line arguments:
parser = argparse.ArgumentParser(description = "Convert FIX to CSV")

parser.add_argument("--input_csv_file", type = str, help = "Path to CSV Input")
parser.add_argument("--output_metrics_file", type = str, help = "Path to Metrics Output")

args = parser.parse_args()

input_csv_file = args.input_csv_file
output_metrics_file = args.output_metrics_file

#Read csv file as pandas:
input_df = pd.read_csv(input_csv_file)

output_contents = pd.DataFrame(index = OUTPUT_COLUMNS)

#Split by Exchange ID:
exchanges = input_df.groupby(["LastMkt"])

#Calculate metrics for each Exchange:
for exchange in exchanges:
    exchange_size = exchange.count()

    #Average Execution Speed
    total_execution_time = exchange.apply(lambda x: x["ExecutionTransactTime"] -
                                          x["OrderTransactTime"]).sum()
    avg_execution_time = total_execution_time / exchange_size

    #Average Savings
    total_execution_price = exchange.apply(lambda x: x["LimitPrice"] -
                                           x["AvgPx"]).sum()
    #^does this take the sum of all the orders per exchange?
    avg_price_improvement = total_execution_price / exchange_size

    new_output_row = [exchange, avg_price_improvement, avg_execution_time]

    #add new row to output dataframe
    output_contents = pd.concat([output_contents, pd.DataFrame(new_output_row)],
                                ignore_index = True)

output_metrics_file = output_contents.to_csv("output_metrics_file", columns = OUTPUT_COLUMNS)

def main():
    ...

if __name__ == "main":
    main()