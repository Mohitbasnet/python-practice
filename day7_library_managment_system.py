# Write a Library class with no_of_books and books as two instance variables. Write a program to create a library from this Library class and show how you can print all books, add a book and get the number of books using different methods. Show that your program doesnt persist the books after the program is stopped!


class Library:
    def __init__(self, books):
        self.books = books
        self.no_of_books = len(books)
    def display_books(self):
       print(f"There are {self.no_of_books} books in the Library.\nThe books are:")
       for book in self.books:
        print(book)

    
    def add_book(self, book):
        self.books.append(book)
        self.no_of_books +=1
  

            
        
# create a library object
library = Library(["Doglapan","The monk who sold his farari","THe subtle art of not giving a fuck"])

# display the books
library.display_books()

# add a new book
library.add_book("Think like a monk")
library.add_book("The mornig miracle")

# display the books again
library.display_books()

