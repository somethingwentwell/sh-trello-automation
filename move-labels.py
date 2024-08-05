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

# Function to get card actions
def get_card_actions(card_id):
    response = requests.get(f'https://api.trello.com/1/cards/{card_id}/actions?key={key}&token={token}')
    return response.json()

# Function to find specific list IDs
def get_list_ids(list_names):
    response = requests.get(f'https://api.trello.com/1/boards/{board_id}/lists?key={key}&token={token}')
    lists = response.json()
    list_ids = {}
    for lst in lists:
        if lst['name'] in list_names:
            list_ids[lst['name']] = lst['id']
    return list_ids

# Function to move a card to a different list
def move_card_to_inactive(card_id, inactive_list_id):
    requests.put(f'https://api.trello.com/1/cards/{card_id}?idList={inactive_list_id}&key={key}&token={token}')
    print(f'Moved card {card_id} to Inactive list')

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

    # Get the Inactive list ID and other lists to exclude
    list_names_to_exclude = ['Templates', 'Closing', 'Won', 'Lost']
    list_ids = get_list_ids(list_names_to_exclude + ['Inactive'])
    
    inactive_list_id = list_ids.get('Inactive')
    if not inactive_list_id:
        print('No "Inactive" list found on the board.')
        return
    
    excluded_list_ids = {list_ids[name] for name in list_names_to_exclude if list_ids.get(name)}

    # lw_sales_label_id = ''
    # lw_presales_label_id = ''
    # tw_sales_label_id = ''
    # tw_presales_label_id = ''

    # for card in cards:
    #     if card['name'] == "All Labels":
    #         for label in card['labels']:
    #             if label['name'] == 'LW Focus: Sales':
    #                 lw_sales_label_id = label['id']
    #             if label['name'] == 'LW Focus: Presales':
    #                 lw_presales_label_id = label['id']
    #             if label['name'] == 'TW Focus: Sales':
    #                 tw_sales_label_id = label['id']
    #             if label['name'] == 'TW Focus: Presales':
    #                 tw_presales_label_id = label['id']
    #         break

    # Two weeks ago date
    two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)

    # Loop through each card
    for card in cards:
        if card['idList'] in excluded_list_ids or card['name'] == "All Labels":
            continue
        
        # Check if the card has activity in the last two weeks
        actions = get_card_actions(card['id'])
        recent_activity = any(datetime.datetime.strptime(action['date'], '%Y-%m-%dT%H:%M:%S.%fZ') > two_weeks_ago for action in actions)

        if not recent_activity:
            move_card_to_inactive(card['id'], inactive_list_id)
            continue  # Skip the rest of the loop for this card

        # Update labels if necessary
        # for label in card['labels']:
        #     if label['id'] == tw_sales_label_id:
        #         update_card_labels(card['id'], label['id'], tw_sales_label_id, lw_sales_label_id)
        #     if label['id'] == tw_presales_label_id:
        #         update_card_labels(card['id'], label['id'], tw_presales_label_id, lw_presales_label_id)


# Run the main function
if __name__ == '__main__':
    main()
