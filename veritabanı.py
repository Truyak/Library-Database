import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry


root = tk.Tk()
root.title("Book Database Application")
root.geometry('860x550+60+50')
root.config(bg='#0077b4')

opened_window = None
window_is_open = False

def is_window_open(window_type):
    return any(w.title() == window_type for w in root.winfo_children() if isinstance(w, tk.Toplevel))

def open_new_window(window_type):
    global opened_window
    # If window is not open, open the window.
    if not is_window_open(window_type):        
        # Call the function for create a window content
        create_content(window_type)

    

def create_content(window_type):
    if window_type == "Add Book":
        add_book()

    elif window_type == "All Books":
        list_books()

    elif window_type == "Update Book":
        update_book_window()

    elif window_type == "Book Detail":
        show_selected_book()
    elif window_type == "lent Books":
        list_books_lent()
    elif window_type == "Borrowed Books":
        list_books_borrowed()

def add_book():
    new_window = tk.Toplevel(root)
    new_window.title("Add Book")
    new_window.geometry('500x500+1000+30')
    new_window.config(bg='#0077b4')

    name_label = tk.Label(new_window, text="Book Name:", bg='#0077b4')
    name_label.grid(row=0, column=0, pady=10)
    
    name_entry = tk.Entry(new_window)
    name_entry.grid(row=0, column=2,ipadx=90, ipady=2, columnspan=2, padx=20, sticky="w")
    
    author_label = tk.Label(new_window, text="author:", bg='#0077b4')
    author_label.grid(row=1, column=0, pady=10)
    
    author_entry = tk.Entry(new_window)
    author_entry.grid(row=1, column=2,ipadx=90, ipady=2, columnspan=2, padx=20, sticky="w")
    
    line_label = tk.Label(new_window, text="Line Number:", bg='#0077b4')
    line_label.grid(row=2, column=0, pady=10)
    
    line_entry = tk.Entry(new_window)
    line_entry.grid(row=2, column=2,ipadx=90, ipady=2, columnspan=2, padx=20, sticky="w")
    
    shelf_label = tk.Label(new_window, text="Shelf", bg='#0077b4')
    shelf_label.grid(row=3, column=0, pady=10)
    
    shelf_entry = tk.Entry(new_window)
    shelf_entry.grid(row=3, column=2,ipadx=90, ipady=2, columnspan=2, padx=20, sticky="w")

    state_label = tk.Label(new_window, text="State:", bg='#0077b4')
    state_label.grid(row=4, column=0, pady=10)
    
    state_var = tk.StringVar()
    state_options = ["Borrowed", "On Shelf", "lent"]
    state_var.set(state_options[1])  # set the default state
    
    state_optionmenu = tk.OptionMenu(new_window, state_var, *state_options)
    state_optionmenu.config(bg='#0077b4')
    state_optionmenu.grid(row=4, column=2,ipadx=50, ipady=2, columnspan=2, padx=20, sticky="w")
    
    date_label = tk.Label(new_window, text="date:", bg='#0077b4')
    date_label.grid(row=5, column=0, pady=10)
    
    date_cal = DateEntry(
                            new_window,
                            foreground='white', borderwidth=2)
    date_cal.grid(row=5, column=1, ipadx=50, ipady=2, columnspan=3, padx=10)
    
    bor_or_lent_person_label = tk.Label(new_window, text="Borrowed or lent Person:",font=("ariel", 8), bg='#0077b4')
    bor_or_lent_person_label.grid(row=6, column=0, pady=10)
    
    bor_or_lent_person_entry = tk.Entry(new_window)
    bor_or_lent_person_entry.grid(row=6, column=1, ipadx=90, ipady=2, columnspan=2, padx=20,sticky="w")

    save_button = tk.Button(new_window, bg='#0077b4', text="save", command=lambda: save_new_book(name_entry.get(), author_entry.get(), line_entry.get(), shelf_entry.get(), state_var.get(), bor_or_lent_person_entry.get() if state_var.get() != "On shelf" else "", date_cal.get_date() if state_var.get() != "On shelf" else ""))
    save_button.grid(row=7, column=0,ipadx=210, ipady=5, columnspan=3, padx=20, sticky="w")
    
        

