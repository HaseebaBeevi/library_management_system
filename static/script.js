
const bookSearch = document.getElementById("bookSearch");
const statusFilter = document.getElementById("statusFilter");
const bookRows = document.querySelectorAll(".book-row");
const emptyMessage = document.getElementById("emptyMessage");
const bookCount = document.getElementById("bookCount");

function filterBooks() {
    const searchValue = bookSearch.value.toLowerCase().trim();
    const selectedStatus = statusFilter.value;

    let visibleCount = 0;

    bookRows.forEach((row) => {
        const rowText = row.textContent.toLowerCase();
        const rowStatus = row.dataset.status;

        const matchesSearch = rowText.includes(searchValue);

        const matchesStatus =
            selectedStatus === "all" || rowStatus === selectedStatus;

        if (matchesSearch && matchesStatus) {
            row.style.display = "";
            visibleCount++;
        } else {
            row.style.display = "none";
        }
    });

    emptyMessage.classList.toggle("hidden", visibleCount !== 0);

    bookCount.textContent = `Showing ${visibleCount} books`;
}

bookSearch.addEventListener("input", filterBooks);
statusFilter.addEventListener("change", filterBooks);
