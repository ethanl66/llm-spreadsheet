# Chat-Based Spreadsheet Application

## Overview
The Chat-Based Spreadsheet application allows users to interact with data in a spreadsheet-like manner through a chat interface. Users can load CSV files, run SQL queries, and receive responses in natural language, making data manipulation intuitive and accessible.

## Features
- Load CSV files into an SQLite database.
- Dynamically create tables based on CSV schema.
- Handle schema conflicts with user prompts.
- Execute SQL queries through a chat interface.
- Generate SQL queries using AI based on user input.

## Project Structure
```
llm-spreadsheet
├── src
│   ├── main.py                # Entry point of the application
│   ├── database
│   │   ├── db_manager.py      # Database operations
│   │   └── schema_handler.py   # Schema management
│   ├── ai
│   │   ├── query_generator.py  # AI query generation
│   │   └── prompt_engineering.py # Prompt crafting for AI
│   ├── utils
│   │   ├── csv_loader.py       # CSV loading utilities
│   │   └── logger.py           # Logging functionality
│   └── cli
│       └── interactive_chat.py  # Chat interaction loop
├── data
│   └── sample.csv              # Sample CSV for testing
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
└── .gitignore                   # Files to ignore in version control
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd chat-based-spreadsheet
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage Guidelines
- Start the application and follow the prompts in the chat interface.
- Load a CSV file by providing the file path when prompted.
- Execute SQL queries by typing them directly into the chat.
- Use natural language to ask for data manipulations, and the AI will generate the corresponding SQL queries.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.