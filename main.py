import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
API_KEY = os.getenv('TICKETMASTER_API_KEY')

url = 'https://app.ticketmaster.com/discovery/v2/events.json'

params = {
    'apikey': API_KEY,
    'city': 'São Paulo',
    'countryCode': 'BR',
    'size': 20,
    'sort': 'date,asc',
    'includeAll': 'true'  # Include additional details like prices
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if '_embedded' in data and 'events' in data['_embedded']:
        events = data['_embedded']['events']
        print("Upcoming Events in São Paulo:")
        print("-" * 50)
        
        current_month = None
        for event in events:
            event_date = datetime.strptime(event['dates']['start']['localDate'], '%Y-%m-%d')
            month_year = event_date.strftime('%B %Y')
            
            if month_year != current_month:
                current_month = month_year
                print(f"\n{month_year.upper()}:")
                print("-" * 50)
            
            print(f"Event: {event['name']}")
            print(f"Date: {event_date.strftime('%d/%m/%Y')}")
            if 'localTime' in event['dates']['start']:
                print(f"Time: {event['dates']['start']['localTime']}")
            if '_embedded' in event and 'venues' in event['_embedded']:
                print(f"Venue: {event['_embedded']['venues'][0]['name']}")
            
            # Price information
            if 'priceRanges' in event:
                for price_range in event['priceRanges']:
                    currency = price_range.get('currency', 'BRL')
                    min_price = price_range.get('min', 0)
                    max_price = price_range.get('max', 0)
                    price_type = price_range.get('type', 'standard')
                    if min_price == max_price:
                        print(f"Price ({price_type}): {currency} {min_price:.2f}")
                    else:
                        print(f"Price Range ({price_type}): {currency} {min_price:.2f} - {max_price:.2f}")
            else:
                print("Price: Check ticket website for prices")
            
            # Add ticket status if available
            if 'dates' in event and 'status' in event['dates']:
                print(f"Status: {event['dates']['status']['code']}")
            
            # Add ticket link if available
            if 'url' in event:
                print(f"Tickets: {event['url']}")
            
            print("-" * 50)
else:
    print(f"Error: {response.status_code}")
    print(f"Response: {response.text}")