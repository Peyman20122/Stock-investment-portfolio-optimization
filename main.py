import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.title("تحلیل‌گر پرتفولیو سرمایه‌گذاری پیشرفته")


st.write("سهام‌های خود را وارد کنید تا تحلیل پرتفولیو را ببینید، شامل معیارهای استاندارد و خلاقانه.")

st.subheader("ورود پرتفولیو")
with st.form("portfolio_form"):

    num_stocks = st.number_input("تعداد سهام مختلف:", min_value=1, max_value=10, value=1)

    stocks = []
    quantities = []

    for i in range(int(num_stocks)):
        cols = st.columns(2)
        with cols[0]:
            stock = st.text_input(f"نماد سهام {i + 1} (مثل AAPL):", key=f"stock_{i}")
        with cols[1]:
            quantity = st.number_input(f"تعداد سهام {i + 1}:", min_value=1, value=1, key=f"quantity_{i}")
        stocks.append(stock.upper())
        quantities.append(quantity)

    submitted = st.form_submit_button("تحلیل پرتفولیو")

if submitted:

    if not all(stocks):
        st.error("لطفاً همه نمادهای سهام را وارد کنید.")
    else:
        try:

            portfolio_data = {}
            total_value = 0
            for stock, qty in zip(stocks, quantities):
                ticker = yf.Ticker(stock)
                price = ticker.history(period="1d")["Close"].iloc[-1]
                portfolio_data[stock] = {"quantity": qty, "price": price, "value": price * qty}
                total_value += price * qty


            df = pd.DataFrame(portfolio_data).T


            historical_data = yf.download(stocks, period="1y")["Close"]

            returns = historical_data.pct_change().mean() * 252
            risk = historical_data.pct_change().std() * np.sqrt(252)
            sharpe_ratio = returns / risk

            st.subheader("نتایج تحلیل استاندارد")
            st.write(f"**ارزش کل پرتفولیو:** ${total_value:.2f}")

            st.write("**جزئیات پرتفولیو:**")
            st.dataframe(df[["quantity", "price", "value"]].rename(
                columns={"quantity": "تعداد", "price": "قیمت فعلی", "value": "ارزش"}))

            fig = px.pie(values=df["value"], names=df.index, title="توزیع پرتفولیو")
            st.plotly_chart(fig)

            st.write("**تحلیل بازده و ریسک:**")
            for stock in stocks:
                st.write(
                    f"{stock}: بازده سالانه = {returns[stock]:.2%}, ریسک = {risk[stock]:.2%}, نسبت شارپ = {sharpe_ratio[stock]:.2f}")

            avg_sharpe = sharpe_ratio.mean()
            if avg_sharpe > 1:
                st.success("پرتفولیو شما خوب است! نسبت شارپ بالاست.")
            elif avg_sharpe > 0.5:
                st.warning("پرتفولیو متوسط است. می‌توانید تنوع را بیشتر کنید.")
            else:
                st.error("پرتفولیو ریسک بالایی دارد یا بازده کمی دارد.")

            market_data = yf.download('^GSPC', period="1y")['Close'].pct_change()

            betas = {}
            for stock in stocks:
                stock_returns = historical_data[stock].pct_change()
                cov = stock_returns.cov(market_data)
                var = market_data.var()
                betas[stock] = cov / var

            st.subheader("بتا سهام‌ها")
            st.write(pd.Series(betas))

            portfolio_returns = (historical_data.pct_change() * df['value'] / total_value).sum(
                axis=1)
            var_95 = np.percentile(portfolio_returns.dropna(), 5) * -1  # VaR 95%
            st.write(f"Value at Risk (95%): {var_95:.2%} (حداکثر ضرر احتمالی)")

            cumulative = (1 + portfolio_returns).cumprod()
            peak = cumulative.cummax()
            drawdown = (cumulative - peak) / peak
            max_drawdown = drawdown.min()
            st.write(f"حداکثر Drawdown: {max_drawdown:.2%}")

            avg_beta = sum(betas.values()) / len(betas)
            if avg_beta > 1.5:
                st.warning("پرتفولیو ریسک‌پذیر است (بتا بالا).")

            risk_free_rate = 0.04  # نرخ بدون ریسک
            market_return = market_data.mean() * 252
            alphas = {}
            for stock in stocks:
                stock_return = returns[stock]
                beta = betas[stock]
                expected = risk_free_rate + beta * (market_return - risk_free_rate)
                alphas[stock] = stock_return - expected

            st.subheader("آلفا سهام‌ها")
            st.write(pd.Series(alphas))

            portfolio_return = portfolio_returns.mean() * 252
            st.write(f"بازده پرتفولیو: {portfolio_return:.2%}")
            st.write(f"بازده بازار (S&P 500): {market_return:.2%}")
            if portfolio_return > market_return:
                st.success("پرتفولیو بهتر از بازار عمل کرده!")

            fundamentals = {}
            for stock in stocks:
                info = yf.Ticker(stock).info
                fundamentals[stock] = {
                    'P/E': info.get('trailingPE', 'نامشخص'),
                    'ROE': info.get('returnOnEquity', 'نامشخص'),
                    'Dividend Yield': info.get('dividendYield', 'نامشخص')
                }

            st.subheader("معیارهای بنیادی")
            st.dataframe(pd.DataFrame(fundamentals).T)

            pe_values = [v['P/E'] for v in fundamentals.values() if v['P/E'] != 'نامشخص']
            if pe_values and sum(pe_values) / len(pe_values) > 25:
                st.warning("سهام‌ها ممکن است overvalued باشند (P/E بالا).")

            correlation = historical_data.pct_change().corr()
            st.subheader("همبستگی سهام‌ها")
            st.dataframe(correlation)

            sectors = {stock: yf.Ticker(stock).info.get('sector', 'نامشخص') for stock in stocks}
            sector_df = pd.DataFrame(sectors.items(), columns=['سهام', 'بخش'])
            st.subheader("تخصیص به بخش‌ها")
            st.dataframe(sector_df.groupby('بخش').size().reset_index(name='تعداد سهام'))

            avg_corr = correlation.mean().mean()
            if avg_corr > 0.7:
                st.warning("تنوع کم است! همبستگی سهام‌ها بالاست.")


            st.subheader("معیارهای خلاقانه تحلیل پرتفولیو")

            innovative_companies = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']
            innovation_scores = {stock: 10 if stock in innovative_companies else 5 for stock in stocks}

            avg_innovation = sum(innovation_scores.values()) / len(stocks)
            st.write(f"میانگین امتیاز نوآوری: {avg_innovation:.2f}/10")
            if avg_innovation > 7:
                st.success("پرتفولیو نوآورانه است و پتانسیل رشد بلندمدت داره!")

            analyzer = SentimentIntensityAnalyzer()
            sample_news = {
                'AAPL': 'Apple launches new innovative product! Investors are excited.',
                'GOOG': 'Google faces antitrust issues, stock might drop.',
                'TSLA': 'Tesla reports record sales.'
            }
            sentiments = {stock: analyzer.polarity_scores(sample_news.get(stock, 'No news available.'))['compound'] for
                          stock in stocks}

            avg_sentiment = sum(sentiments.values()) / len(stocks)
            st.write(f"میانگین احساسات اجتماعی: {avg_sentiment:.2f} (از -1 منفی تا +1 مثبت)")
            if avg_sentiment < 0:
                st.warning("احساسات منفی غالبه؛ ریسک اخبار بد وجود داره.")

            num_simulations = 1000
            simulation_periods = 252
            returns_mean = returns.mean()
            returns_std = risk.mean()
            simulations = np.random.normal(returns_mean, returns_std, (simulation_periods, num_simulations))
            final_values = np.prod(1 + simulations, axis=0) * total_value

            avg_final = np.mean(final_values)
            st.write(f"ارزش پیش‌بینی‌شده پس از یک سال: ${avg_final:.2f}")
            st.write(f"ریسک ۹۵٪: ارزش ممکنه تا ${np.percentile(final_values, 5):.2f} برسه.")
            fig_mc = px.histogram(final_values, title="توزیع ارزش آینده")
            st.plotly_chart(fig_mc)

            trends = {'AAPL': 'Technology', 'GOOG': 'AI', 'TSLA': 'Green Energy', 'MSFT': 'Cloud',
                      'AMZN': 'E-commerce'}  # دسته‌بندی نمونه
            trend_coverage = len(set([trends.get(stock, 'Unknown') for stock in stocks])) / len(stocks) if stocks else 0

            st.write(f"پوشش روندها: {trend_coverage:.2%} (چقدر پرتفولیو متنوع در ترندهای آینده‌ست)")
            if trend_coverage > 0.5:
                st.success("پرتفولیو به روندهای آینده مثل AI و انرژی سبز وصله!")

            sector_counts = pd.Series(sectors.values()).value_counts()
            hhi = sum((sector_counts / len(stocks)) ** 2) * 10000  # HHI formula

            st.write(f"HHI: {hhi:.2f} (کمتر از ۱۵۰۰ یعنی تنوع disruptive بالا)")
            if hhi < 1500:
                st.success("پرتفولیو disruptive و متنوع در صنایع مختله!")

            synergy_score = 1 - correlation.mean().mean()

            st.write(f"سینرژی پرتفولیو: {synergy_score:.2f}")
            st.write("پیشنهاد: اگر سینرژی کمه، سهام‌هایی مثل NVDA برای AI اضافه کن.")
            if synergy_score > 0.5:
                st.success("سینرژی بالا؛ پرتفولیو بهینه‌سازی‌شده با AI-like approach.")

        except Exception as e:
            st.error(f"خطا در تحلیل: {str(e)}. مطمئن شوید نمادهای سهام درست هستند.")
