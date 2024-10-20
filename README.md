# Current Events to Podcast Automation

This Python project scrapes the latest current events from Wikipedia,
logs into Google Notebook, pastes the scraped content, and generates a
shareable link that is then sent to a Discord channel via a webhook.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [How to Run](#how-to-run)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Additional Notes](#additional-notes)
- [License](#license)

## Prerequisites

1. Python 3.7+ - Make sure Python is installed on your system.
2. Git - Required to clone the repository (optional).
3. Chrome Browser - Required for web scraping and automation.
4. ChromeDriver - Use `undetected-chromedriver` to automate Chrome.
   It should match the installed Chrome version.
5. Discord Webhook - For sending the generated link to a Discord channel.

## Setup

### 1. Clone the Repository

Clone the repository to your local machine:

`git clone https://github.com/mitchelldeamon/current-events-to-podcast.git`

`cd current_events_to_podcast`

### 2. Create a Virtual Environment

It is recommended to use a virtual environment: `python -m venv .venv`

Activate the virtual environment:

- On Windows: `.venv\Scripts\activate`
- On macOS/Linux: `source .venv/bin/activate`

### 3. Install the Requirements

Install the required dependencies using the `requirements.txt` file:

`pip install -r requirements.txt`

### 4. Set Up Environment Variables

Create a `.env` file in the project directory to store your environment variables:

`EMAIL=your_google_email`

`PASSWORD=your_google_password`

`DISCORD_WEBHOOK_URL=your_discord_webhook_url`

`DISCORD_TAG=@your_discord_tag`

- Replace `your_google_email` with your Google email address.
- Replace `your_google_password` with your Google password.
- Replace `your_discord_webhook_url` with the Discord webhook URL.
- Replace `@your_discord_tag` with your Discord tag.

### 5. Verify ChromeDriver Installation

Ensure that ChromeDriver is correctly installed and matches the installed version of Chrome:
pip install undetected-chromedriver

## How to Run

To run the automation script, execute the following command:
python <current_events_to_podcast>.py

## How It Works

### 1. Scrape Current Events:

- The script scrapes current events from Wikipedia for the previous day.
- The content is extracted from the page's HTML and formatted for submission.

### 2. Login to Google Notebook:

- The script opens Google Notebook in Chrome using Selenium.
- It enters the Google account credentials to log in.

### 3. Submit Scraped Content:

- The script navigates through the interface to paste the scraped content into a textarea in Google Notebook.

### 4. Generate Shareable Link:

- After submitting the content, the script generates a shareable link by interacting with the interface.

### 5. Send the Link to Discord:

- The generated link is sent to the specified Discord channel via the webhook.

## Troubleshooting

- Issue: Chrome not launching properly.
  Solution: Ensure that Chrome and ChromeDriver are installed and that their versions match.

- Issue: Environment variables not loading.
  Solution: Check if the `.env` file is correctly set up and located in the project directory.

- Issue: Discord webhook not working.
  Solution: Verify that the webhook URL is correct and that the Discord channel is accessible.

- Issue: Errors related to the ChromeDriver version.
  Solution: Reinstall ChromeDriver to match your version of Chrome using `undetected-chromedriver`.

## Additional Notes

- Security: Avoid sharing your `.env` file publicly, as it contains sensitive information.
- Discord Rate Limits: Be aware that Discord may impose rate limits on the webhook if used frequently.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
