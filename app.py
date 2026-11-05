from flask import Flask, render_template, request
from library import library, Book

app = Flask(__name__)

library.load_data()

if not library.books:
    book1 = Book(
        101, "Harry Potter and the Philosopher’s Stone", "J.K. Rowling", 5, 5, 499
    )
    book2 = Book(
        102, "Harry Potter and the Chamber of Secrets", "J.K. Rowling", 5, 5, 499
    )
    book3 = Book(
        103, "Harry Potter and the Prisoner of Azkaban", "J.K. Rowling", 5, 5, 499
    )

    library.add_books(book1)
    library.add_books(book2)
    library.add_books(book3)

    library.save_data()


@app.route("/")
def dashboard():
    total_books = sum(book.total_quantity for book in library.books.values())

    available_books = sum(book.available_quantity for book in library.books.values())

    borrowed_books = total_books - available_books

    recent_books = list(library.books.values())[-5:]

    return render_template(
        "dashboard.html",
        total_books=total_books,
        available_books=available_books,
        borrowed_books=borrowed_books,
        recent_books=recent_books,
    )


@app.route("/books")
def view_books():
    return render_template("view_books.html", books=library.books.values())


@app.route("/add-book", methods=["GET", "POST"])
def add_book():
    message = ""

    if request.method == "POST":
        book_id = request.form.get("bookId")
        title = request.form.get("title")
        author = request.form.get("author")
        quantity = request.form.get("quantity")
        price = request.form.get("price")

        book_id = int(book_id)
        quantity = int(quantity)
        price = float(price)

        if price <= 0:
            message = "Price must be greater than 0!"

        elif book_id not in library.books:
            new_book = Book(book_id, title, author, quantity, quantity, price)
            library.add_books(new_book)
            library.save_data()
            message = "Book added successfully!"

        else:
            message = "Book ID already exists!"

    return render_template("add_book.html", message=message)


@app.route("/search")
def search_book():
    search_query = request.args.get("q", "").strip()

    results = []

    for book in library.books.values():
        if (
            search_query.lower() in str(book.bookId).lower()
            or search_query.lower() in book.title.lower()
            or search_query.lower() in book.author.lower()
        ):
            results.append(book)

    return render_template(
        "search_book.html",
        books=results,
        search_query=search_query,
    )


@app.route("/issue-book", methods=["GET", "POST"])
def issue_book():
    message = ""

    if request.method == "POST":
        student_name = request.form.get("studentName", "").strip()
        student_id = request.form.get("studentId", "").strip()

        if not student_name or not student_id:
            message = "Please enter the student details!"
        else:
            try:
                book_id = int(request.form.get("bookId"))
                quantity = int(request.form.get("quantity"))

                success, message = library.issue_book(
                    student_name,
                    student_id,
                    book_id,
                    quantity,
                )

                if success:
                    library.save_data()

            except (ValueError, TypeError):
                message = "Please enter valid book ID and quantity!"

    return render_template("issue_book.html", message=message)


@app.route("/return-book", methods=["GET", "POST"])
def return_book():
    message = ""

    if request.method == "POST":
        student_id = request.form.get("studentId", "").strip()

        try:
            book_id = int(request.form.get("bookId"))
            quantity = int(request.form.get("quantity"))

            if not student_id:
                message = "Please enter the student ID!"
            else:
                success, message = library.return_book(
                    student_id,
                    book_id,
                    quantity,
                )

                if success:
                    library.save_data()

        except (ValueError, TypeError):
            message = "Please enter a valid book ID and quantity!"

    return render_template("return_book.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
