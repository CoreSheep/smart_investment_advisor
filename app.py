import streamlit as st
import os
import openai
from dotenv import load_dotenv
import plotly.graph_objects as go

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
            "color": "#2E86C1",  # Blue
            "recommendations": [
                {"name": "Vanguard Total Bond Market ETF (BND)", "ticker": "BND"},
                {"name": "iShares Core U.S. Aggregate Bond ETF (AGG)", "ticker": "AGG"}
            ]
        },
        "Cash": {
            "percentage": 20,
            "color": "#27AE60",  # Green
            "recommendations": [
                {"name": "High-Yield Savings Account", "ticker": "N/A"},
                {"name": "Money Market Funds", "ticker": "N/A"}
            ]
        },
        "ETFs": {
            "percentage": 10,
            "color": "#F1C40F",  # Yellow
            "recommendations": [
                {"name": "Vanguard Total Stock Market ETF (VTI)", "ticker": "VTI"},
                {"name": "SPDR S&P 500 ETF Trust (SPY)", "ticker": "SPY"}
            ]
        }
    },
    "Medium": {
        "Bonds": {
            "percentage": 40,
            "color": "#2E86C1",  # Blue
            "recommendations": [
                {"name": "Vanguard Total Bond Market ETF (BND)", "ticker": "BND"},
                {"name": "iShares Core U.S. Aggregate Bond ETF (AGG)", "ticker": "AGG"}
            ]
        },
        "Stocks": {
            "percentage": 30,
            "color": "#E74C3C",  # Red
            "recommendations": [
                {"name": "Apple Inc. (AAPL)", "ticker": "AAPL"},
                {"name": "Microsoft Corporation (MSFT)", "ticker": "MSFT"},
                {"name": "Amazon.com Inc. (AMZN)", "ticker": "AMZN"}
            ]
        },
        "ETFs": {
            "percentage": 20,
            "color": "#F1C40F",  # Yellow
            "recommendations": [
                {"name": "Vanguard Total Stock Market ETF (VTI)", "ticker": "VTI"},
                {"name": "Invesco QQQ Trust (QQQ)", "ticker": "QQQ"}
            ]
        },
        "Cash": {
            "percentage": 10,
            "color": "#27AE60",  # Green
            "recommendations": [
                {"name": "High-Yield Savings Account", "ticker": "N/A"},
                {"name": "Money Market Funds", "ticker": "N/A"}
            ]
        }
    },
    "High": {
        "Stocks": {
            "percentage": 70,
            "color": "#E74C3C",  # Red
            "recommendations": [
                {"name": "Tesla Inc. (TSLA)", "ticker": "TSLA"},
                {"name": "NVIDIA Corporation (NVDA)", "ticker": "NVDA"},
                {"name": "Meta Platforms Inc. (META)", "ticker": "META"},
                {"name": "Alphabet Inc. (GOOGL)", "ticker": "GOOGL"}
            ]
        },
        "ETFs": {
            "percentage": 20,
            "color": "#F1C40F",  # Yellow
            "recommendations": [
                {"name": "ARK Innovation ETF (ARKK)", "ticker": "ARKK"},
                {"name": "Global X Robotics & Artificial Intelligence ETF (BOTZ)", "ticker": "BOTZ"}
            ]
        },
        "Cash": {
            "percentage": 10,
            "color": "#27AE60",  # Green
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
    As a professional financial advisor, provide a concise and clear investment recommendation based on:
    
    Investment Profile:
    - Amount: ${investment_amount:,.2f}
    - Risk Tolerance: {risk_level}
    - Time Horizon: {time_horizon} years
    
    Portfolio Allocation:
    {portfolio}
    
    Please provide:
    1. A brief overview of why this allocation suits their profile
    2. Key benefits of each asset class in their portfolio
    3. One sentence explanation for each recommended investment
    Keep the explanation professional but easy to understand.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional financial advisor providing clear and concise investment advice."},
                {"role": "user", "content": prompt}
            ]
        )
        # 兼容不同模型返回格式
        if hasattr(response.choices[0], 'message') and hasattr(response.choices[0].message, 'content'):
            return response.choices[0].message.content.strip()
        elif hasattr(response.choices[0], 'text'):
            return response.choices[0].text.strip()
        else:
            return "[No explanation returned by LLM]"
    except Exception as e:
        return f"Error generating explanation: {str(e)}"