def save_new_book(name, author, line, shelf, state, bor_or_lent_person="", date=""):
    if name and author and line and shelf and state:
        if (state == "Borrowed" or state == "lent") and (bor_or_lent_person and date):
            add_book_to_database(name, author, line, shelf, state, bor_or_lent_person, date)
            messagebox.showinfo("Successful", "Book added!")
        elif state == "On shelf": 
            add_book_to_database(name, author, line, shelf, state)
            messagebox.showinfo("Successful", "Book added!")
        else:
            messagebox.showerror("Error!", "Fill all spaces!")
    else:
        messagebox.showerror("Error!", "Fill all spaces!")

def add_book_to_database(name, author, line, shelf, state, bor_or_lent_person = None, date = None):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    if state != "On shelf":
        if state == "Borrowed":
            cursor.execute('INSERT INTO books (name, author, line, shelf, state, lent_person, date) VALUES (?, ?, ?, ?, ?, ?, ?)', (name, author, line, shelf, state, bor_or_lent_person, date))
        else:
            cursor.execute('INSERT INTO books (name, author, line, shelf, state, date, borrowed_person) VALUES (?, ?, ?, ?, ?, ?, ?)', (name, author, line, shelf, state, date, bor_or_lent_person))
    else:
        cursor.execute('INSERT INTO books (name, author, line, shelf, state) VALUES (?, ?, ?, ?, ?)', (name, author, line, shelf, state))
    
    connection.commit()
    connection.close()

def search_book(event=None):
    search_text = search_entry.get()

    if search_text:        
        books = search_book_on_database(search_text)
        if books:
            book_listbox.delete(0, tk.END)
            for i, book in enumerate(books):
                if book[4] == "Borrowed":
                    bg_color = '#fe0017'
                elif book[4] == "lent":
                    bg_color = "#01daff"
                elif i % 2 == 0:
                    bg_color = '#bcbcbc'
                else:
                    bg_color = '#ffffff'
                
                book_name = f"Name: {book[0]}, author: {book[1]}"
                book_listbox.insert(tk.END, book_name)
                book_listbox.itemconfig(tk.END, {'bg': bg_color})

            results_label.config(text=f"{len(books)} results found.")
        else:
            book_listbox.delete(0, tk.END)
            results_label.config(text="Results could not find.")

def auto_search(event):
    search_text = search_entry.get()
    if len(search_text) >= 1:
        search_book()
    if len(search_text) == 0:
        book_listbox.delete(0, tk.END)

def list_books():
    new_window = tk.Toplevel(root)
    new_window.title("All Books")
    new_window.geometry('800x700+700+50')
    
    book_listbox = tk.Listbox(new_window, width=50, height=20, font=('Times new roman', 25, "italic"))
    book_listbox.pack(fill=tk.BOTH, expand=True) 
    book_listbox.config(fg='#000000')
    
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name, author FROM books')
    books = cursor.fetchall()
    connection.close()
    
    for i, book in enumerate(books):
        if i % 2 == 0:
            bg_color = '#bcbcbc'
        else:
            bg_color = '#ffffff'
        
        book_name = f"Name: {book[1]}, Author: {book[2]}"
        book_listbox.insert(tk.END, book_name)
        book_listbox.itemconfig(tk.END, {'bg': bg_color})
    total_book_label = tk.Label(new_window, text=f"Total {len(books)} book found.", font=("Times new roman", 15))
    total_book_label.pack()

    book_listbox.bind("<Double-Button-1>", lambda event: show_book_detail_from_list(event, book_listbox))

def search_book_on_database(search_text):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    
    search_text = search_text.lower()
            
    cursor.execute('SELECT name, author, line, shelf, state FROM books WHERE name LIKE ? OR author LIKE ? ORDER BY name',
                   ('%' + search_text + '%', '%' + search_text + '%'))
    books = cursor.fetchall()
    connection.close()
    
    return books

def list_books_lent():
    new_window = tk.Toplevel(root)
    new_window.title("lent Books")
    new_window.geometry('500x300+950+50')

    book_listbox = tk.Listbox(new_window, width=80, height=20, font=('times new roman', 15), bg="#f0b1a4", exportselection=False)
    book_listbox.pack(fill=tk.BOTH, expand=True)

    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()

    query = 'SELECT id, name, author FROM books WHERE state = "lent"'
    cursor.execute(query)
    
    books = cursor.fetchall()
    connection.close()

    for i, Book in enumerate(books):
        if i % 2 == 0:
            bg_color = '#bcbcbc'
        else:
            bg_color = '#ffffff'
        
        book_name = f"Name: {Book[1]}, author: {Book[2]}"
        book_listbox.insert(tk.END, book_name)
        book_listbox.itemconfig(tk.END, {'bg': bg_color})

    book_listbox.bind("<Double-Button-1>", lambda event: show_book_detail_from_list(event, book_listbox))

