# Portfolio Analyzer
This is a Streamlit-based web application that allows users to input their stock portfolio and receive a comprehensive analysis, including standard and creative metrics. Designed for beginner to intermediate investors, it provides insights into performance, risk, diversification, and future-oriented trends.
### Features

Portfolio Input: Users can enter stock symbols (e.g., AAPL) and quantities.
Standard Metrics:
Total portfolio value, annualized returns, risk (volatility), Sharpe Ratio, Beta, Alpha, Value at Risk (VaR), and Maximum Drawdown.
Fundamental metrics: P/E, ROE, Dividend Yield.
Stock correlation and sector allocation analysis.


Creative Metrics:
Innovation Score: Evaluates the innovation potential of companies (based on a sample list).
Social Sentiment Analysis: Assesses sentiment from news (currently using sample data).
Monte Carlo Simulation: Forecasts future portfolio value.
Secular Trends Factor: Measures exposure to future trends like AI and green energy.
Industry Disruption Index (HHI): Assesses diversification in disruptive industries.
AI Optimization Score: Evaluates portfolio synergy based on low correlation.


Visualizations: Interactive charts (e.g., pie chart for allocation, histogram for forecasts) using Plotly.
Language: Primarily in Persian with clear messages, but easily adaptable to English.

Prerequisites

Python 3.8 or higher
Required libraries:pip install streamlit yfinance pandas numpy plotly vaderSentiment



Installation and Setup

Clone the repository or download the app.py file:git clone <repository-url>
cd portfolio-analyzer


Install dependencies:pip install -r requirements.txt


Run the application:streamlit run app.py


A browser will open automatically (localhost:8501). Enter stock symbols (e.g., AAPL, GOOG) and quantities to view the analysis.

Project Structure

app.py: Main Streamlit application file.
requirements.txt: List of required libraries (optional, for automated installation).

Usage

In the "Portfolio Input" section, select the number of different stocks (up to 10).
Enter the stock symbol and quantity for each stock.
Click the "Analyze Portfolio" button.
Results are displayed with tables, charts, and textual evaluations.

Limitations

Data API: Uses yfinance, which is free but may slow down with high traffic. For real-time data, consider APIs like Alpha Vantage or NewsAPI.
Iranian Stocks: Currently supports only international stocks. For Tehran Stock Exchange, APIs like TseTmc or Farabixo are needed.
Sentiment Analysis: Uses sample news data. Real-time sentiment requires an API like NewsAPI (free up to 100 requests/day).

Improvement Suggestions

SEO and Monetization: Add Google AdSense or affiliate links (e.g., brokerage platforms) for revenue.
Iranian Market Support: Integrate Iranian APIs (e.g., TseTmc) for local stock analysis.
Customization: Add filters for metrics (e.g., show only risk metrics).
Security: For public hosting, use HTTPS and a login system (e.g., Firebase).
UI Enhancements: Add Persian fonts (e.g., Vazir) and full RTL support via CSS.

Hosting

Use Streamlit Cloud (free for small projects) or Heroku for online deployment.
Purchase a custom domain (e.g., portfolioanalyzer.ir) from Namecheap and connect it.

Developers
Developed by Grok (xAI) for beginner to intermediate investors. Contact us for questions or contributions.
License
MIT License - Free to use and modify with attribution.
