# Flask Trending Topics App

This is a Flask web application that scrapes trending topics from Twitter (X) using Selenium, stores the data in MongoDB, and serves it through an API. The app also provides a simple frontend to display these topics.

## Project Overview

This project involves two parts:
1. **Flask API** – A backend service that fetches trending topics from Twitter (X) using a Selenium scraper, stores the results in MongoDB, and provides an API to retrieve the topics.
2. **Frontend** – A simple HTML page that fetches and displays the trending topics by calling the Flask API.


## Technologies Used

- **Python**: Backend programming language.
- **Flask**: Web framework for Python.
- **Selenium**: Web scraping tool to fetch trending topics from Twitter.
- **MongoDB**: NoSQL database to store the scraped data.
- **Vercel**: Platform to deploy and host the Flask app.

## Prerequisites

Before getting started, ensure you have the following:
- Python 3.x installed on your machine.
- Node.js and npm for installing Vercel CLI.
- A Vercel account to deploy the app.

## Installation

### Step 1: Clone the Repository
Clone the project repository to your local machine.

```bash
git clone https://github.com/webcrafter000/scraper.git
cd my-flask-app
python app.py


