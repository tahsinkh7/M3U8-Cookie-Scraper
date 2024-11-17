import re
import time
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def copy_to_clipboard(data):
    root = tk.Tk()
    root.withdraw()  
    root.clipboard_clear()
    root.clipboard_append(data)
    root.update()
    root.destroy()
    print(f"Copied to clipboard:\n{data}")



options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")  


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = "https://toffeelive.com/en/live"  
driver.get(url)


time.sleep(10)


page_source = driver.page_source


m3u8_urls = list(
    set(
        url for url in re.findall(r'https://[^"]+\.m3u8', page_source)
        if "bldcmprod-cdn.toffeelive.com" in url
    )
)


cookie_match = re.search(r'Edge-Cache-Cookie=([^;\\]+)', page_source)
edge_cache_cookie = f"Edge-Cache-Cookie={cookie_match.group(1)}" if cookie_match else "Edge-Cache-Cookie=Not Available"


driver.quit()



root = tk.Tk()
root.title("M3U8 and Cookie Copier")
root.geometry("700x400")  
root.configure(bg="#303033") 


frame = ttk.Frame(root)
canvas = tk.Canvas(frame, bg="#303033")
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

frame.pack(fill="both", expand=True)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")



if m3u8_urls:
    for i, m3u8_url in enumerate(m3u8_urls):
        
        m3u8_label = tk.Label(scrollable_frame, text=f"M3U8: {m3u8_url}", fg="white", bg="#303033", anchor="w", wraplength=650)
        m3u8_label.grid(row=i * 2, column=0, sticky="w", padx=10, pady=5)

       
        cookie_label = tk.Label(scrollable_frame, text=f"Cookie: {edge_cache_cookie}", fg="white", bg="#303033", anchor="w", wraplength=650)
        cookie_label.grid(row=i * 2 + 1, column=0, sticky="w", padx=10, pady=5)

        
        copy_m3u8_button = tk.Button(
            scrollable_frame,
            text="Copy M3U8",
            command=lambda url=m3u8_url: copy_to_clipboard(url),
            bg="#505055",
            fg="white"
        )
        copy_m3u8_button.grid(row=i * 2, column=1, padx=10, pady=5)

        
        copy_cookie_button = tk.Button(
            scrollable_frame,
            text="Copy Cookie",
            command=lambda cookie=edge_cache_cookie: copy_to_clipboard(cookie),
            bg="#505055",
            fg="white"
        )
        copy_cookie_button.grid(row=i * 2 + 1, column=1, padx=10, pady=5)
else:
    no_data_label = tk.Label(scrollable_frame, text="No M3U8 URLs found from the specified domain.", fg="white", bg="#303033")
    no_data_label.pack(pady=20)


root.mainloop()

