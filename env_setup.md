# Environment Setup

## API Key Security

For security, the Groq API key should not be hardcoded in the source code. Follow these steps to properly configure your environment:

1. Create a file named `.env` in the project root with the following content:
   ```
   # Groq API key
   GROQ_API_KEY=your_api_key_here
   ```

2. Replace `your_api_key_here` with your actual Groq API key.

3. Install the `python-dotenv` package:
   ```
   pip install python-dotenv
   ```

4. Modify `run_sahtech.py` to load the environment variables from the `.env` file:
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # Load environment variables from .env
   
   # Then use os.environ.get("GROQ_API_KEY") to get the API key
   ```

## Important Security Notes

- Never commit the `.env` file to version control
- Keep your API key confidential
- Regularly rotate your API keys for better security
- In production environments, use proper secrets management systems 