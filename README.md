# NYTimes Article Fetcher

This Python project connects to the New York Times Article Search API and fetches news articles in batches, presenting them as flattened dictionaries. It includes optional arguments for customizing the number of batches and the amount of information displayed.

---

## Features

- Fetches articles in batches from the New York Times API.
- Handles rate-limiting with retry logic.
- Supports incremental fetching and dynamic schema generation.
- User-friendly CLI arguments for controlling behavior.

---

## Requirements

- Python 3.6 or higher
- A valid New York Times API key (stored in a `.env` file)

---

## Setup and Installation

To set up and run this project, follow these steps:

```bash
# Clone the repository
git clone https://github.com/AlexanPetrov/SquirroPython.git

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install dependencies
pip3 install --upgrade pip

# Install dependencies from requirements.txt
pip3 install -r requirements.txt

# Deactivate the virtual environment (when done)
deactivate

# Setup Instructions for Environment Variables and Usage

Create a `.env` file in the project root with the following content:

NYTIMES_API_KEY=your_api_key_here  
BASE_URL=https://api.nytimes.com/svc/search/v2/articlesearch.json  
NYT_PAGE_SIZE=10  

Replace `your_api_key_here` with your actual New York Times API key.

Run the following commands to use the project:

# Run the main script  
python3 main.py  

# Fetch a limited number of batches  
python3 main.py --max_batches 5  

# Display all items in each batch  
python3 main.py --max_batches 5 --show_all
