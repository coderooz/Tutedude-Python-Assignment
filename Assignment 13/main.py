import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests, csv, json
from bs4 import BeautifulSoup

class PriceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Price Tracker Demo")
        self.root.geometry("850x600")

        self.data = []  # Store scraped results

        # --- Input Frame ---
        input_frame = tk.LabelFrame(root, text="Scraper Settings", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="URLs (comma separated):").grid(row=0, column=0, sticky="w")
        self.url_entry = tk.Entry(input_frame, width=80)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Title Selector:").grid(row=1, column=0, sticky="w")
        self.title_entry = tk.Entry(input_frame, width=50)
        self.title_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Price Selector:").grid(row=2, column=0, sticky="w")
        self.price_entry = tk.Entry(input_frame, width=50)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        scrape_btn = tk.Button(input_frame, text="Scrape", command=self.scrape_data, bg="#4CAF50", fg="white")
        scrape_btn.grid(row=0, column=2, rowspan=2, padx=10, ipadx=10, ipady=5)

        clear_btn = tk.Button(input_frame, text="Clear", command=self.clear_data, bg="#f44336", fg="white")
        clear_btn.grid(row=2, column=2, padx=10, ipadx=10, ipady=5)

        # --- Table Frame ---
        table_frame = tk.LabelFrame(root, text="Scraped Data", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=("url", "title", "price"), show="headings")
        self.tree.heading("url", text="URL")
        self.tree.heading("title", text="Title")
        self.tree.heading("price", text="Price")
        self.tree.column("url", width=300)
        self.tree.column("title", width=200)
        self.tree.column("price", width=100)
        self.tree.pack(fill="both", expand=True)

        # --- Export Frame ---
        export_frame = tk.Frame(root)
        export_frame.pack(fill="x", padx=10, pady=5)

        export_csv_btn = tk.Button(export_frame, text="Export CSV", command=self.export_csv, bg="#2196F3", fg="white")
        export_csv_btn.pack(side="left", padx=5, ipadx=10, ipady=5)

        export_json_btn = tk.Button(export_frame, text="Export JSON", command=self.export_json, bg="#FF9800", fg="white")
        export_json_btn.pack(side="left", padx=5, ipadx=10, ipady=5)

    # --- Scraping Function ---
    def scrape_data(self):
        urls = self.url_entry.get().split(",")
        title_selector = self.title_entry.get().strip()
        price_selector = self.price_entry.get().strip()

        if not urls or not title_selector or not price_selector:
            messagebox.showerror("Error", "Please provide URLs and selectors")
            return

        for url in urls:
            url = url.strip()
            try:
                r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "html.parser")
                    title_elem = soup.select_one(title_selector)
                    price_elem = soup.select_one(price_selector)

                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    price = price_elem.get_text(strip=True) if price_elem else "N/A"

                    self.data.append({"url": url, "title": title, "price": price})
                    self.tree.insert("", "end", values=(url, title, price))
                else:
                    messagebox.showwarning("Warning", f"Failed to fetch {url} (Status {r.status_code})")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to scrape {url}\n{e}")

    # --- Clear Data ---
    def clear_data(self):
        self.tree.delete(*self.tree.get_children())
        self.data = []

    # --- Export CSV ---
    def export_csv(self):
        if not self.data:
            messagebox.showerror("Error", "No data to export")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["url", "title", "price"])
                writer.writeheader()
                writer.writerows(self.data)
            messagebox.showinfo("Success", f"Data exported to {file_path}")

    # --- Export JSON ---
    def export_json(self):
        if not self.data:
            messagebox.showerror("Error", "No data to export")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            messagebox.showinfo("Success", f"Data exported to {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PriceTrackerApp(root)
    root.mainloop()
