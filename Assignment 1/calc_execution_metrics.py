"""
Assignment 1, Task 2:
Rreate a program called calc_execution_metrics.py, 
which will require two parameters: --input_csv_file and 
--output_metrics_file

This program will do the following:
(1) Read csv file as pandas
(2) Calculate per exchange average execution speed in seconds. 
    Note that the LastMkt column contains exchange (or broker) IDs
(3) Calculate per exchange, the average savings by comparing limit price 
    vs average execution price (there should be no negative values)

Classmates Cited: Ilija Steinmann & Annie Reynolds
"""

import argparse
import pandas as pd

OUTPUT_COLUMNS = ["LastMkt", "AvgPriceImprovement", "AvgExecSpeedSecs"]

def parse_inputs():
    """
    Helper function to parse command line inputs
    Output: parsed arguments
    """
    parser = argparse.ArgumentParser(description = "Convert FIX to CSV")
    parser.add_argument("--input_csv_file", type = str, help = "Path to CSV Input")
    parser.add_argument("--output_metrics_file", type = str, help = "Path to Metrics Output")
    return parser.parse_args()

def calculate_avg_price_improvement(exchange):
    """
    Helper function that takes an exchange (GroupBy item) 
    and calculates  the average savings by comparing 
    limit price vs average execution price
    Output: avg_price_improvement
    """
    #Convert data to numeric values:
    limit_price = pd.to_numeric(exchange["LimitPrice"], errors = "coerce")
    average_price = pd.to_numeric(exchange["AvgPx"], errors = "coerce")
    #Calculate average savings:
    avg_price_improvement = (limit_price - average_price).mean()
    return avg_price_improvement

def calculate_avg_exec_speed_secs(exchange):
    """
    Helper function that tkes an exchange (GroupBy item) 
    and calculates the average execution speed and returns
    that quantity converted to seconds
    Output: avg_execution_time_secs
    """
    #Convert data to datetime values:
    execution_time = pd.to_datetime(exchange["ExecutionTransactTime"], errors = "coerce")
    transaction_time =  pd.to_datetime(exchange["OrderTransactTime"], errors = "coerce")
    avg_execution_time = (execution_time - transaction_time).mean()
    #Convert to seconds:
    avg_execution_time_secs = avg_execution_time.total_seconds()
    return avg_execution_time_secs

def clean_exchange_name(exchange):
    """
    Helper function that removes symbols from exchange name
    and returns the cleaned name without symbols
    Output: clean_name
    """
    name = str(exchange)
    extra_chars = ["," , "(", ")", "'"]
    for char in extra_chars:
        name = name.replace(char, "")
    clean_name = name.strip()
    return clean_name

def main():
    """
    Main function of this program
    """
    args = parse_inputs()
    input_csv_file = args.input_csv_file
    output_metrics_file = args.output_metrics_file

    #Read csv file as pandas:
    input_df = pd.read_csv(input_csv_file)
    #New dataframe to store relevant metrics:
    output_contents = pd.DataFrame(columns = OUTPUT_COLUMNS)

    #Split by Exchange ID:
    exchanges = input_df.groupby(["LastMkt"])

    #Calculate metrics for each Exchange:
    for exchange_name, exchange_data in exchanges:
        cleaned_name = clean_exchange_name(exchange_name)
        avg_price_improvement = calculate_avg_price_improvement(exchange_data)
        avg_exec_speed_secs = calculate_avg_exec_speed_secs(exchange_data)

        new_output_row = {"LastMkt" : cleaned_name,
                          "AvgPriceImprovement" : avg_price_improvement, 
                          "AvgExecSpeedSecs" : avg_exec_speed_secs
                          }

        #Add new row to output dataframe:
        output_contents = pd.concat([output_contents, pd.DataFrame([new_output_row])],
                                    ignore_index = True)

    #Convert output to CSV:
    output_metrics_file = output_contents.to_csv(args.output_metrics_file, index = False)
    print("Success - Output Metrics Availible")
    return output_metrics_file

if __name__ == "__main__":
    main()
