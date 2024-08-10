# Stock Analysis Project

## Overview

This project aims to develop a comprehensive stock analysis report that includes trend analysis, predictions, and investment recommendations.

## Setting Up the Environment

### Step 1: Setting Up `pyproject.toml`

The `pyproject.toml` file turns all the requirements of our project into code, so we can run an install script to package and build all the necessary dependencies.

1. **Install Poetry**:
    ```sh
    pipx install poetry
    ```

2. **Install pipx**:
    ```sh
    py -m pip install --user pipx
    ```

3. **Create `pyproject.toml`**:
    - Define core components under `[tool.poetry]` such as `name` and `description`.
    - Specify dependencies required for the project.
    - Use `tool.pyright` to check Python codes for type errors.
    - Use `tool.ruff` to check for errors and styling issues.
    - Define `build-system` to use Poetry version.

### Step 2: Install Dependencies

Open the terminal and run:
```sh
poetry install --no-root
```

### Step 3: Check Python Version

Check the currently used Python version for your Poetry environment:
```sh
poetry env list
```

### Step 4: Enter Poetry Environment

Enter into the Poetry environment:
```sh
poetry shell
```

After this, you will have a Python environment in which you can work.


## Cheat Sheet to Make a Good Agent

### General Guidelines:
- **Begin with the end in mind**: Identify the specific outcome your tasks are aiming to achieve.
- **Break down the outcome into actionable tasks**: Assign each task to the appropriate agent.
- **Ensure the tasks are descriptive**: Provide clear instructions and expected deliverables.

### Project Goal
Develop a comprehensive stock analysis report that includes trend analysis, predictions, and investment recommendations.

### Key Roles
**Captain/Manager/Boss**

**Role**: Expert Stock Analyst
- **Responsibilities**: Oversees the entire stock analysis project.
- **Goal**: Ensure the final report is accurate, comprehensive, and actionable.
- **Backstory**: Experienced stock analyst with a background in financial markets and data analysis.

### Employees/Experts to Hire
**Data Collection Specialist**

**Role**: Collects relevant stock data from various sources.
- **Goal**: Gather comprehensive and accurate data for analysis.
- **Backstory**: Proficient in web scraping, API usage, and data gathering techniques.

**Data Cleaning Expert**

**Role**: Cleans and preprocesses the collected data.
- **Goal**: Ensure the data is clean, consistent, and ready for analysis.
- **Backstory**: Experienced in data cleaning and preprocessing with strong attention to detail.

**Data Visualization Expert**

**Role**: Creates visual representations of the data.
- **Goal**: Develop insightful charts and graphs to visualize trends and patterns.
- **Backstory**: Skilled in data visualization tools like Matplotlib, Seaborn, and Plotly.

**Prediction Model Specialist**

**Role**: Builds and trains predictive models.
- **Goal**: Develop accurate models to predict stock trends and prices.
- **Backstory**: Proficient in machine learning and statistical modeling techniques.

**Investment Advisor**

**Role**: Provides investment recommendations based on analysis.
- **Goal**: Offer actionable investment advice to maximize returns.
- **Backstory**: Experienced financial advisor with a deep understanding of stock markets and investment strategies. 


## SOME QUERIES TO BE ANSWERED

The project is not using traditional machine learning models like ANN (Artificial Neural Networks) or CNN (Convolutional Neural Networks). Instead, it leverages pre-existing AI tools and APIs to perform various tasks such as web scraping, financial calculations, and document analysis.

### Which model would be optimal to train the model and get the output and why?

Given the nature of this project, which involves financial data analysis, market trend interpretation, and investment recommendations, a traditional machine learning model is not necessarily optimal. Instead, using pre-trained models and APIs like those provided by LangChain, SEC API, and other specific tools is more effective. These tools are designed to handle specific tasks like data scraping, document parsing, and embeddings for document similarity.
If we were to incorporate a custom model, we might consider:
**Natural Language Processing (NLP)** models for text analysis and summarization.
**Time Series Analysis models** for financial trend prediction.
**Ensemble Models** that combine multiple approaches for more robust predictions.

### this project using an LLM (Large Language Model)

The project utilizes LLMs through the LangChain library and specific tools like the **YahooFinanceNewsTool** and the custom agents defined in stock_analysis_agents.py. These tools and agents use pre-trained language models to perform tasks like **summarizing web content, searching the internet, and analyzing financial documents**.

## THE PROJECT CAN BE CHANGED TO "LLM-Powered Financial Analysis and Investment Advisor"

## SOME RESEARCH WORKS TO SUPPORT THE IDEAS OF THIS PROJECT

1. **"A Multi-agent Q-learning Framework for Optimizing Stock Trading Systems"** by Jae Won Lee and Jangmin O. This paper explores the use of a multi-agent system combined with Q-learning techniques to optimize stock trading strategies. It emphasizes the integration of reinforcement learning to enhance decision-making in trading environments, aligning well with the project on using agents for stock analysis and recommendation​.
link to the paper : [https://link.springer.com/chapter/10.1007/3-540-46146-9_16](url)

2. **"Using Multi-agent Systems Simulations for Stock Market Predictions"** by Diana Dezsi, Emil Scarlat, and Iulia Mărieş. This study presents an agent-based simulation approach for predicting stock market trends. It highlights how different agents can represent various market participants and interact to simulate realistic market conditions, which can improve the accuracy of stock market predictions and analyses​.
link to paper : [https://link.springer.com/chapter/10.1007/978-3-319-05458-2_6](url)


## Explanation of the code 

1. There are 3 agents : **Research Analyst Agent**, **Financial Analyst Agent**, **Investment Advisor Agent**, Stock Analysis Report 
    -*The Financial Analyst Agent*: To impress all customers with the financial data and market analysis.
    -*The Research Analyst Agent*: To being the best at gathering information, interpreting data and amazing the customer with it.
    -*The Investment Advisor Agent*: To Impress the customers with full analyses over stocks and complete the investment recommendations.

2. Each agent have some tools provided to work with it. These tools are being imported in the starting lines.

3. There is a folder called **Tools** thats where all the tools exist. 
    -*The Browser Tools*: will be used to scrape website content.
    -*The Calculator Tools*: will be used to make any mathematical calculations.
    -*The Search Tools*: will be used to search the internet.
    -*The Sec Tool*: will be used to search 10Q forms.
    -**YAHOO FINANCE NEWS TOOLS**: used to collect the latest finance news from the news tool.

4. Now lets summarize the tasks to be performed by the agents:
    -*The Research Task*: to collect and summarize recent news articles 
    -*The Financial Analysis*: to conduct a thorough analysis of the stock's financial health and market performance.
    -*The Filings Analysis*: to analyze the latest filings
    -*The Recommend Task*: to review and synthesize the analysis provided by the financial and research analysts

5. Finally we are going to merge all the above functions of the agents, tools and tasks to run the code and the get the final output.

## SUMMARY
The project leverages various pre-trained tools and APIs to perform its tasks, without the need for traditional machine learning models like ANN or CNN. The integration of LLMs through LangChain and specific financial analysis tools forms the core of the project's analytical capabilities.




