import streamlit as st
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please set your OpenAI API key in the .env file")
    st.stop()

openai.api_key = api_key

# Predefined portfolio allocations and specific recommendations
PORTFOLIO_ALLOCATIONS = {
    "Low": {
        "Bonds": {
            "percentage": 70,
            "recommendations": [
                {"name": "Vanguard Total Bond Market ETF (BND)", "ticker": "BND"},
                {"name": "iShares Core U.S. Aggregate Bond ETF (AGG)", "ticker": "AGG"}
            ]
        },
        "Cash": {
            "percentage": 20,
            "recommendations": [
                {"name": "High-Yield Savings Account", "ticker": "N/A"},
                {"name": "Money Market Funds", "ticker": "N/A"}
            ]
        },
        "ETFs": {
            "percentage": 10,
            "recommendations": [
                {"name": "Vanguard Total Stock Market ETF (VTI)", "ticker": "VTI"},
                {"name": "SPDR S&P 500 ETF Trust (SPY)", "ticker": "SPY"}
            ]
        }
    },
    "Medium": {
        "Bonds": {
            "percentage": 40,
            "recommendations": [
                {"name": "Vanguard Total Bond Market ETF (BND)", "ticker": "BND"},
                {"name": "iShares Core U.S. Aggregate Bond ETF (AGG)", "ticker": "AGG"}
            ]
        },
        "Stocks": {
            "percentage": 30,
            "recommendations": [
                {"name": "Apple Inc. (AAPL)", "ticker": "AAPL"},
                {"name": "Microsoft Corporation (MSFT)", "ticker": "MSFT"},
                {"name": "Amazon.com Inc. (AMZN)", "ticker": "AMZN"}
            ]
        },
        "ETFs": {
            "percentage": 20,
            "recommendations": [
                {"name": "Vanguard Total Stock Market ETF (VTI)", "ticker": "VTI"},
                {"name": "Invesco QQQ Trust (QQQ)", "ticker": "QQQ"}
            ]
        },
        "Cash": {
            "percentage": 10,
            "recommendations": [
                {"name": "High-Yield Savings Account", "ticker": "N/A"},
                {"name": "Money Market Funds", "ticker": "N/A"}
            ]
        }
    },
    "High": {
        "Stocks": {
            "percentage": 70,
            "recommendations": [
                {"name": "Tesla Inc. (TSLA)", "ticker": "TSLA"},
                {"name": "NVIDIA Corporation (NVDA)", "ticker": "NVDA"},
                {"name": "Meta Platforms Inc. (META)", "ticker": "META"},
                {"name": "Alphabet Inc. (GOOGL)", "ticker": "GOOGL"}
            ]
        },
        "ETFs": {
            "percentage": 20,
            "recommendations": [
                {"name": "ARK Innovation ETF (ARKK)", "ticker": "ARKK"},
                {"name": "Global X Robotics & Artificial Intelligence ETF (BOTZ)", "ticker": "BOTZ"}
            ]
        },
        "Cash": {
            "percentage": 10,
            "recommendations": [
                {"name": "High-Yield Savings Account", "ticker": "N/A"},
                {"name": "Money Market Funds", "ticker": "N/A"}
            ]
        }
    }
}

def generate_investment_explanation(investment_amount, risk_level, time_horizon, portfolio):
    """Generate investment explanation using OpenAI"""
    prompt = f"""
    Create a personalized investment explanation for a client with the following details:
    - Investment Amount: ${investment_amount:,.2f}
    - Risk Level: {risk_level}
    - Time Horizon: {time_horizon} years
    - Portfolio Allocation: {portfolio}
    
    Please provide a clear, professional explanation of why this portfolio is suitable for their risk profile and investment goals.
    Include brief explanations of why each recommended stock/ETF is included in the portfolio.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional financial advisor providing clear and concise investment advice."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating explanation: {str(e)}"

def main():
    st.set_page_config(page_title="Smart Investment Advisor")
    
    st.title("Smart Investment Advisor")
    st.write("Get personalized investment recommendations based on your risk profile")
    
    # User Input Section
    st.header("Your Investment Profile")
    
    investment_amount = st.number_input(
        "Investment Amount ($)",
        min_value=1000,
        value=10000,
        step=1000
    )
    
    risk_level = st.selectbox(
        "Risk Tolerance",
        ["Low", "Medium", "High"],
        index=1
    )
    
    time_horizon = st.slider(
        "Investment Time Horizon (years)",
        min_value=1,
        max_value=30,
        value=5
    )
    
    if st.button("Generate Investment Plan"):
        # Get portfolio allocation
        portfolio = PORTFOLIO_ALLOCATIONS[risk_level]
        
        # Display Portfolio Allocation
        st.header("Recommended Portfolio Allocation")
        
        # Create data for the bar chart
        allocation_data = {
            "Asset Class": list(portfolio.keys()),
            "Percentage": [asset["percentage"] for asset in portfolio.values()]
        }
        
        st.bar_chart(allocation_data, x="Asset Class", y="Percentage")
        
        # Calculate actual amounts and display recommendations
        st.subheader("Investment Breakdown")
        for asset_class, details in portfolio.items():
            percentage = details["percentage"]
            amount = investment_amount * (percentage / 100)
            
            st.write(f"### {asset_class} (${amount:,.2f} - {percentage}%)")
            st.write("Recommended Investments:")
            
            for rec in details["recommendations"]:
                if rec["ticker"] != "N/A":
                    st.write(f"- {rec['name']} ({rec['ticker']})")
                else:
                    st.write(f"- {rec['name']}")
        
        # Generate and display explanation
        st.header("Investment Explanation")
        explanation = generate_investment_explanation(
            investment_amount,
            risk_level,
            time_horizon,
            portfolio
        )
        st.write(explanation)

if __name__ == "__main__":
    main() 