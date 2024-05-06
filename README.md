# sh-trello-automation

This script is used to manage labels on Trello cards. It can delete specific labels and update the name and color of other labels.

### Prerequisites

- Python 3
- `requests` library
- `python-dotenv` library

You can install the necessary libraries with pip:

```bash
pip install -r requirements.txt
```

### Setup

1. Clone this repository to your local machine.

2. Create a `.env` file in the root directory of the project. This file will store your Trello API key, token, and board ID.

3. Get your Trello API key and token:

   - Go to https://trello.com/app-key and copy the key.
   - Scroll down and click on the 'Token' link to generate a token.
   - Paste both the key and token into your `.env` file like this:

   ```bash
   TRELLO_KEY=your_key_here
   TRELLO_TOKEN=your_token_here
   ```

4. Get your Trello board ID:

   - Open the Trello board you want to manage.
   - The board ID is the last part of the URL (after the last `/`).
   - Paste the board ID into your `.env` file like this:

   ```bash
   TRELLO_BOARD_ID=your_board_id_here
   ```

### Usage

Run the script with Python:

```bash
python move-labels.py
```

The script will get all cards on the specified Trello board, then loop through each card. If a card has a label with the name 'LW Focus: Sales' or 'LW Focus: Presales', that label will be deleted. If a card has a label with the name 'TW Focus: Sales' or 'TW Focus: Presales', that label's name and color will be updated.
