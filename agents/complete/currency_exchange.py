import requests

def currency_exchange_tool(currency_from: str, currency_to: str) -> float:
    """
    Get the exchange rate between two currencies.
    
    Args:
        currency_from (str): Source currency code (e.g., 'usd', 'eur')
        currency_to (str): Target currency code (e.g., 'usd', 'eur', 'btc')
    
    Returns:
        float: Exchange rate from source to target currency, or 1.0 if not found
    """

    print(f"🤖 TOOL: Checking currency rates {currency_from}->{currency_to}")

    # Convert to lowercase to match API format
    currency_from = currency_from.lower()
    currency_to = currency_to.lower()

    # If same currency, return 1
    if currency_from == currency_to:
        return 1.0

    try:
        # Make API call to get exchange rates for the source currency
        url = f"https://latest.currency-api.pages.dev/v1/currencies/{currency_from}.json"
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Warning: Unable to fetch exchange rates for '{currency_from}'. HTTP status: {response.status_code}")
            return 1.0
        
        # Parse the JSON response
        data = response.json()
        
        # Check if the source currency data exists
        if currency_from not in data:
            print(f"Warning: Source currency '{currency_from}' not found in the response.")
            return 1.0
        
        # Get the exchange rates for the source currency
        exchange_rates = data[currency_from]
        
        # Check if the target currency is available
        if currency_to not in exchange_rates:
            print(f"Warning: Target currency '{currency_to}' not found for source currency '{currency_from}'.")
            return 1.0
        
        # Return the exchange rate
        print(f"The exchange rate for {currency_from} to {currency_to} is {exchange_rates[currency_to]}")
        return float(exchange_rates[currency_to])
    
    except Exception as e:
        print(f"Warning: An unexpected error occurred: {e}")
        return 1.0