# heritage_search
The project provides a convinient webscraper and parser to search a specific person in archieves. It can 
be useful, if you research your heritage and want to find any information about your relatives, but 
instead of a manual search, you can use this project.


### How to use it

1. When you run the main.py, a user interface window made with "tkinter" library opens. It You can use 
the 'default search' or you can use the 'advanced search' ("Розширений пошук"), where you select a 
parameter you want to fill. Its not necessary to fill all the parameters but it provides more accurate 
search.

2. Next you press on the button "Пошук" (Search). It shows your input quote. You should close this 
window and the program starts to search data across different websites and webarchieves which are 
available in the list 'available_sies.txt'

3. After some time, it stores results of the search in a CSV format. The files are stored in the 
'results' directory as result_0.csv, result_1.csv, ..., result_n.csv.

### The main principle of work

There are webarchieves in the Internet with different information (ww2 soldiers, repressed persons,
KIA persons etc). The main problem of these resources is the time required to search the data on the 1st 
website, then switching to the 2nd website and the search there,then switching to the 2rd website and 
the search there. And so on. The advantage of the program is to speed up your efforts utilizing 
automatical search across popular webarchieves which are provided in the list: 'available_sites.txt'. 
You fill a form only once and then you get results from all the sites. Its really convinient.
The program uses a basic OOP archiecture of adapters.

All the sites have a different page of search with many parameters. So a pipeline of the program looks in the 
following way:

python3 main.py -> user interface, where you fill parameters of search -> query preprocessing -> site parser (uses 
adapter for the particular site) -> website\webarchieve page -> data -> data filtering -> storing in the 'results' directory in the csv format

here is an example of the search window:

![alt text]('image_for_readme.png')







