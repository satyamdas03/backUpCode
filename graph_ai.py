from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk import sent_tokenize
import re

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sid = SentimentIntensityAnalyzer()

# Initialize global variables
data = {}

# Function to parse the input text and extract financial metrics
def parse_input(text, graph_type):
    if graph_type == "Sentiment Line Chart":
        parse_news_input(text, graph_type)
    else:
        parse_financial_metrics(text, graph_type)

def parse_news_input(text, graph_type):
    sentiment_scores = []
    sentences = sent_tokenize(text)
    
    for sentence in sentences:
        sentiment = sid.polarity_scores(sentence)
        sentiment_scores.append(sentiment['compound'])  # Use compound score for overall sentiment
    
    overall_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0  # Calculate average sentiment
    recommendation, reason = generate_recommendation(overall_sentiment)  # Generate recommendation and reason
    
    if graph_type == "Sentiment Line Chart":
        create_sentiment_line_chart(sentiment_scores, overall_sentiment)

    # Return both the recommendation and reason if they exist
    if recommendation and reason:
        return recommendation, reason
    else:
        return None  # Return None if no recommendation is generated
    


def generate_recommendation(overall_sentiment):
    if overall_sentiment > 0.2:
        recommendation = "BUY"
        reason = "The overall sentiment is positive, suggesting optimism in the market. Consider buying the stock due to favorable conditions such as strong financial performance, positive news, and a bullish trend in sentiment."
    elif overall_sentiment < -0.2:
        recommendation = "DON'T BUY"
        reason = "The overall sentiment is negative, indicating caution. It may be advisable to refrain from buying due to negative news, poor financial performance, or bearish sentiment in the market."
    else:
        recommendation = "HOLD"
        reason = "The sentiment is neutral, indicating uncertainty. Holding the stock is recommended until clearer trends emerge or further analysis is conducted."
    
    return recommendation, reason

def parse_financial_metrics(text, graph_type):
    global data
    data.clear()  # Clear previous data
    
    # Define metrics we want to extract
    metrics = {
        "Price-to-Earnings (P/E) Ratio": None,
        "Debt Ratio": None,
        "Book Value per Share": None,
        "Earnings Per Share (EPS)": None,
        "Current Ratio": None,
        "Return on Equity (ROE)": None,
        "P/E Growth (PEG) Ratio": None,
        "Lost Sales Ratio": None,
        "Dividend Yield": None,
        "Free Cash Flow": None,
        "Gross Margin": None,
        "Operating Margin": None,
        "Net Profit Margin": None,
        "Quick Ratio": None,
        "Revenue": None,
        "CAGR (Compound Annual Growth Rate)": None,
        "Capital Ratios": None,
        "Cash Ratio": None,
        "Inventory Turnover": None,
        "Liquidity Ratio": None,
        "Rate of Return": None,
        "Revenue Per Employee": None,
        "The Bottom Line": None
    }
    
    sentences = sent_tokenize(text)
    
    # Extract metrics from the text
    for sentence in sentences:
        # Price-to-Earnings Ratio (P/E Ratio)
        if "P/E ratio" in sentence or "Price-to-Earnings" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Price-to-Earnings (P/E) Ratio"] = float(match.group())
        
        # Debt Ratio
        if "Debt ratio" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Debt Ratio"] = float(match.group())
        
        # Book Value per Share
        if "Book value per share" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Book Value per Share"] = float(match.group())
        
        # Earnings Per Share (EPS)
        if "EPS" in sentence or "Earnings per share" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Earnings Per Share (EPS)"] = float(match.group())
        
        # Current Ratio
        if "Current ratio" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Current Ratio"] = float(match.group())
        
        # Return on Equity (ROE)
        if "Return on equity" in sentence or "ROE" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Return on Equity (ROE)"] = float(match.group())
        
        # P/E Growth (PEG) Ratio
        if "PEG ratio" in sentence or "P/E Growth" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["P/E Growth (PEG) Ratio"] = float(match.group())
        
        # Lost Sales Ratio
        if "Lost sales ratio" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Lost Sales Ratio"] = float(match.group())
        
        # Dividend Yield
        if "Dividend yield" in sentence:
            match = re.search(r"\b\d+(\.\d+)?%", sentence)
            if match:
                metrics["Dividend Yield"] = float(match.group().replace('%', ''))
        
        # Free Cash Flow
        if "Free cash flow" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Free Cash Flow"] = float(match.group())
        
        # Gross Margin
        if "Gross margin" in sentence:
            match = re.search(r"\b\d+(\.\d+)?%", sentence)
            if match:
                metrics["Gross Margin"] = float(match.group().replace('%', ''))
        
        # Operating Margin
        if "Operating margin" in sentence:
            match = re.search(r"\b\d+(\.\d+)?%", sentence)
            if match:
                metrics["Operating Margin"] = float(match.group().replace('%', ''))
        
        # Net Profit Margin
        if "Net profit" in sentence or "Net profit margin" in sentence:
            match = re.search(r"\b\d+(\.\d+)?%", sentence)
            if match:
                metrics["Net Profit Margin"] = float(match.group().replace('%', ''))
        
        # Quick Ratio
        if "Quick ratio" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Quick Ratio"] = float(match.group())
        
        # Revenue
        if "Revenue" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Revenue"] = float(match.group())
        
        # CAGR (Compound Annual Growth Rate)
        if "CAGR" in sentence:
            match = re.search(r"\b\d+(\.\d+)?%", sentence)
            if match:
                metrics["CAGR (Compound Annual Growth Rate)"] = float(match.group().replace('%', ''))
        
        # Capital Ratios
        if "Capital ratio" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Capital Ratios"] = float(match.group())
        
        # Cash Ratio
        if "Cash ratio" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Cash Ratio"] = float(match.group())
        
        # Inventory Turnover
        if "Inventory turnover" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Inventory Turnover"] = float(match.group())
        
        # Liquidity Ratio
        if "Liquidity" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Liquidity Ratio"] = float(match.group())
        
        # Rate of Return
        if "Rate of return" in sentence:
            match = re.search(r"\b\d+(\.\d+)?%", sentence)
            if match:
                metrics["Rate of Return"] = float(match.group().replace('%', ''))
        
        # Revenue Per Employee
        if "Revenue per employee" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["Revenue Per Employee"] = float(match.group())
        
        # The Bottom Line
        if "The bottom line" in sentence:
            match = re.search(r"\b\d+(\.\d+)?", sentence)
            if match:
                metrics["The Bottom Line"] = float(match.group())

    data = {key: value for key, value in metrics.items() if value is not None}
    
    # Determine recommendation based on financial metrics
    if data:  # Check if any metrics are present
        # You can set a threshold or some condition to make a recommendation
        if (metrics["Earnings Per Share (EPS)"] and metrics["Earnings Per Share (EPS)"] > 1.0 and 
            metrics["Return on Equity (ROE)"] and metrics["Return on Equity (ROE)"] > 15):
            recommendation = "Buy"
            reason = "Strong EPS and ROE indicate good performance."
        elif metrics["Debt Ratio"] and metrics["Debt Ratio"] > 0.5:
            recommendation = "Sell"
            reason = "High Debt Ratio indicates financial risk."
        else:
            recommendation = "Hold"
            reason = "Stable financial metrics over the last quarter."
        
        # Generate the appropriate chart based on user selection
        if graph_type == "Bar Chart":
            create_bar_chart()
        elif graph_type == "Pie Chart":
            create_pie_chart()
        elif graph_type == "Histogram":
            create_histogram()
        
        return recommendation, reason  # Return recommendation and reason
    else:
        # If no data was extracted, return None
        return None

