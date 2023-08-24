# Congress Data Fetcher

## Description
The `Congress Data Fetcher` is a Python script designed to fetch data from the Congress API and extract text content from the available PDFs. Specifically, this tool fetches Senate-related documents from a given date range, converts the PDF documents to text, and saves the text in an output directory.

Key Features:
- Extracts text from PDF documents retrieved from the Congress API.
- Processes dates concurrently for improved efficiency.
- Handles API rate limiting by switching to alternative API keys.
- Outputs text to a specified directory with a structured naming convention.

## Prerequisites
1. Python 3.x
2. You must have an API key to access the Congress API. For registration and key access, visit [Congress API Sign-Up](https://api.congress.gov/sign-up/).

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone git@github.com:hengliu0919/CongressData.git
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the `API_KEY_LIST` in the script with your obtained API keys:
   ```python
   API_KEY_LIST = [
	   "YOUR_API_KEY_HERE",
	   #... add additional keys if available
   ]
   ```

## Usage
To run the script and fetch Congress data:
```bash
python congressData.py
```
By default, the script fetches data from January 1, 2009, to August 12, 2023, and stores the text output in the `./output/txt_output` directory. You can adjust these dates within the `job()` function.

## Output
The extracted text from each Senate document will be saved as `.txt` files in the `./output/txt_output` directory, following the naming convention: `<date>_Senate_<part>.txt`.

## Troubleshooting & Logging
The script utilizes logging to provide real-time feedback on the data fetching process. Log messages include successful data fetches, skipped dates, rate limiting notifications, and any exceptions encountered.
