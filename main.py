import customtkinter as ctk
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from crewai import Crew
from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks
from dotenv import load_dotenv
from graph_ai import parse_input  # Import the parse_input function from graph_ai.py
from ib_insync import IB, Stock, MarketOrder  # Import IBKR API

load_dotenv()

# Function to connect to Interactive Brokers
def connect_to_ibkr():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)  # Ensure TWS/IB Gateway is running and configured to accept connections
    return ib

# Function to place a trade order based on analysis
def place_trade(ib, symbol, action, quantity):
    stock = Stock(symbol, 'SMART', 'USD')  # Replace with your market and currency
    ib.qualifyContracts(stock)
    order = MarketOrder(action, quantity)
    trade = ib.placeOrder(stock, order)
    print(f'Placing {action} order for {quantity} shares of {symbol}')
    return trade


class FinancialCrew:
    def __init__(self, company):
        self.company = company

    def run(self):
        agents = StockAnalysisAgents()
        tasks = StockAnalysisTasks()

        research_analyst_agent = agents.research_analyst()
        financial_analyst_agent = agents.financial_analyst()
        investment_advisor_agent = agents.investment_advisor()

        research_task = tasks.research(research_analyst_agent, self.company)
        financial_task = tasks.financial_analysis(financial_analyst_agent)
        filings_task = tasks.filings_analysis(financial_analyst_agent)
        recommend_task = tasks.recommend(investment_advisor_agent)

        crew = Crew(
            agents=[
                research_analyst_agent,
                financial_analyst_agent,
                investment_advisor_agent
            ],
            tasks=[
                research_task,
                financial_task,
                filings_task,
                recommend_task
            ],
            verbose=False  # Set verbose to False to suppress terminal output
        )

        result = crew.kickoff()
        final_summary = result.get("final_summary", "Summary not found")  # Modify the key as per your actual structure
        sentiment_score = result.get("sentiment_score", 0)  # Extract sentiment score for trading decision
        return final_summary, sentiment_score
    
    def execute_trading_strategy(self, sentiment_score):
        # Connect to IBKR
        ib = connect_to_ibkr()

        # Determine action based on sentiment score
        action = "HOLD"
        if sentiment_score > 0.3:
            action = "BUY"
        elif sentiment_score < -0.3:
            action = "SELL"

        # Execute trade if buy/sell
        if action != "HOLD":
            trade = place_trade(ib, self.company, action, quantity=100)  # Example quantity
            print(f"Trade status: {trade.orderStatus.status}")

        # Disconnect after execution
        ib.disconnect()

class FinancialAnalysisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Financial Analysis Terminal")
        self.geometry("500x400")
        self.resizable(False, False)  # Prevent window resizing

        # Set up main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Configure grid layout
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)

        # Company Name Label and Entry
        self.company_label = ctk.CTkLabel(self.main_frame, text="Company Name:", font=("Arial", 18, "bold"))
        self.company_label.grid(row=0, column=0, sticky="w")

        self.company_entry = ctk.CTkEntry(self.main_frame, width=320)
        self.company_entry.grid(row=0, column=1, sticky="e", padx=(10, 0))

        # Analyze Button
        self.analyze_button = ctk.CTkButton(self.main_frame, text="Analyze", command=self.start_analysis, width=100, font=("Arial", 14, "bold"))
        self.analyze_button.grid(row=1, column=0, columnspan=2, pady=(15, 0))

        # Analysis Result Textbox
        self.analysis_text = ctk.CTkTextbox(self.main_frame, height=15, width=400)
        self.analysis_text.grid(row=2, column=0, columnspan=2, pady=(15, 0))

        # Financial Metrics Label and Textbox
        self.graph_input_label = ctk.CTkLabel(self.main_frame, text="Financial Metrics:", font=("Arial", 18, "bold"))
        self.graph_input_label.grid(row=3, column=0, sticky="w", pady=(15, 0))

        # Instruction Label for Sentiment Line Chart
        self.sentiment_instruction_label = ctk.CTkLabel(self.main_frame, text="Choose Sentiment Line Chart to see the final answer.", font=("Arial", 12, "italic"))
        self.sentiment_instruction_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(5, 0))

        # Financial Metrics Textbox
        self.graph_input_text = ctk.CTkTextbox(self.main_frame, height=100, width=400)
        self.graph_input_text.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        # Graph Type Dropdown
        self.graph_type_var = ctk.StringVar()
        self.graph_type_var.set("Bar Chart")  # Default option
        self.graph_type_menu = ctk.CTkOptionMenu(self.main_frame, variable=self.graph_type_var, values=["Bar Chart", "Pie Chart", "Histogram", "Sentiment Line Chart"], font=("Arial", 14, "bold"))
        self.graph_type_menu.grid(row=6, column=0, columnspan=2, pady=(10, 0))

        # Generate Graph Button
        self.graph_button = ctk.CTkButton(self.main_frame, text="Generate Graph", command=self.generate_graph, width=120, font=("Arial", 14, "bold"))
        self.graph_button.grid(row=7, column=0, columnspan=2, pady=(10, 0))

        # Canvas for displaying the graph
        self.graph_canvas = None

    def start_analysis(self):
        company_name = self.company_entry.get().strip()
        if company_name:
            self.analysis_text.delete("1.0", ctk.END)
            self.analysis_text.insert(ctk.END, f"Analyzing {company_name}...\n")
            threading.Thread(target=self.run_analysis, args=(company_name,)).start()
        else:
            self.analysis_text.delete("1.0", ctk.END)
            self.analysis_text.insert(ctk.END, "Please enter a company name.")

    def run_analysis(self, company_name):
        crew = FinancialCrew(company_name)
        summary, sentiment_score = crew.run()
        self.analysis_text.insert(ctk.END, f"{summary}\n")
        self.execute_trading_strategy(sentiment_score)

    def execute_trading_strategy(self, sentiment_score):
        crew = FinancialCrew(self.company_entry.get().strip())
        trading_action = "HOLD"
        if sentiment_score > 0.3:
            trading_action = "BUY"
        elif sentiment_score < -0.3:
            trading_action = "SELL"
        
        self.trading_decision_text.delete("1.0", ctk.END)
        self.trading_decision_text.insert(ctk.END, f"Trading Decision: {trading_action}\n")

        if trading_action != "HOLD":
            crew.execute_trading_strategy(sentiment_score)
            self.trading_decision_text.insert(ctk.END, "Trade executed.\n")
        else:
            self.trading_decision_text.insert(ctk.END, "No trade executed.\n")

    

    def generate_graph(self):
        user_input = self.graph_input_text.get("1.0", ctk.END).strip()
        graph_type = self.graph_type_var.get()  # Get selected graph type
        if user_input:
            # Call the parse_input function and capture any recommendation output
            recommendation = parse_input(user_input, graph_type)  # Assume parse_input returns recommendation text
            self.display_graph(recommendation)
        else:
            ctk.messagebox.showwarning("Input Error", "Please enter financial metrics.")

    def display_graph(self, recommendation):
        # Assuming `parse_input` function generates a Matplotlib plot based on user input.
        fig = plt.figure(figsize=(6, 4))

        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()

        self.graph_canvas = FigureCanvasTkAgg(fig, self.main_frame)
        self.graph_canvas.get_tk_widget().grid(row=10, column=0, columnspan=2)
        self.graph_canvas.draw()

        if recommendation:
            self.analysis_text.insert(ctk.END, f"\n{recommendation}\n")

if __name__ == "__main__":
    app = FinancialAnalysisApp()
    app.mainloop()



