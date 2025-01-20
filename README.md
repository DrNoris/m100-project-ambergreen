# AmberGreen Carbon Footprint Calculator

AmberGreen is an AI-powered application designed to calculate, monitor, and predict the carbon footprint of state-owned buildings. It provides actionable recommendations to help institutions reduce their environmental impact while leveraging AI and prediction models for better insights.

## Features

### 🔍 Carbon Footprint Calculation
- Calculates carbon emissions based on monthly utility consumption (electricity, water, heating, etc.).

### 🤖 AI-Powered Recommendations
- Uses **Ollama's Llama3.1** AI integration to generate actionable recommendations for reducing carbon emissions.

### 📈 Carbon Footprint Prediction
- Employs a **modified version of Prophet** to forecast future emissions based on historical utility consumption data.

### 👥 User Roles
- **Institution Users**:
  - Log in to input monthly utility consumption data.
  - View detailed reports and AI-generated recommendations.
- **Guest Users**:
  - View the carbon footprint of state-owned buildings (read-only access).

### 🗂️ Data Storage
- **PostgreSQL** is used for storing user data and utility consumption records.

### 💻 Frontend & Backend
- **Frontend**: Built using **Kivy**.
- **Backend**: Powered by **Python**.

## Current Status

AmberGreen is currently in **demo mode** and requires running directly from an Integrated Development Environment (IDE).

## Technology Stack

- **Frontend Framework**: Kivy
- **Backend Framework**: Python
- **Database**: PostgreSQL
- **AI Integration**: Ollama (Llama3.1)
- **Prediction Framework**: Modified Prophet

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.9+
- PostgreSQL
- Virtual Environment Manager (e.g., Pipenv, virtualenv)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/ambergreen-carbon-footprint-calculator.git
   cd ambergreen-carbon-footprint-calculator
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate 
   ```

3. **Set up the database**:
   - Create a PostgreSQL database.
   - Update the database configuration code.

4. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Institution Users
- **Login Required**: Access the login screen to log in with your institutional credentials.
- **Features**:
  - Input monthly utility consumption data.
  - View detailed reports on carbon emissions and receive AI-powered recommendations.

### Guest Users
- **No Login Required**: Access limited, read-only data.
- **Features**:
  - View the carbon footprint for institutional buildings.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

## Acknowledgments

- **[Ollama](https://ollama.ai/)** for Llama3.1 AI integration.
- **[Prophet](https://facebook.github.io/prophet/)** for advanced prediction capabilities.
- **[Kivy](https://kivy.org/)** for the flexible frontend framework.
- **[PostgreSQL](https://www.postgresql.org/)** for robust and scalable data storage.


