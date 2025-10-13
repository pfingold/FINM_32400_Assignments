"""
Assignment 1, Task 1:
Create a program called fix_to_csv.py, 
which will require two parameters: 
    --input_fix_file and --output_csv_file
"""
import argparse
import pandas as pd

#Identifier for SOH character:
SEPARATOR = chr(1)

#Desired orders:
RELEVANT_FIELDS = [
    "35=D",
    "35=8",
    "150=2",
    "39=2",
    "40=2"]

#Output columns for output_csv_file:
OUTPUT_COLUMNS = ["OrderID", "OrderTransactTime", "ExecutionTransactTime",
                  "Symbol", "Side", "OrderQty", "LimitPrice", "AvgPx", "LastMkt"]

def parse_inputs():
    """
    Helper function to parse command line arguments
    """
    parser = argparse.ArgumentParser(description = "Convert FIX to CSV")

    parser.add_argument("--input_fix_file", type = str, help = "Path to FIX file")
    parser.add_argument("--output_csv_file", type = str, help = "Path to CSV file")

    print("Sucess - parsed inputs!")
    return parser.parse_args()

def new_limit_order(message, cloid, orders):
    """
    Helper function that updates the orders dictionary (orders)
    with relevant information from a message (message) for a new 
    limit order based on its orderID (cloid)
    Output: updated order dictionary
    """
    orders[cloid] = {
        "ClOrdID" : cloid,
        "OrderTransactTime" : message.get("60"),
        "Symbol" : message.get("55"),
        "Side" : message.get("54"),
        "OrderQty" : message.get("38"),
        "LimitPrice" : message.get("44")
        }

    return orders

def create_fill_output(message, order):
    """
    Helper function to extract information for a specific Fill notification
    based on content in the original message (message) and the exisitng 
    order (order)

    Output: set that contains the information for a specific Fill
    that will correspond to a new line in the dataframe of order data
    """
    new_row = ({"OrderID" : order.get("ClOrdID"),
                "OrderTransactTime" : order.get("OrderTransactTime"),
                "ExecutionTransactTime" : message.get("60"),
                "Symbol" : order.get("Symbol"),
                "Side" : order.get("Side"),
                "OrderQty" : order.get("OrderQty"),
                "LimitPrice" : order.get("LimitPrice"),
                "AvgPx" : message.get("6"),
                "LastMkt" : message.get("30") })
    return new_row

def main():
    """
    Main function of this program
    """
    args = parse_inputs()
    orders = {}
    new_rows = []

    with open(args.input_fix_file, "r") as f:
        for line in f:
            message = {}
            for part in line.split(SEPARATOR):
                if "=" in part:
                    #split into key-value pairs
                    key, value = part.split("=", 1)
                    message[key] = value
            if not message: #don't address empty message
                continue

            msgtype = message.get("35")
            cloid = message.get("11")

            #Limit orders being sent to the market:
            if msgtype == "D" and message.get("40") == "2":
                orders = new_limit_order(message, cloid, orders)

            #Fills received on those orders:
            elif msgtype == "8":
                if message.get("150") == "2" and message.get("39") == "2":
                    if cloid in orders: #confirm order exists
                        new_row = create_fill_output (message, orders[cloid])
                        new_rows.append(new_row)

    #Store the output in a dataframe:
    output_df = pd.DataFrame(new_rows)
    output_df = output_df.reindex(columns = OUTPUT_COLUMNS)

    #Numeric consistency:
    for column in ["OrderQty", "LimitPrice", "AvgPx"]:
        if column in output_df.columns:
            output_df[column] = pd.to_numeric(output_df[column], errors = "coerce")

    #DateTime consistency:
    for column in ["OrderTransactTime", "ExecutionTransactTime"]:
        if column in output_df.columns:
            output_df[column] = pd.to_datetime(output_df[column], errors = "coerce")

    #Convert dataframe to CSV file:
    output_csv_file = output_df.to_csv(args.output_csv_file, index = False)
    print("Success - FIX to CSV")
    return output_csv_file

if __name__ == "__main__":
    main()
