import customtkinter as ctk
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import time
from crewai import Crew
from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks
from dotenv import load_dotenv
from graph_ai import parse_input  # Import the parse_input function from graph_ai.py
import tkinter.messagebox as messagebox  # Import messagebox from tkinter

load_dotenv()

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
        return final_summary

class FinancialAnalysisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Financial Analysis Terminal")
        self.geometry("530x500")
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

        # Real-Time Stock Price Button
        self.stock_price_button = ctk.CTkButton(self.main_frame, text="Show Real-Time Stock Prices", command=self.show_realtime_prices, width=200, font=("Arial", 14, "bold"))
        self.stock_price_button.grid(row=8, column=0, columnspan=2, pady=(25, 0))

        # Canvas for displaying the graph
        self.graph_canvas = None
        self.plot_thread = None
        self.fetcher = RealTimeStockPriceFetcher()  # Initialize the RealTimeStockPriceFetcher class

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
        summary = FinancialCrew(company_name).run()
        self.analysis_text.insert(ctk.END, f"{summary}\n")

    def generate_graph(self):
        user_input = self.graph_input_text.get("1.0", ctk.END).strip()
        graph_type = self.graph_type_var.get()  # Get selected graph type
        if user_input:
            # Call the parse_input function and capture any recommendation output
            recommendation = parse_input(user_input, graph_type)  # Assume parse_input returns recommendation text
            self.display_graph(recommendation)
        else:
            messagebox.showwarning("Input Error", "Please enter financial metrics.")

    def display_graph(self, recommendation=None):
        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()  # Remove previous canvas if it exists

        fig = plt.gcf()  # Get the current figure from matplotlib

        # Create a new window for the graph
        graph_window = ctk.CTkToplevel(self)
        graph_window.title("Financial Graph")
        graph_window.resizable(False, False)

        self.graph_canvas = FigureCanvasTkAgg(fig, master=graph_window)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack()

        if recommendation:
            messagebox.showinfo("Recommendation", recommendation)  # Display the recommendation as a messagebox

    def show_realtime_prices(self):
        company_name = self.company_entry.get().strip()
        if not company_name:
            messagebox.showwarning("Input Error", "Please enter a company name.")
            return

        if self.plot_thread and self.plot_thread.is_alive():
            messagebox.showwarning("Error", "Real-time price fetching is already running.")
            return
        
        # Start real-time plotting in a separate thread
        self.plot_thread = threading.Thread(target=self.fetcher.fetch_realtime_prices, args=(company_name,))
        self.plot_thread.start()

    def stop_realtime_prices(self):
        if self.plot_thread and self.plot_thread.is_alive():
            self.fetcher.stop()
            self.plot_thread.join()

    def on_closing(self):
        self.stop_realtime_prices()
        self.destroy()

class RealTimeStockPriceFetcher:
    def __init__(self):
        self.running = False

    def fetch_realtime_prices(self, company_name):
        ticker = yf.Ticker(company_name)
        try:
            plt.ion()  # Turn on interactive mode
            fig, ax = plt.subplots()  # Create a figure and an axis for the plot
            
            self.running = True
            while self.running:
                # Fetch 1-minute interval data for the last 7 days
                data = ticker.history(period='7d', interval='1m')
                
                # Check if data is empty
                if data.empty:
                    print(f"No price data found for {company_name}, please check the ticker symbol.")
                    break

                # Extract the closing prices
                prices = data['Close']

                # Update the plot
                ax.clear()  # Clear the previous data
                ax.plot(prices.index, prices.values)  # Plot the new data
                ax.set_title(f"Real-Time Price for {company_name}")
                ax.set_xlabel("Time")
                ax.set_ylabel("Price (USD)")
                plt.draw()  # Update the plot
                plt.pause(60)  # Pause for 60 seconds before updating again

        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            plt.ioff()  # Turn off interactive mode after plotting is finished
            plt.show()  # Show the final plot

    def stop(self):
        self.running = False

if __name__ == "__main__":
    app = FinancialAnalysisApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # Handle window closing event
    app.mainloop()
