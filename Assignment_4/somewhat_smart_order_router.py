"""
Assignment 4, Task 2:

Load the models trained in Jupyter Notebook
and implement best_price_improvement() using 
those models

Classmates Cited: Annie Reynolds

"""
from typing import Dict, Optional, Tuple
import pandas as pd
from joblib import load

#Trained Model Paths:
trained_model_paths = {
    'ID1516' : 'gbt_price_improvement_model_ID1516.joblib', 
    'ID29608' :'gbt_price_improvement_model_ID29608.joblib'}

#Function to Load Trained Models:
def load_models(trained_model_paths: Dict[str, str]) -> Dict[str, object]:
    """Helper function that loads the trained models from disk
    from their file paths, using joblib functionality

    Inputs:
        trained_model_paths (List[str]): list of file paths to trained models
    Outputs:
        loaded_models (Dict[str, object]): dictionary of the loaded trained models
    """
    loaded_models = {}
    for exchange_id, path in trained_model_paths.items():
        model = load(path)
        loaded_models[exchange_id] = model

    return loaded_models

#Function to Identify Best Price Improvement:
def best_price_improvement(symbol: Optional[str], side: str, quantity: int,
                           limit_price: float, bid_price: float,
                           ask_price: float, bid_size: int, ask_size: int) -> Tuple[str, float]:
    """
    Accepts a new order and the quotes at the time of the order, 
        runs this input through the price improvement model for each 
        exchange and returns the exchange with the best predicted price 
        improvement

    Inputs:
        symbol: ticker symbol of the stock
        side: 'B' for buy, 'S' for sell
        quantity: number of shares to buy or sell
        limit_price: order limit price
        bid_price: order bid price
        ask_price: order ask price
        bid_size: order bid size
        ask_size: order ask size
    Outputs:
        best_exchange (str): exchange id with the best predicted price improvemnent
        best_price_improvement (float): predicted price improvement at best_exchange
    """

    #Confirm Valid Inputs:
    if side not in ['B', 'S']:
        raise ValueError('Invalid side, must be \'B\' for buy or \'S\' for sell)')
    if quantity <= 0 or not isinstance(quantity, int):
        raise ValueError('Quantity must be positive integer')
    if limit_price <= 0 or bid_price <= 0 or ask_price <= 0 \
        or (not isinstance(limit_price, float)) \
        or (not isinstance(bid_price, float)) \
        or (not isinstance(ask_price, float)):
        raise ValueError('Prices must be positive floats')
    if (bid_size <= 0 or ask_size <= 0) or \
        (not isinstance(bid_size, int)) or (not isinstance(ask_size, int)):
        raise ValueError('Sizes must be positive integers')

    side_numeric = 1 if side == 'B' else 2
    model_input = pd.DataFrame([{
        'side' : side_numeric,
        'order_qty' : quantity,
        'limit_price' : limit_price,
        'bid_price' : bid_price,
        'ask_price' : ask_price,
        'bid_size' : bid_size,
        'ask_size' : ask_size
    }])

    #Store Outputs from Each Model as a Dictionary
        # where keys = Exchange ID & values = predicted price improvement
    price_improvements = {}

    #Load Models:
    loaded_models = load_models(trained_model_paths)
    for exchange_id, model in loaded_models.items():
        prediction = model.predict(model_input)[0]
        price_improvements[exchange_id] = prediction

    #Identify Exchange with Best Predicted Price Improvement:
    best_exchange = max(price_improvements, key=price_improvements.get)
    best_exchange_improvement = float(price_improvements[best_exchange])

    return (best_exchange, best_exchange_improvement)
