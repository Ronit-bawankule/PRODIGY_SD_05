import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def scrape_books():
    url = "http://books.toscrape.com/catalogue/page-1.html"
    products = []

    try:
        for page in range(1, 3):  # Scrape first 2 pages (you can increase this)
            response = requests.get(f"http://books.toscrape.com/catalogue/page-{page}.html")
            soup = BeautifulSoup(response.content, "html.parser")
            books = soup.find_all("article", class_="product_pod")

            for book in books:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text.strip()
                rating = book.p["class"][1]

                products.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating
                })

        df = pd.DataFrame(products)
        df.to_csv("scraped_books.csv", index=False)
        messagebox.showinfo("Success", "Data scraped and saved to 'scraped_books.csv'")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

# ------------------- GUI -------------------

app = tk.Tk()
app.title("Web Scraper - Books to Scrape")
app.geometry("400x200")

label = tk.Label(app, text="Scrape Book Info from BooksToScrape.com", font=("Arial", 14), wraplength=300)
label.pack(pady=20)

scrape_button = tk.Button(app, text="Start Scraping", command=scrape_books, bg="green", fg="white", padx=10, pady=5)
scrape_button.pack(pady=10)

app.mainloop()
