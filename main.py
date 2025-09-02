import tkinter as tk
import csv
from query_preprocessor import InputQuery
from search_kernel import SearchKernel
from entry_window import EntryWindow
import os
# from adapters import base_adapter, martyrology,

if __name__ == '__main__':
    tks = tk.Tk()
    s = EntryWindow(tks)
    tks.mainloop()
    res = s.query
    print(res)

    query = InputQuery.preprocess_query(res)
    print(query)
    sites = InputQuery.preprocess_sites('available_sites.txt')
    # sites = InputQuery.preprocess_sites('heritage_websearch/available_sites.txt')
 
    searcher = SearchKernel()
    result = searcher.search_all(query, sites)

    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)

        # Отримуємо унікальні заголовки з усіх словників у блоці
    for i, block in enumerate(result):
        if not block or not isinstance(block, list):
            continue  # Пропускаємо порожні або некоректні блоки

        # Беремо ключі тільки з першого словника — порядок збережеться
        headers = list(block[0].keys())

        filename = os.path.join(results_dir, f"result_{i}.csv")
        
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for entry in block:
                writer.writerow(entry)

        print(f"Збережено у {filename}")

    # print(result)

# не зберігай парам чойс