import json


class Library:
    def __init__(self):
        self.books = {}
        self.borrowed = {}
        self.borrowing_id = 1

    def save_data(self):
        data = {
            "books": [],
            "borrowed": self.borrowed,
            "borrowing_id": self.borrowing_id,
        }

        for book in self.books.values():
            book_data = {
                "bookId": book.bookId,
                "title": book.title,
                "author": book.author,
                "total_quantity": book.total_quantity,
                "available_quantity": book.available_quantity,
                "price": book.price,
            }

            data["books"].append(book_data)

        with open("library_data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)

            self.books = {}

            for book_data in data["books"]:
                book = Book(
                    book_data["bookId"],
                    book_data["title"],
                    book_data["author"],
                    book_data["total_quantity"],
                    book_data["available_quantity"],
                    book_data["price"],
                )

                self.books[book.bookId] = book

            self.borrowed = {int(key): value for key, value in data["borrowed"].items()}

            self.borrowing_id = data["borrowing_id"]

        except FileNotFoundError:
            print("No saved library data found. Starting fresh!")

    def add_books(self, book):
        self.books[book.bookId] = book

    def add_book_by_input(self):
        while True:
            bookId = int(input("Enter the book ID: "))
            if bookId > 0:
                break
            else:
                print("please enter a valid bookid")

        if bookId in self.books:
            print("book id already exist")
            return

        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book: ")

        while True:
            total_quantity = int(input("Enter the total quantity: "))
            if total_quantity > 0:
                break
            else:
                print("please enter a positive number")

        available_quantity = total_quantity

        while True:
            price = int(input("Enter the price of the book: "))
            if price > 0:
                break
            else:
                print("enter a valid price")

        book = Book(bookId, title, author, total_quantity, available_quantity, price)

        self.add_books(book)

    def view_books(self):
        for book in self.books.values():
            book.display()

    def search_books(self):
        search_id = int(input("enter the book id you want to find"))

        if search_id in self.books:
            found_book = self.books[search_id]
            found_book.display()
        else:
            print("book not found")

    def search_book_bytitle(self):
        search_title = input("enter the title of the book you want to find")
        found = False

        for bookobj in self.books.values():
            if bookobj.title.lower() == search_title.lower():
                found = True
                print("book found")
                bookobj.display()

        if found == False:
            print("book not found")

    def issue_book(self, student_name, student_id, book_id, quantity):
        if book_id not in self.books:
            return False, "Book not found!"

        book = self.books[book_id]

        if quantity <= 0:
            return False, "Please enter a valid quantity!"

        if book.available_quantity < quantity:
            return False, "Not enough copies available!"

        book.available_quantity -= quantity

        self.borrowed[self.borrowing_id] = {
            "student_name": student_name,
            "student_id": student_id,
            "borrowing_bookid": book_id,
            "quantity": quantity,
        }

        self.borrowing_id += 1

        return True, "Book issued successfully!"

    def return_book(self, student_id, book_id, quantity):
        if book_id not in self.books:
            return False, "Book not found!"

        if quantity <= 0:
            return False, "Please enter a valid quantity!"

        for borrowing_id, details in self.borrowed.items():
            if (
                details["student_id"] == student_id
                and details["borrowing_bookid"] == book_id
            ):
                if quantity > details["quantity"]:
                    return False, "You cannot return more copies than borrowed!"

                details["quantity"] -= quantity
                self.books[book_id].available_quantity += quantity

                if details["quantity"] == 0:
                    del self.borrowed[borrowing_id]

                return True, "Book returned successfully!"

        return False, "No matching borrowing record found!"

    def check_availability(self):
        check_id = int(input("enter the bookid of the book you want to check"))

        if check_id in self.books:
            print(
                f"available quantity is = " f"{self.books[check_id].available_quantity}"
            )
        else:
            print("book not found")

    def main_menu(self):
        choice = 0

        while choice != 8:
            print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
            print("1. Add Book")
            print("2. View Books")
            print("3. Search Book by ID")
            print("4. Search Book by Title")
            print("5. Issue Book")
            print("6. Return Book")
            print("7. check book availability")
            print("8. exit")

            choice = int(input("ENTER YOUR CHOICE : "))

            if choice == 1:
                self.add_book_by_input()
            elif choice == 2:
                self.view_books()
            elif choice == 3:
                self.search_books()
            elif choice == 4:
                self.search_book_bytitle()
            elif choice == 5:
                self.issue_book()
            elif choice == 6:
                self.return_book()
            elif choice == 7:
                self.check_availability()
            elif choice == 8:
                print("Thank you for using the Library Management System!")
            else:
                print("Invalid choice! Please try again.")


class Book:
    def __init__(
        self, bookId, title, author, total_quantity, available_quantity, price
    ):
        self.bookId = bookId
        self.title = title
        self.author = author
        self.total_quantity = total_quantity
        self.available_quantity = available_quantity
        self.price = price

    def display(self):
        print(
            f"Book ID: {self.bookId}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"Total Quantity: {self.total_quantity}, "
            f"Available Quantity: {self.available_quantity}, "
            f"Price: {self.price}"
        )


library = Library()
