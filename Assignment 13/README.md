# 🛒 Price Tracker Demo (Tkinter + BeautifulSoup + Requests)

A simple **Price Tracking desktop application** built with **Python, Tkinter, Requests, and BeautifulSoup**.
This demo allows users to scrape product **titles and prices** from websites, display results in a table, and export data in **CSV** or **JSON** format.

---

## 🚀 Features

* ✅ **User-friendly GUI** built with Tkinter.
* ✅ **Enter multiple URLs** (comma-separated) for scraping.
* ✅ **Custom CSS selectors** for product titles and prices.
* ✅ **Displays results in a table** (URL, Title, Price).
* ✅ **Export results** to **CSV** and **JSON**.
* ✅ **Clear table** to reset data.

---

## 📦 Requirements

Make sure you have **Python 3.8+** installed.
Install dependencies with:

```bash
pip install requests beautifulsoup4
```

---

## ▶️ How to Run

1. Clone or download this repository.
2. Run the script:

```bash
python main.py
```

3. The app window will open.

---

## 📝 Usage Example

### Test URL

You can use the [Web Scraper test site](https://webscraper.io/test-sites/e-commerce/allinone).

* **URL:**

  ```
  https://webscraper.io/test-sites/e-commerce/allinone
  ```
* **Title Selector:**

  ```
  h4 > a.title
  ```
* **Price Selector:**

  ```
  h4.price
  ```

### Steps

1. Paste the URL(s) into the `URLs` field.
   Example:

   ```
   https://webscraper.io/test-sites/e-commerce/allinone
   ```
2. Enter the CSS selectors for title and price.
3. Click **Scrape**.
4. Data will appear in the table.
5. Click **Export CSV** or **Export JSON** to save results.

---

## 📂 Output Examples

### CSV Output

```csv
url,title,price
https://webscraper.io/test-sites/e-commerce/allinone, Asus Laptop, $499.00
https://webscraper.io/test-sites/e-commerce/allinone, Lenovo Laptop, $599.00
```

### JSON Output

```json
[
  {
    "url": "https://webscraper.io/test-sites/e-commerce/allinone",
    "title": "Asus Laptop",
    "price": "$499.00"
  },
  {
    "url": "https://webscraper.io/test-sites/e-commerce/allinone",
    "title": "Lenovo Laptop",
    "price": "$599.00"
  }
]
```

---

## 🛠️ Tech Stack

* **Python 3**
* **Tkinter** – GUI
* **Requests** – Fetch HTML content
* **BeautifulSoup4** – Parse HTML

---

## 📌 Notes

* This is a **demo project** and may not work on all e-commerce websites due to **dynamic content (JavaScript)** or **anti-scraping protections**.
* For production use, consider using tools like **Selenium** or **Playwright**.

---

## 📜 License

This project is open-source under the **MIT License**.