def list_books_borrowed():
    new_window = tk.Toplevel(root)
    new_window.title("Borrowed Books")
    new_window.geometry('500x300+950+50')

    book_listbox = tk.Listbox(new_window, width=80, height=20, font=('times new roman', 15), bg="#f0b1a4", exportselection=False)
    book_listbox.pack(fill=tk.BOTH, expand=True)

    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()

    query = 'SELECT id, name, author FROM books WHERE state = "Borrowed"'
    cursor.execute(query)
    
    books = cursor.fetchall()
    connection.close()

    for i, Book in enumerate(books):
        if i % 2 == 0:
            bg_color = '#bcbcbc'
        else:
            bg_color = '#ffffff'
        
        book_name = f"Name: {Book[1]}, author: {Book[2]}"
        book_listbox.insert(tk.END, book_name)
        book_listbox.itemconfig(tk.END, {'bg': bg_color})

    book_listbox.bind("<Double-Button-1>", lambda event: show_book_detail_from_list(event, book_listbox))

def remove_selected_book():
    selected_item = book_listbox.curselection()
    if selected_item:
        index = selected_item[0]
        selected_book = book_listbox.get(index)
        book_name = selected_book.split(",")[0][6:]
        
        answer = messagebox.askyesno("ARE YOU SURE?", f"Are you sure to remove this book : {book_name}")
        
        if answer:
            book_id = remove_book_from_database(book_name)
            if book_id is not None:
                book_listbox.delete(index)
                messagebox.showinfo("Successful", f"{book_name} Book Deleted")
            else:
                messagebox.showerror("Error!", "Book Not Deleted.")
        else:
            messagebox.showinfo("Info", "Book Not Deleted.")
    else:
        messagebox.showerror("Error!", "Select a book!")

def remove_book_from_database(book_name):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT id FROM books WHERE name = ?', (book_name,))
    book_id = cursor.fetchone()
    
    if book_id:
        book_id = book_id[0]
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        connection.commit()
    
    connection.close()
    
    return book_id

def update_selected_book(book_id, new_infos):
    
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    date_info = new_infos[6]  

    if len(new_infos) == 7 and new_infos[4] == "lent":
         cursor.execute('UPDATE books SET name = ?, author = ?, line = ?, shelf = ?, state = ?, lent_person = ?, date = ?, borrowed_person = ? WHERE id = ?',
                   (new_infos[0], new_infos[1], new_infos[2], new_infos[3], new_infos[4], None, date_info, new_infos[5], book_id))
    else:
        if new_infos[4] == 'On shelf':  # If date and person info are empty assign to NULL
            cursor.execute('UPDATE books SET name = ?, author = ?, line = ?, shelf = ?, state = ?, lent_person = ?, date = ?, borrowed_person = ? WHERE id = ?',
                    (new_infos[0], new_infos[1], new_infos[2], new_infos[3], new_infos[4], None, None, None, book_id))
        elif new_infos[4] == 'Borrowed':
            cursor.execute('UPDATE books SET name = ?, author = ?, line = ?, shelf = ?, state = ?, lent_person = ?, date = ?, borrowed_person = ? WHERE id = ?',
                    (new_infos[0], new_infos[1], new_infos[2], new_infos[3], new_infos[4], new_infos[5], date_info, None, book_id))

    connection.commit()
    connection.close()

    messagebox.showinfo("Successful", "Book Updated!")
    update_window.destroy()       

