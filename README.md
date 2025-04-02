# InterviewCoder Subscription Manager

A simple CLI tool for managing InterviewCoder subscriptions.

## Features

- Sign up for a new account with a 30-day subscription
- Activate a subscription with your existing account
- Choose your preferred programming language
- Beautiful terminal UI using Rich

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -e .
   ```
4. Create a `.env` file with your Supabase credentials:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

## Usage

Simply run the main script:

```bash
python main.py
```

Follow the interactive prompts to:

1. Sign up as a new user or log in as an existing user
2. Enter your email and password
3. Choose your preferred programming language
4. Activate your subscription

## Requirements

- Python 3.11+
- Supabase account
- Dependencies listed in pyproject.toml

<!-- SUPABASE_URL=https://zitarfwubshssxrmpdpi.supabase.co/
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppdGFyZnd1YnNoc3N4cm1wZHBpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA5MDk0NzIsImV4cCI6MjA1NjQ4NTQ3Mn0.eWoOj_9Ei6jF1irPTajVxhpammoPfgxXubc4cV63GiI -->
