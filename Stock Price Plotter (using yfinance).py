import tkinter as tk
from tkinter import messagebox, filedialog
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

class StockPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📈 Stock Price Plotter with MA & Compare")
        self.root.geometry("450x350")

        tk.Label(root, text="Enter Stock Symbols (comma-separated):", font=("Arial", 11)).pack()
        self.symbol_entry = tk.Entry(root, font=("Arial", 12), width=30)
        self.symbol_entry.pack(pady=5)
        self.symbol_entry.insert(0, "AAPL, MSFT")

        tk.Label(root, text="Start Date (YYYY-MM-DD):").pack()
        self.start_entry = tk.Entry(root, font=("Arial", 12), width=20)
        self.start_entry.pack(pady=5)
        self.start_entry.insert(0, "2023-01-01")

        tk.Label(root, text="End Date (YYYY-MM-DD):").pack()
        self.end_entry = tk.Entry(root, font=("Arial", 12), width=20)
        self.end_entry.pack(pady=5)
        self.end_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        self.ma_var = tk.IntVar()
        tk.Checkbutton(root, text="📏 Show Moving Averages (20/50)", variable=self.ma_var).pack(pady=5)

        tk.Button(root, text="📊 Plot Stock Prices", font=("Arial", 12), command=self.plot_stocks).pack(pady=10)

    def plot_stocks(self):
        symbols = [s.strip().upper() for s in self.symbol_entry.get().split(",") if s.strip()]
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        show_ma = self.ma_var.get()

        if not symbols:
            messagebox.showwarning("Missing Input", "Please enter at least one stock symbol.")
            return

        plt.figure(figsize=(12, 6))

        try:
            for symbol in symbols:
                data = yf.download(symbol, start=start, end=end, auto_adjust=False)
                if data.empty:
                    messagebox.showwarning("No Data", f"No data for {symbol}")
                    continue

                col = "Adj Close" if "Adj Close" in data.columns else "Close"
                plt.plot(data[col], label=f"{symbol} {col}", linewidth=2)

                if show_ma:
                    ma20 = data[col].rolling(window=20).mean()
                    ma50 = data[col].rolling(window=50).mean()
                    plt.plot(ma20, linestyle='--', alpha=0.7, label=f"{symbol} MA20")
                    plt.plot(ma50, linestyle='--', alpha=0.7, label=f"{symbol} MA50")

            if len(plt.gca().lines) == 0:
                raise Exception("No valid data found for any stock.")

            plt.title(f"Stock Price Comparison: {', '.join(symbols)}")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()

            save = messagebox.askyesno("Save Chart", "Save the chart as PNG?")
            if save:
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
                if file_path:
                    plt.savefig(file_path)
                    messagebox.showinfo("Saved", f"Chart saved to:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch or plot data:\n{e}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    StockPlotterApp(root)
    root.mainloop()
