import PyPDF2
import re

file_name = "Employee Sample Data.pdf"
doc = PyPDF2.PdfReader(file_name)

# Get the number of pages
num_pages = len(doc.pages)  # Call the method here

# Search terms
search = 'Beijing'

# List of tuples (count of occurrences, page number)
list_pages = []

for i in range(num_pages):  # Use the stored number of pages
    current_page = doc.pages[i]
    text = current_page.extract_text()

    # Find all occurrences using re.findall
    occurrences = re.findall(search, text)
    count_page = len(occurrences)

    if occurrences:  # Check if there are any occurrences
        list_pages.append((count_page, i + 1))

print(list_pages)
