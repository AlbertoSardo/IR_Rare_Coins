# IR Rare Coins

## About

This project aims to gather information about rare coins from various sources and display them on a custom website.

## Installation

### Prerequisites

- Python 3.x
- `pyenv` (optional but recommended)

### Setup Virtual Environment

1. Clone this repository.
2. Navigate to the project directory.
3. Ensure you have Python 3.x installed.
4. Create a virtual environment using `pyenv` (recommended) or `virtualenv`:

    ```bash
    # If using pyenv
    pyenv install 3.x.x  # Install Python 3.x if not already installed
    pyenv virtualenv 3.x.x rare_coins_venv  # Create a virtual environment
    pyenv local rare_coins_venv  # Set the virtual environment for the project directory
    ```

    Replace `3.x.x` with your desired Python version.

5. Activate the virtual environment:

    ```bash
    pyenv activate rare_coins_venv
    ```

6. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once the virtual environment is activated, you can run the project using Python.

In the terminal, ensure that the virtual environment is active (the environment name should be displayed at the beginning of the command line). If not, activate it using:

```bash
pyenv activate rare_coins_venv
```

### Run the project
To run the frontend and the backend:
    ```bash
    uvicorn main:app --reload
    ```