# myhealth

## Description

This is a health tracking application that utilizes the Oura Ring API to retrieve and display personal health data.

## Features

- Retrieve and display sleep data
- Retrieve and display activity data
- Retrieve and display heart rate data
- Retrieve and display body temperature data
- Retrieve and display readiness data

## Installation

To use this application, you need to have an Oura Ring and obtain API credentials from the Oura Ring developer portal. Once you have the credentials, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/takeru-a/myhealth.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure the API credentials:

    ```bash
    touch .streamlit/secrets.toml
    ```

    Open the `secrets.toml` file and replace the placeholders with your actual API credentials.

4. Start the application:

    ```bash
    python -m streamlit run app.py
    ```

5. Open your browser and navigate to `http://localhost:85101` to access the application.

6. Demo
https://myhealth-8jpwvvsqnt3cjr8op8fyem.streamlit.app/

## Usage

Once the application is running, you can navigate through the different sections to view your health data. The data will be fetched from [the Oura Ring API](https://cloud.ouraring.com/v2/docs) and displayed in a user-friendly format.


