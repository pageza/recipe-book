# ChatGPT Recipe Book

A native desktop application for Ubuntu that uses the OpenAI API (GPT-4) to generate recipes, stores them in an SQLite database, and provides a searchable recipe book interface built with GTK+ 3.

## Features

- **Recipe Generation:**  
  Generate recipes on the fly using ChatGPT with detailed instructions, a list of ingredients, and an estimated calorie count.

- **Recipe Book:**  
  Save generated recipes in an SQLite database.  
  - **Search and Filter:** Search recipes by name or ingredient and filter by calories.
  - **Detailed View:** Select recipes to view full instructions.
  - **Delete Functionality:** Select and delete recipes from your collection (checkbox-based selection).

- **Modular Architecture:**  
  The project is organized into separate modules for database operations (`db.py`), OpenAI integration (`openai_integration.py`), utility functions (`utils.py`), and the GTK user interface (`gui.py`).

- **DevContainer Support:**  
  A `.devcontainer` configuration is provided to enable a consistent development environment using Docker and VSCode Remote Containers on Ubuntu 24.04 LTS.

## Technologies

- **Programming Language:** Python 3
- **User Interface:** GTK+ 3 (via PyGObject)
- **Database:** SQLite
- **API Integration:** OpenAI API (GPT-4)
- **Environment Management:** [python-dotenv](https://pypi.org/project/python-dotenv/)
- **Containerization:** Docker, VSCode DevContainers

## Prerequisites

- **Ubuntu 24.04 LTS** (or a similar Linux distribution)
- **Docker** (if you wish to use the DevContainer)
- **Visual Studio Code** with the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension (for containerized development)
- **Python 3.8+**

## Setup and Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/pageza/recipe-book.git
   cd recipe-book

2. **Create a `.env` File**

    Create a file named `.env` in the project root (this file should be added to your `.gitignore`) and add your OpenAI API key:

    ```dotenv
    OPENAI_API_KEY=your-actual-openai-api-key

3. **Using the VSCode DevContainer (Recommended)**

    1. Open the project folder in VSCode.
    2. Open the Command Palette (`Ctrl+Shift+P`) and select **"Remote-Containers: Reopen in Container"**.
    3. Once the container is running, open a terminal and run:

    ```bash
    python main.py

4. **Running Locally (Without a DevContainer)**

    1. Install the required system packages (if not already installed):

    ```bash
    sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
    ```
    
    2. Install Python dependencies:
    
    ```bash
    pip3 install -r requirements.txt
    ```
    
    3. Run the application:
    ```bash
    python3 main.py
    ```

### Project Structure

```plaintext
recipe-book/
├── .devcontainer/
│   ├── Dockerfile
│   └── devcontainer.json
├── .env             # Contains environment variables (gitignored)
├── .gitignore
├── db.py            # Database initialization and operations
├── gui.py           # GTK user interface and callbacks
├── main.py          # Application entry point
├── openai_integration.py  # OpenAI API integration logic
├── utils.py         # Utility functions (e.g., formatting recipe text)
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

## Usage

**Generate a Recipe:**  
In the "Generate Recipe" tab, enter a prompt (or modifications) and click the **Generate Recipe** button. The generated recipe appears in the output pane.

**Save a Recipe:**  
After generating a recipe, click **Save Recipe** to open a dialog pre-populated with recipe data. Edit as needed and click **OK** to save the recipe to the database.

**View and Delete Recipes:**  
In the "Recipe Book" tab:  
- Use the search bar to filter recipes by name or ingredient.  
- The left pane displays a list of recipes with checkboxes for selection.  
- The right pane shows full recipe details when a recipe is selected.  
- Click **Delete Selected** to remove checked recipes from the database.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- **OpenAI** for the API.
- The **GTK+ community** for PyGObject.
- The **VSCode Remote - Containers team** for their excellent tooling.