def update_book_window():
    selected_item = book_listbox.curselection()
    if selected_item:
        index = selected_item[0]
        selected_book = book_listbox.get(index)
        book_name = selected_book.split(",")[0][6:]
        book_id = bring_book_id(book_name)
        
        if book_id:
            book_infos = bring_book_infos(book_id)
            global update_window
            update_window = tk.Toplevel(root)
            update_window.title("Update Book")
            update_window.geometry('500x400+800+50')
            update_window.config(bg='#0077b4')
            
            entry_list = []  
            
            for i, (label_text, bilgi) in enumerate(zip(["Book Name:", "Author:", "Line Number:", "Shelf:"], book_infos[:4])):
                label = tk.Label(update_window, text=label_text, bg='#0077b4')
                label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
                entry = tk.Entry(update_window, bg='#0077b4')
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                entry.insert(0, bilgi)  
                entry_list.append(entry)  
            
            state_info_label = tk.Label(update_window, text="state:", bg='#0077b4')
            state_info_label.grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            
            state_var = tk.StringVar()
            state_options = ["Borrowed", "On shelf", "lent"]
            state_var.set(book_infos[4]) 
    
            state_optionmenu = tk.OptionMenu(update_window, state_var, *state_options, command=lambda value: update_bor_or_lent_person(value, bor_or_lent_person_entry, date_cal))
            state_optionmenu.config(bg='#0077b4')
            state_optionmenu.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
            
            date_label = tk.Label(update_window, text="date:", bg='#0077b4')
            date_label.grid(row=i+2, column=0, padx=10, pady=5, sticky="e")
            
            date_cal = DateEntry(
                update_window, width=12, background='darkblue',
                foreground='white', borderwidth=2)
            date_cal.grid(row=i+2, column=1, padx=10, pady=5, sticky="w")
            
            bor_or_lent_person_label = tk.Label(update_window, text="Borrowed or lent Person:", bg='#0077b4')
            bor_or_lent_person_label.grid(row=i+3, column=0, padx=10, pady=5, sticky="e")
            
            bor_or_lent_person_entry = tk.Entry(update_window, bg='#0077b4')
            bor_or_lent_person_entry.grid(row=i+3, column=1, padx=10, pady=5, sticky="w")            
            
            if book_infos[4] == "Borrowed" or book_infos[4] == "lent":
                if book_infos[5]:
                    bor_or_lent_person_entry.insert(0, book_infos[5])  
                elif book_infos[7]:
                    bor_or_lent_person_entry.insert(0, book_infos[7])  
                if book_infos[6]:
                    date_str = book_infos[6]  
                    try:
                        date_datetime = datetime.strptime(date_str, "%Y-%m-%d")  
                        date_cal.set_date(date_datetime.date())  
                    except ValueError:
                        print("Invalid Date Format:", date_str)
                    
            delete_date_button = tk.Button(
                update_window, text="Delete Date",
                command=lambda: delete_lent_bor_date(date_cal))
            delete_date_button.grid(row=i+2, column=2, padx=10, pady=5, sticky="w")
            
            update_button = tk.Button(update_window, bg='#0077b4', text="Update", command=lambda: update_selected_book(book_id, [entry.get() for entry in entry_list] + [state_var.get(), bor_or_lent_person_entry.get(), date_cal.get_date()]))
            update_button.grid(row=i+5, columnspan=2, pady=10)
        else:
            messagebox.showerror("Error!", "Book Could Not Find!.")
    else:
        messagebox.showerror("Error!", "Select a book!") 

def update_bor_or_lent_person(value, bor_or_lent_person_entry, date_cal):
    if value == "On shelf":
        bor_or_lent_person_entry.delete(0, tk.END)
        date_cal.set_date(None)  # Reset Date


def delete_lent_bor_date(date_cal):
    date_cal._set_text("")


def bring_book_id(book_name):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT id FROM books WHERE name = ?', (book_name,))
    book_id = cursor.fetchone()
    
    connection.close()
    
    if book_id:
        return book_id[0]
    else:
        return None
    
def show_selected_book():
    selected_item = book_listbox.curselection()
    if selected_item:
        index = selected_item[0]
        selected_book = book_listbox.get(index)
        book_name = selected_book.split(",")[0][6:]

        book_id = bring_book_id(book_name)
        if book_id is not None:
            show_book_detail(book_id)
        else:
            messagebox.showerror("Error!", "Book Could Not Find!.")
    else:
        messagebox.showerror("Error!", "Select a book!")

