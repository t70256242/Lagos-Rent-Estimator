# Lagos Rent Estimator App

## Overview
This is a Flask-based web application that predicts house rental prices in Lagos based on user inputs such as property type, number of bedrooms, number of bathrooms, and location. The app utilizes a trained machine learning model to generate price predictions and provides an interactive user interface built with Flask-WTF and Bootstrap.

## Features
- Predicts house rental prices based on user inputs.
- User-friendly web interface using Flask and Bootstrap.
- Secure contact form with email functionality.
- Dynamic dropdowns for property types and locations.
- Real-time mean price display for reference.

## Technologies Used
- Python (Flask, Flask-WTF, Flask-Bootstrap)
- Machine Learning (scikit-learn, DecisionTreeRegressor)
- Data Handling (Pandas, NumPy, Joblib)
- Frontend (HTML, CSS, Bootstrap)
- SMTP for email functionality

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```sh
   git clone <repo_url>
   cd <repo_folder>
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Create a `.env` file in the root directory and add:
   ```env
   SECRET_KEY=<your_secret_key>
   MY_EMAIL=<your_email>
   MY_PASSWORD=<your_email_password>
   ```
5. Run the application:
   ```sh
   python app.py
   ```
6. Open a browser and navigate to `http://127.0.0.1:5000/`

## File Structure
```
|-- static/
|-- templates/
|-- app.py
|-- load_artifacts.py
|-- requirements.txt
|-- .env
```

## Usage
### Predicting House Prices
1. Select property type, location, number of bedrooms, and bathrooms.
2. Click `Submit` to get a price prediction.

### Contact Form
1. Enter your name, email, subject, and message.
2. Click `Send` to submit the form.

## Model Training
The model is a `DecisionTreeRegressor`, trained using housing rental data. Artifacts such as column names and mean rent prices are stored in JSON files and loaded dynamically.

## License
This project is open-source under the MIT License.

## Author
Ayodele Ayorinde