def main():
    st.set_page_config(
        page_title="Smart Investment Advisor",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
        .main {padding: 1rem 2rem 0.5rem 2rem;}
        .stButton>button {
            width: 100%;
            background-color: #23304A;
            color: #f5f6fa;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
            transition: background 0.2s;
        }
        .stButton>button:hover {
            background-color: #34507b;
            color: #fff;
        }
        .css-1d391kg {padding: 1rem; border-radius: 0.5rem; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
        .spacer {height: 2.5rem;}
        .explanation-dark {background: #23272f !important; color: #f5f6fa !important; border-left: 4px solid #2E86C1; padding: 20px; border-radius: 10px;}
        .breakdown-card {
            margin: 6px 0;
            padding: 10px 14px !important;
        }
        .breakdown-card h3 {
            font-size: 1.15rem !important;
            margin-bottom: 0.3rem !important;
        }
        .breakdown-card p {
            font-size: 0.98rem !important;
            margin: 0 0 0.3rem 0 !important;
        }
        .breakdown-card ul {
            margin: 0.2rem 0 0.2rem 1.1rem !important;
            padding: 0 !important;
        }
        .breakdown-card li {
            font-size: 0.95rem !important;
            margin-bottom: 0.15rem !important;
        }
        .block-container {padding-top: 0.5rem !important;}
        .kevin-title {
            font-family: 'Poppins', 'Montserrat', sans-serif;
            font-size: 2.4rem;
            font-weight: 700;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            letter-spacing: 0.01em;
            color: #5b8bd6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.title("Investment Profile")
        st.write("Configure your investment preferences")
        investment_amount = st.number_input("Investment Amount ($)", min_value=1000, value=10000, step=1000)
        risk_level = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"], index=1)
        time_horizon = st.slider("Investment Time Horizon (years)", min_value=1, max_value=30, value=5)
        if st.button("Generate Investment Plan"):
            st.session_state.generate = True
        else:
            st.session_state.generate = False
    
    # Main Content
    st.markdown('<h1 class="kevin-title">Kevin -- Your Personal Investment Advisor</h1>', unsafe_allow_html=True)
    if st.session_state.get('generate', False):
        portfolio = PORTFOLIO_ALLOCATIONS[risk_level]
        col1, col2 = st.columns([2, 1], gap="large")
        with col1:
            st.header("Portfolio Allocation")
            # Plotly bar chart with custom colors and horizontal labels
            asset_classes = list(portfolio.keys())
            percentages = [portfolio[a]["percentage"] for a in asset_classes]
            colors = [portfolio[a]["color"] for a in asset_classes]
            fig = go.Figure(data=[go.Bar(
                x=asset_classes,
                y=percentages,
                marker_color=colors,
                text=[f"{p}%" for p in percentages],
                textposition='outside',
            )])
            fig.update_layout(
                plot_bgcolor='#18191A',
                paper_bgcolor='#18191A',
                font_color='#f5f6fa',
                xaxis=dict(title='Asset Class', tickangle=0),
                yaxis=dict(title='Percentage', range=[0, 100]),
                margin=dict(l=20, r=20, t=20, b=20),
                height=350,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
            st.header("Investment Explanation")
            explanation = generate_investment_explanation(
                investment_amount,
                risk_level,
                time_horizon,
                portfolio
            )
            if not explanation or explanation.strip() == "":
                st.warning("No explanation was generated. Please check your OpenAI API key and network connection.")
            else:
                st.markdown(f"<div class='explanation-dark'>{explanation}</div>", unsafe_allow_html=True)
        with col2:
            st.header("Investment Breakdown")
            for asset_class, details in portfolio.items():
                percentage = details["percentage"]
                amount = investment_amount * (percentage / 100)
                st.markdown(f"""
                    <div class='breakdown-card' style='background-color: {details['color']}22; border-radius: 10px;'>
                        <h3 style='color: {details['color']};'>{asset_class}</h3>
                        <p>${amount:,.2f} ({percentage}%)</p>
                        <p><strong>Recommended:</strong></p>
                        <ul>
                """, unsafe_allow_html=True)
                for rec in details["recommendations"]:
                    if rec["ticker"] != "N/A":
                        st.markdown(f"<li>{rec['name']} ({rec['ticker']})</li>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<li>{rec['name']}</li>", unsafe_allow_html=True)
                st.markdown("</ul></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 