def show_book_detail(book_id):
    global window_is_open

    if not window_is_open:
        window_is_open = True
        book_infos = bring_book_infos(book_id)
        def close_window():
            global window_is_open
            window_is_open = False
            detail_window.destroy()

        detail_window = tk.Toplevel(root)
        detail_window.title("Book Detail")
        detail_window.geometry('650x300+800+50')
        detail_window.config(bg='#0077b4')

        detay_label = tk.Label(detail_window, text=f"Book Name: {book_infos[0]}\nAuthor: {book_infos[1]}\nLine: {book_infos[2]}\nshelf: {book_infos[3]}\nstate: {book_infos[4]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
        detay_label.pack()

        detail_window.protocol("WM_DELETE_WINDOW", close_window)
        if book_infos[5] is not None and book_infos[6] is not None:
            lent_person_label = tk.Label(detail_window, text=f"Borrowed Person: {book_infos[5]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
            lent_person_label.pack(pady=(10,0))

            date_label = tk.Label(detail_window, text=f"Borrowed Date: {book_infos[6]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
            date_label.pack()
        elif book_infos[7] is not None and book_infos[6] is not None:
            lent_person_label = tk.Label(detail_window, text=f"Lent Person: {book_infos[7]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
            lent_person_label.pack(pady=(10,0))

            date_label = tk.Label(detail_window, text=f"Lent Date: {book_infos[6]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
            date_label.pack()
        else:
            pass

        
    else:
        pass

def show_book_detail_from_list(event, book_listbox):
    selected_item = book_listbox.curselection()
    if selected_item:
        index = selected_item[0]
        selected_book = book_listbox.get(index)
        book_name = selected_book.split(",")[0][6:]
        book_id = bring_book_id(book_name)
        
        if book_id is not None:
            show_book_detail(book_id)
        else:
            messagebox.showerror("Error!", "Book Could Not Find!.")
    
def bring_book_infos(book_id):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name, author, line, shelf, state, lent_person, date, borrowed_person FROM books WHERE id = ?', (book_id,))
    book_infos = cursor.fetchone()
    connection.close()
    return book_infos

if __name__ == "__main__":

    add_button = tk.Button(root, text="Add Book", command=lambda: open_new_window("Add Book"), bg='#123fff', fg='#ffffff', relief=tk.RAISED)
    add_button.grid(row=0, column=2, padx=(20, 10), pady=10, sticky='e')

    library_label = tk.Label(root, text="LIBRARY OF ÖZCAN'S FAMILY", bg='#0077b4', font=(10))
    library_label.grid(row=0, column=1,columnspan=2, padx=(100, 10), pady=10, sticky='w')

    remove_button = tk.Button(root, text="Remove Selected Book", command=remove_selected_book, bg='#ee0000', fg='#ffffff', relief=tk.RAISED)
    remove_button.grid(row=0, column=0, padx=(10, 20), pady=(10,0), sticky='w')

    search_label = tk.Label(root, text="Search:", bg='#0077b4', fg='#ffffff', font=('times new roman', 13, 'bold'))
    search_label.grid(row=1, column=0, padx=8, pady=(0, 5), sticky='w')

    search_entry = tk.Entry(root)
    search_entry.config(bg='#ffffff', relief=tk.SUNKEN , fg='#000000')
    search_entry.grid(row=1, column=1,columnspan=2, padx=10, pady=(0, 10),ipadx=(250),ipady=(4), sticky='w')

    search_entry.bind("<KeyRelease>", auto_search)

    book_listbox = tk.Listbox(root, width=80, height=9, font=('times new roman', 15), bg="#f0b1a4")
    book_listbox.grid(row=3, column=0, columnspan=3, padx=10, ipadx=20)

    show_detail_button = tk.Button(root, text="Show Book Detail", command=lambda: open_new_window("Book Detail"), bg='#fff111')
    show_detail_button.grid(row=4, column=2, padx=(10, 10), pady=(10, 0),ipady=10, sticky='e')

    results_label = tk.Label(root, text="", bg='#0077b4', fg='#ffffff', font=('times new roman', 12, 'bold'))
    results_label.grid(row=4, column=1, padx=(100,80), pady=5, sticky='we')

    update_book_button = tk.Button(root, text="Update Selected Book", command=lambda: open_new_window("Update Book"), bg='#fff111', relief="raised")
    update_book_button.grid(row=4, column=0, padx=(10, 10), pady=(10, 0),ipady=10, sticky='w')

    list_lent_button = tk.Button(root, text="List lent Books", relief="raised", command=lambda: open_new_window("lent Books"), bg='#fff111')
    list_lent_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='we')

    list_borrowed_button = tk.Button(root, text="List Borrowed Books", relief="raised", command=lambda: open_new_window("Borrowed Books"), bg='#fff111')
    list_borrowed_button.grid(row=6, column=0, columnspan=3, padx=10, pady=(10,0), sticky='we')

    listele_button = tk.Button(root, text="List Books", relief="raised", command=lambda: open_new_window("All Books"), bg='#fff111')
    listele_button.grid(row=7, column=0, columnspan=3,ipady=5, padx=10, pady=20, sticky='we')


    root.mainloop()