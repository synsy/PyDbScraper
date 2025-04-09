import requests
import time
import pandas as pd
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

# Authorization token
access_token = os.getenv("ACCESS_TOKEN")

# API endpoint
url = "https://portal.uooutlands.com/api/VendorSearch/Search"

# List of items to search
search_terms = [
    "bronze mastery chain link Aegis Keep Damage",
    "bronze mastery chain link Alchemy/Healing/Vet",
    "bronze mastery chain link Bard Reset/Break Ignore Chance",
    "bronze mastery chain link Barding Effect Durations",
    "bronze mastery chain link Cavernam Damage",
    "bronze mastery chain link Chest Success Chance / Progress",
    "bronze mastery chain link Chivalry Skill",
    "bronze mastery chain link Damage on Ships",
    "bronze mastery chain link Damage to Barded Creatures",
    "bronze mastery chain link Damage to Creatures Above 66%",
    "bronze mastery chain link Damage to Diseased Creatures",
    "bronze mastery chain link Damage to Poisoned Creatures",
    "bronze mastery chain link Darkmire Temple Damage",
    "bronze mastery chain link Effective Barding Skill",
    "bronze mastery chain link Effective Poisoning Skill",
    "bronze mastery chain link Exceptional Quality Chance",
    "bronze mastery chain link Follower Accuracy/Defense",
    "bronze mastery chain link Inferno Damage",
    "bronze mastery chain link Kraul Hive Damage",
    "bronze mastery chain link Mausoleum Damage",
    "bronze mastery chain link Melee Accuracy/Defense",
    "bronze mastery chain link Melee Aspect Effect Modifier",
    "bronze mastery chain link Melee Damage/Ignore Chance",
    "bronze mastery chain link Melee Special Chance/Special Damage",
    "bronze mastery chain link Melee Swing Speed",
    "bronze mastery chain link Necromancy Skill",
    "bronze mastery chain link Nusero Damage",
    "bronze mastery chain link Netherzone Damage",
    "bronze mastery chain link Ossuary Damage",
    "bronze mastery chain link Poison Damage/Resist Ignore",
    "bronze mastery chain link Ship Cannon Damage",
    "bronze mastery chain link Special/Rare Loot Chance",
    "bronze mastery chain link Spell Damage no Followers",
    "bronze mastery chain link Spirit Speak/Inscription",
    "bronze mastery chain link Trap Damage",
    "bronze mastery chain link Wilderness Damage",
    "silver mastery chain link Chest Success Chances/Progress",
    "silver mastery chain link Chivalry Skill",
    "silver mastery chain link Damage to Barded Creatures",
    "silver mastery chain link Damage to Bleeding Creatures",
    "silver mastery chain link Effective Poisoning Skill",
    "silver mastery chain link Follower Accuracy/Defense",
    "silver mastery chain link Mausoleum Damage",
    "silver mastery chain link Necromancy Skill",
    "silver mastery chain link Netherzone Damage",
    "silver mastery chain link Nusero Damage",
    "silver mastery chain link Pulma Damage",
    "silver mastery chain link Special/Rare Loot Chance",
    "silver mastery chain link Spell Damage No Followers",
    "silver mastery chain link Trap Damage",
    "gold mastery chain link Cavernam Damage",
    "gold mastery chain link Effective Skill on Chest",
    "gold mastery chain link Melee Special Chance/Special Damage",
    "Air aspect core",
    "Arcane aspect core",
    "Artisan aspect core",
    "Blood aspect core",
    "Command aspect core",
    "Death aspect core",
    "Chromatic core",
    "Discipline aspect core",
    "Earth aspect core",
    "Eldritch aspect core",
    "Fire aspect core",
    "Fortune aspect core",
    "Frost aspect core",
    "Gadget aspect core",
    "Harvest aspect core",
    "Holy aspect core",
    "Lightning aspect core",
    "Lyric aspect core",
    "Madness aspect core",
    "Poison aspect core",
    "Shadow aspect core",
    "Void aspect core",
    "Water aspect core"
]

# Headers for the API request
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

# Function to search for a single item
def search_item(item):
    time.sleep(5)
    payload = {
        "page": 0,
        "pageSize": 20,
        "sortName": "Price",
        "sortAscending": True,
        "filterParams": {
            "name": item,
            "propertyFilters": []
        }
    }
    try:
        # Start time
        start_time = time.time()

        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # End time
        end_time = time.time()

        # Process the response if successful
        if response.status_code == 200:
            data = response.json()

            # Calculate average price using the 'calculate_average_price' function
            item_name, average_price, item_count = calculate_average_price(data)

            # Display response time, average price, and results
            response_time = end_time - start_time
            print(f"\nResults for '{item}':")
            print(f"Retrieved in {response_time:.2f} seconds.")
            print(f"Average price: {average_price:.2f} per item (from {item_count} items)")

            return item_name, average_price, item_count

    except requests.exceptions.RequestException as e:
        print(f"\nError occurred during the request for '{item}': {e}")
        if hasattr(e.response, 'status_code'):
            print(f"Error status code: {e.response.status_code}")
        if hasattr(e.response, 'text'):
            print(f"Error response: {e.response.text}")
        return None, None, None  # Return None for error handling

# Function to calculate average price
def calculate_average_price(data):
    """
    Calculates the average price of an item from given data.

    Args:
        data: A dictionary containing item information, including a list of items
              with price and amount.

    Returns:
        A tuple containing:
          - The name of the item.
          - The average price of the item.
          - The number of items used to calculate the average.
    """

    items = data.get('items', [])
    if not items:
        return None, 0, 0  # No items found

    item_name = items[0]['name']  # Get the item name from the first item

    total_price = 0
    item_count = 0

    for item in items:
        total_price += item['price']
        item_count += 1

    if item_count > 0:
        average_price = total_price / item_count
    else:
        average_price = 0

    return item_name, average_price, item_count

# List to store results
results = []

# Loop through each search term
for term in search_terms:
    item_name, average_price, item_count = search_item(term)
    if item_name and average_price and item_count:  # Check for successful search
        results.append([item_name, average_price, item_count])

# Create a Pandas DataFrame
df = pd.DataFrame(results, columns=['Item Name', 'Average Price', 'Amount'])

# Export to Excel
df.to_excel('item_prices.xlsx', index=False)

# Export to Google Sheets (Not fully implemented)
# import gspread
# from google.auth import default
# gc = gspread.authorize(default())
# sheet = gc.create('Item Prices')
# worksheet = sheet.sheet1
# worksheet.update([df.columns.tolist()] + df.values.tolist())
