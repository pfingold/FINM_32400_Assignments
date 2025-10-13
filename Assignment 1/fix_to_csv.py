"""
Task: create a program called fix_to_csv.py, 
which will require two parameters: 
    --input_fix_file and --output_csv_file
"""

import argparse
import pandas as pd

#identifier for SOH character
SEPARATOR = chr(1)

#orders to look for
RELEVANT_FIELDS = [
    "35=D",
    "35=8",
    "150=2",
    "39=2",
    "40=2"]

#Output columns in output_csv_file
OUTPUT_COLUMNS = ["OrderID", "OrderTransactTime", "ExecutionTransactTime",
                  "Symbol", "Side", "OrderQty", "LimitPrice", "AvgPx", "LastMkt"]

#FIX messages look like "key = value" where ach key is a tag number &
# value is the value for the tag, each tag-value pair is seprated by SOH

def parse_inputs():
    """
    Helper function to parse command line arguments
    """
    parser = argparse.ArgumentParser(description = "Convert FIX to CSV")

    parser.add_argument("--input_fix_file", type = str, help = "Path to FIX file")
    parser.add_argument("--output_csv_file", type = str, help = "Path to CSV file")

    print("Sucess - parsed inputs!")
    return parser.parse_args()

def main():
    args = parse_inputs()
    orders = {}
    new_rows = []

    with open(args.input_fix_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            message = {}
            message_parts = line.split(SEPARATOR)
            for part in message_parts:
                if "=" in part:
                    #split into key-value pairs
                    key, value = part.split("=", 1)
                    message[key] = value

            if not message: #don't address empty message
                continue

            msgtype = message.get("35")
            #print("message type: ", msgtype)

            #Limit orders being sent to the market:
            if msgtype == "D" and message.get("40") == "2":
                cloid = message.get("11")
                if cloid:
                    orders[cloid] = {
                        "ClOrdID" : cloid,
                        "OrderTransactTime" : message.get("60"),
                        "Symbol" : message.get("55"),
                        "Side" : message.get("54"),
                        "OrderQty" : message.get("38"),
                        "LimitPrice" : message.get("44")
                        }
                    print("new limit order added!")

            #Fills received on those orders:
            elif msgtype == "8":
                if message.get("150") == "2" and message.get("39") == "2":
                    cloid = message.get("11")

                    if cloid and cloid in orders:
                        o = orders[cloid]
                        new_rows.append({
                            "OrderID" : o.get("ClOrdID"),
                            "OrderTransactTime" : o.get("OrderTransactTime"),
                            "ExecutionTransactTime" : message.get("60"),
                            "Symbol" : o.get("Symbol"),
                            "Side" : o.get("Side"),
                            "OrderQty" : o.get("OrderQty"),
                            "LimitPrice" : o.get("LimitPrice"),
                            "AvgPx" : message.get("6"),
                            "LastMkt" : message.get("30")
                        })
                        print("added a new row!")

    output_df = pd.DataFrame(new_rows)
    output_df = output_df.reindex(columns = OUTPUT_COLUMNS)

    #Numeric Consistency:
    for column in ["OrderQty", "LimitPrice", "AvgPx"]:
        if column in output_df.columns:
            output_df[column] = pd.to_numeric(output_df[column], errors = "coerce")

    #DateTime Consistency:
    for column in ["OrderTransactTime", "ExecutionTransactTime"]:
        if column in output_df.columns:
            output_df[column] = pd.to_datetime(output_df[column], errors = "coerce")


    output_csv_file = output_df.to_csv(args.output_csv_file, index = False)
    print("Success - FIX to CSV")
    return output_csv_file

if __name__ == "__main__":
    main()

"""
python3 fix_to_csv.py --input_fix_file cleaned.fix --output_csv_file executions.csv
"""