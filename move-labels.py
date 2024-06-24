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
def update_card_labels(card_id, label_id, old_label_id, new_label_id):
    delete_card_labels(card_id, old_label_id)
    requests.post(f'https://api.trello.com/1/cards/{card_id}/idLabels?key={key}&token={token}&value={new_label_id}')
    print('Updated label ' + label_id)

def delete_card_labels(card_id, label_id):
    requests.delete(f'https://api.trello.com/1/cards/{card_id}/idLabels/{label_id}?key={key}&token={token}')
    print('Deleted label ' + label_id)

# Main function
def main():
    # Get all cards on the board
    cards = get_cards()

    lw_sales_label_id = ''
    lw_presales_label_id = ''
    tw_sales_label_id = ''
    tw_presales_label_id = ''

    for card in cards:
        if card['name'] == "All Labels":
            for label in card['labels']:
                if label['name'] == 'LW Focus: Sales':
                    lw_sales_label_id = label['id']
                if label['name'] == 'LW Focus: Presales':
                    lw_presales_label_id = label['id']
                if label['name'] == 'TW Focus: Sales':
                    tw_sales_label_id = label['id']
                if label['name'] == 'TW Focus: Presales':
                    tw_presales_label_id = label['id']
            break

    # Loop through each card
    for card in cards:
        if card['name'] != "All Labels":
            for label in card['labels']:
                if label['id'] == tw_sales_label_id:
                    update_card_labels(card['id'], label['id'], tw_sales_label_id, lw_sales_label_id)
                if label['id'] == tw_presales_label_id:
                    update_card_labels(card['id'], label['id'], tw_presales_label_id, lw_presales_label_id)


# Run the main function
if __name__ == '__main__':
    main()
