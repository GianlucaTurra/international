# International BE

## Setup

Python version: 3.13
All commands are displayed first for bash and second for batch

1. Create the virtual environment:

   ```bash
   python3 -m venv .venv
   ```

   ```batch
   python -m venv .venv
   ```

2. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

   ```batch
   .venv/bin/activate.bat
   ```

3. Install dependencies:

   There's no difference at this point

   ```bash
   pip install -r requirements.txt
   ```

4. Run the server in debug mode:

   ```bash
   python ./manage.py runserver
   ```

## APIs

Docs about the APIs are generated and available at `localhost:8000/api/docs`.
