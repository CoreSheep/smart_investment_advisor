# Smart Investment Advisor

A simple investment advisor application that provides personalized portfolio recommendations based on user's risk profile and investment goals.

## Features

- User-friendly interface for inputting investment preferences
- Risk-based portfolio allocation
- AI-powered investment explanations using OpenAI
- Visual representation of portfolio allocation

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Enter your investment amount
2. Select your risk tolerance level
3. Choose your investment time horizon
4. Click "Generate Investment Plan" to see your personalized recommendation
5. Review the portfolio allocation and AI-generated explanation

## Note

This is a demo application and should not be used for actual investment decisions. Always consult with a qualified financial advisor before making investment decisions. 