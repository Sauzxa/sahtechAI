@echo off
echo Setting up Python 3.10 virtual environment...

rem Create a virtual environment
python -m venv venv

rem Activate the virtual environment
call venv\Scripts\activate

rem Upgrade pip
python -m pip install --upgrade pip

rem Install dependencies from requirements.txt
pip install -r requirements.txt

rem Install Jupyter
pip install notebook

echo Setup completed. To start working, run: venv\Scripts\activate
echo Then run: jupyter notebook 