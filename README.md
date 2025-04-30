# Sahtech AI Health Advisor

This is a Python implementation of an AI health advisor for the Sahtech application. The system analyzes food products and provides recommendations based on a user's health profile.

## Requirements

- Python 3.10
- Required packages (installed via requirements.txt):
  - groq
  - requests
  - python-dotenv

## Setup

1. Run the setup script to create a virtual environment and install dependencies:

   ```
   .\setup.bat
   ```

2. The script will create a virtual environment (venv) and install all necessary dependencies.

3. Set up your environment variables by creating a `.env` file:
   ```
   # Groq API key
   GROQ_API_KEY=your_api_key_here
   ```
   See `env_setup.md` for more detailed instructions.

## Running the Code

You can run the code in two ways:

### 1. Using the Python Script

Run the standalone Python script:

```
cmd /c "venv\Scripts\activate.bat && python run_sahtech.py"
```

This will execute two example scenarios:
- A user with milk allergy considering a yogurt product
- A user with iron deficiency anemia considering chocolate biscuits

### 2. Using Jupyter Notebook (optional)

If you prefer to use Jupyter Notebook:

```
cmd /c "venv\Scripts\activate.bat && jupyter notebook IA_Sahtech.ipynb"
```

## How It Works

The system:
1. Takes a user health profile and product information
2. Uses an AI agent (powered by Groq) to analyze compatibility
3. Follows a ReAct framework (Thought → Action → Observation)
4. Provides a final recommendation

## Components

- `Agent` class: Manages communication with the Groq LLM API
- Helper functions: 
  - `get_product_data`: Retrieves product information (mock data for testing)
  - `get_user_profile`: Retrieves user health profile (mock data for testing)
  - `compare_product_with_user`: Analyzes compatibility between product and user
  - `detailed_product_report`: Generates readable product reports

## Security Notes

- Never commit your `.env` file containing API keys to version control
- The `.gitignore` file is configured to exclude sensitive files
- Keep your API keys confidential and rotate them regularly
- In production, use proper secrets management systems

## Note

This implementation uses a mock database for demonstration. In a production environment, you would connect to real APIs for product and user data. 