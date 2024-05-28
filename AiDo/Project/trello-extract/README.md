# Trello Extract

Trello Extract is a Python project that uses the `py-trello` library and `python-dotenv` to authenticate with the Trello API and fetch details from Trello boards, lists, and cards. This project demonstrates how to securely manage API credentials and interact with Trello's API to retrieve project data for further processing.

## Features

- Authenticate with the Trello API using OAuth.
- Fetch details of all accessible Trello boards.
- Retrieve lists and cards from a specified Trello board.
- Securely manage API credentials using environment variables.

## Requirements

- Python 3.11+

## Setup

### Step 1: Register for Trello API Access

1. **Sign Up for a Trello Account**:

   - If you don't have a Trello account, sign up at [Trello](https://trello.com/).

2. **Get API Key and Token**:
   - Go to the [Trello Developer Portal](https://trello.com/app-key).
   - Copy your API Key.
   - Click on the "Token" link to generate a token. This token will be used for authentication in your API requests.

### Step 2: Install Necessary Python Packages

1. Setup a virtual environment with dependencies and activate it:

```bash
brew install hatch
hatch env create
hatch shell
```

### Step 3: Configure Environment Variables

1. Copy the env.local file to a new file named .env

```bash
cp env.local .env
```

2. Update `.env` file with your Trello API credentials:

```
TRELLO_API_KEY=your_api_key
TRELLO_API_SECRET=your_api_secret
TRELLO_OAUTH_TOKEN=your_oauth_token
TRELLO_OAUTH_TOKEN_SECRET=your_oauth_token_secret
```

### Step 4: Run the Script

Run the script to authenticate and fetch data from your Trello board:

```bash
python trello_integration.py
```

## Usage

The `trello_integration.py` script will:

1. Authenticate with the Trello API using the credentials provided in the `.env` file.
2. Fetch and print the details of all accessible Trello boards.
3. Fetch and print the lists and cards from the first Trello board in the list.

### Example Output

```
Boards:
- Example Board (ID: 1234567890abcdef12345678)

Fetching details for board: Example Board
Board Details: {'name': 'Example Board', 'description': 'This is an example Trello board.', 'url': 'https://trello.com/b/12345678/example-board'}

Lists in Example Board:
- To Do (ID: 1234567890abcdef12345678)
- In Progress (ID: 1234567890abcdef12345679)
- Done (ID: 1234567890abcdef12345680)

Cards in list To Do:
- {'name': 'Example Card 1', 'description': 'This is an example card.', 'due_date': None, 'url': 'https://trello.com/c/12345678/example-card-1'}
- {'name': 'Example Card 2', 'description': 'This is another example card.', 'due_date': '2024-06-01T12:00:00.000Z', 'url': 'https://trello.com/c/12345679/example-card-2'}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue to improve this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
