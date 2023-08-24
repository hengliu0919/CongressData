import logging

import requests
from datetime import date, timedelta
import PyPDF2
from io import BytesIO
import concurrent.futures
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_URL = "https://api.congress.gov/v3/congressional-record/"
API_KEY_LIST = [
	# please use your own API key
	# https://api.congress.gov/sign-up/
]


def pdf_to_text(pdf_content):
	with BytesIO(pdf_content) as pdf_file:
		reader = PyPDF2.PdfReader(pdf_file)
		text = ""
		for page_num in range(len(reader.pages)):
			text += reader.pages[page_num].extract_text()
	return text


def reformat_text(text):
	# Replace line breaks with spaces
	text_without_breaks = text.replace('\n', '')

	# Remove any hyphenated line breaks
	text_without_breaks = text_without_breaks.replace('- ', '')

	# Remove any  " f "
	text_without_breaks = text_without_breaks.replace(' f ', '\n\n')

	return text_without_breaks.strip()


def fetch_congress_data_for_one_date(date, output_directory_txt, index=0):
	if index >= len(API_KEY_LIST):
		logging.debug(f"Ran out of API keys for {date}")
		return
	if not os.path.exists(output_directory_txt):
		os.makedirs(output_directory_txt)
	txt_file_path = f"{output_directory_txt}/{date}_Senate_1.txt"
	if os.path.exists(txt_file_path):
		logging.debug(f"Skipping {date} as it already exists")
		return
	year, month, day = date.year, date.month, date.day
	try:
		response = requests.get(f"{API_URL}?y={year}&m={month}&d={day}&api_key={API_KEY_LIST[index]}")

		# Check if request was successful
		if response.status_code == 200:
			data = response.json()

			# Extract PDF URLs
			issues = data.get("Results", {}).get("Issues", [])
			if len(issues) == 0:
				logging.debug(f"No issues found for {date}")
				return
			for issue in issues:
				senate_content = issue["Links"].get("Senate", {})
				for pdf in senate_content.get("PDF", []):
					pdf_url = pdf["Url"]

					# Download and save the PDF
					pdf_response = requests.get(pdf_url)

					# Convert PDF to text
					text_content = pdf_to_text(pdf_response.content)

					# Save the content as a txt file
					with open(f"{output_directory_txt}/{date}_Senate_{pdf['Part']}.txt", "w", encoding='utf-8') as f:
						formatted_text = reformat_text(text_content)
						f.write(formatted_text)
						logging.info(f"Finished processing {date} with API key {API_KEY_LIST[index]}")

		else:
			if response.status_code == 429:
				# retry with a different API key
				logging.debug(
					f"API key {API_KEY_LIST[index]} has been rate limited. Trying with a different API key for {date}")
				fetch_congress_data_for_one_date(date, output_directory_txt, index + 1)
	except Exception as e:
		logging.debug(f"Failed to fetch data for {date}. Exception: {e}")


def fetch_congress_data(start_date, end_date, output_directory_text):
	# Create a list of dates to process
	dates_to_process = []
	while start_date <= end_date:
		txt_file_path = f"{output_directory_text}/{start_date}_Senate_1.txt"
		if os.path.exists(txt_file_path):
			logging.debug(f"Skipping {start_date} as it already exists")
		else:
			dates_to_process.append(start_date)
		start_date += timedelta(days=1)

	# # of files in output_directory_text
	logging.info(f"Number of files in {output_directory_text}: {len(os.listdir(output_directory_text))}")
	logging.info(f"Number of dates to process: {len(dates_to_process)}")

	# Use ThreadPoolExecutor to process dates concurrently
	with concurrent.futures.ThreadPoolExecutor() as executor:
		results = [executor.submit(fetch_congress_data_for_one_date, date, output_directory_text)
				   for date in dates_to_process]
		for future in concurrent.futures.as_completed(results):
			future.result()  # This line can be used to catch exceptions if any


def job():
	start_date = date(2009, 1, 1)
	end_date = date(2023, 8, 12)

	# start_date = date(2012, 4, 27)
	# end_date = date(2012, 4, 27)
	fetch_congress_data(start_date, end_date, './output/txt_output')


if __name__ == '__main__':
	job()
