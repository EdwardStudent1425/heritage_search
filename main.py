import tkinter as tk
from query_preprocessor import InputQuery
from search_kernel import SearchKernel
from entry_window import EntryWindow
# from adapters import base_adapter, martyrology,

if __name__ == '__main__':
    tks = tk.Tk()
    s = EntryWindow(tks)
    tks.mainloop()
    res = s.query
    print(res)

    query = InputQuery.preprocess_query(res)
    # print(query)
    # sites = InputQuery.preprocess_sites('available_sites.txt')
    sites = InputQuery.preprocess_sites('heritage_websearch/available_sites.txt')

    searcher = SearchKernel()
    result = searcher.search_all(query, sites)

    print(result)

