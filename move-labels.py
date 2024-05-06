import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Trello API key and token
key = os.environ['TRELLO_KEY']
token = os.environ['TRELLO_TOKEN']

# ID of your Trello board
board_id = os.environ['TRELLO_BOARD_ID']

# Function to get all cards on the board
def get_cards():
    response = requests.get(f'https://api.trello.com/1/boards/{board_id}/cards?key={key}&token={token}')
    return response.json()

# Function to update a card's labels
def update_card_labels(label_id, new_label_name, new_label_color):
    requests.put(f'https://api.trello.com/1/labels/{label_id}?key={key}&token={token}&name={new_label_name}&color={new_label_color}')
    print('Updated label ' + label_id)

def delete_card_labels(label_id):
    requests.delete(f'https://api.trello.com/1/labels/{label_id}?key={key}&token={token}')
    print('Deleted label ' + label_id)

# Main function
def main():
    # Get all cards on the board
    cards = get_cards()

    # Loop through each card
    for card in cards:
        for label in card['labels']:
            if label['name'] == 'LW Focus: Sales':
                delete_card_labels(label['id'])
            if label['name'] == 'LW Focus: Presales':
                delete_card_labels(label['id'])

    for card in cards:
        for label in card['labels']:
            if label['name'] == 'TW Focus: Sales':
                update_card_labels(label['id'], 'LW Focus: Sales', 'orange')
            if label['name'] == 'TW Focus: Presales':
                update_card_labels(label['id'], 'LW Focus: Presales', 'purple')


# Run the main function
if __name__ == '__main__':
    main()