# Function to create and display a bar chart
def create_bar_chart():
    global data
    if not data:
        return
    
    plt.clf()
    
    categories = list(data.keys())
    values = list(data.values())
    
    sns.barplot(x=categories, y=values)
    plt.title('Financial Metrics - Bar Chart')
    plt.ylabel('Value')
    plt.xticks(rotation=45, ha='right')
    
    plt.show()

# Function to create and display a pie chart
def create_pie_chart():
    global data
    if not data:
        return
    
    plt.clf()
    
    categories = list(data.keys())
    values = list(data.values())
    
    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Financial Metrics - Pie Chart')
    
    plt.show()

# Function to create and display a histogram
def create_histogram():
    global data
    if not data:
        return
    
    plt.clf()
    
    values = list(data.values())
    
    plt.hist(values, bins=10, alpha=0.75)
    plt.title('Financial Metrics - Histogram')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    
    plt.show()

def create_sentiment_line_chart(sentiment_scores, overall_sentiment):
    # Plot sentiment scores
    plt.figure(figsize=(10, 6))
    plt.plot(sentiment_scores, marker='o', linestyle='-', color='b')
    plt.title('Sentiment Analysis Over Time')
    plt.xlabel('Sentence Number')
    plt.ylabel('Sentiment Score')
    plt.axhline(0, color='gray', linewidth=0.8)  # Neutral line

    # Display recommendation
    if overall_sentiment > 0.05:
        recommendation = "BUY"
        plt.text(0.5, max(sentiment_scores), recommendation, color='green', fontsize=15, ha='center', fontweight='bold')
    elif overall_sentiment < -0.05:
        recommendation = "DON'T BUY"
        plt.text(0.5, max(sentiment_scores), recommendation, color='red', fontsize=15, ha='center', fontweight='bold')
    else:
        recommendation = "HOLD/RE-EVALUATE"
        plt.text(0.5, max(sentiment_scores), recommendation, color='orange', fontsize=15, ha='center', fontweight='bold')

    # Show the plot
    plt.show()









