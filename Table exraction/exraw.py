import PyPDF2

def extract_rows_from_pdf(pdf_path, search_keyword):
    extracted_rows = []
    
    with open("C:/Users/Admin/Desktop/Table exraction/Employee Sample Data.pdf", 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text = page.extract_text()
            
            # Split the text into lines
            lines = text.split('\n')
            
            for line in lines:
                # Check if the search keyword is present in the line
                if search_keyword in line:
                    # Append the line to the extracted rows
                    extracted_rows.append(line)
    
    return extracted_rows

# Example usage
pdf_path = 'C:/Users/Admin/Desktop/Table exraction/Employee Sample Data.pdf'  # Path to the PDF file
search_keyword = 'Manufacturing'  # Keyword to search for in the PDF
extracted_rows = extract_rows_from_pdf(pdf_path, search_keyword)

# Print the extracted rows
for row in extracted_rows:
    print(row)
