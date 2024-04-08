'''from flask import Flask, request, render_template
import PyPDF2
import io
import os
from openai import OpenAI

# Set up OpenAI API key (replace with your actual key)
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

app = Flask(__name__)

def extract_and_summarize_pdf(pdf_content, search_keywords=None):
    """
    Extracts data from a PDF content, optionally filters by multiple keywords, and summarizes it using OpenAI.

    Args:
        pdf_content (bytes): Content of the PDF file.
        search_keywords (list, optional): List of keywords to filter extracted data (default: None).

    Returns:
        tuple: A tuple containing the summarized text and the extracted data.
    """
    extracted_data = []

    pdf_file = io.BytesIO(pdf_content)
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)

    for page_number in range(num_pages):
        page = reader.pages[page_number]
        text = page.extract_text()

        # Split the text into lines
        lines = text.split('\n')

        # Optionally filter by multiple keywords
        if search_keywords:
            for line in lines:
                if any(keyword in line for keyword in search_keywords):
                    extracted_data.append(line)

    # Combine extracted data for summarization
    data_to_summarize = "\n".join(extracted_data)

    messages = [
        {"role": "system", "content": "You are a helpful PDF summarization assistant."},
        {"role": "user", "content": f"Summarize this along with proper details: {data_to_summarize}."}
    ]

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',  # Experiment with models for longer text
        messages=messages,
        max_tokens=270,  # Adjust based on desired summary length
        stop=None,
        temperature=0.8  # Fine-tune for conciseness and factual accuracy
    )

    # Access generated summary
    summary_text = response.choices[0].message.content.strip()
    return summary_text, extracted_data

@app.route('/', methods=['GET', 'POST'])
def upload_or_display():
    if request.method == 'GET':
        # Display upload form
        return render_template('try.html', form=True)
    elif request.method == 'POST':
        if 'pdf_file' not in request.files:
            return render_template('try.html', message='No file uploaded!', form=True)
    
        pdf_file = request.files['pdf_file']
        pdf_content = pdf_file.read()

        # Split the keywords by a comma 
        search_keywords = request.form['keywords'].split(',') if request.form['keywords'] else None 

        summary_text, extracted_data = extract_and_summarize_pdf(pdf_content, search_keywords)

        return render_template('try.html', summary=summary_text, extracted_data=extracted_data)

if __name__ == '__main__':
    app.run(debug=True)
'''

from flask import Flask, request, render_template
import PyPDF2
import io
import os
from openai import OpenAI

# Set up OpenAI API key (replace with your actual key)
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

app = Flask(__name__)

def extract_and_summarize_pdf(pdf_content, search_sentence=None):
    """
    Extracts data from a PDF content, optionally filters by a sentence (treated as multiple keywords), and summarizes it using OpenAI.

    Args:
        pdf_content (bytes): Content of the PDF file.
        search_sentence (str, optional): Sentence to treat as keywords for filtering extracted data (default: None).

    Returns:
        tuple: A tuple containing the summarized text and the extracted data.
    """
    extracted_data = []

    pdf_file = io.BytesIO(pdf_content)
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)

    for page_number in range(num_pages):
        page = reader.pages[page_number]
        text = page.extract_text()

        # Split the text into lines
        lines = text.split('\n')

        # Optionally filter by a sentence (treated as multiple keywords)
        if search_sentence and search_sentence.strip():  # Check if sentence is not empty
            search_keywords = search_sentence.split()  # Split sentence into individual words
            for line in lines:
                if any(keyword in line for keyword in search_keywords):
                    extracted_data.append(line)
        else:
            extracted_data.extend(lines)  # No sentence provided, include all lines

    # Combine extracted data for summarization
    data_to_summarize = "\n".join(extracted_data)

    # Trim input sentence if it exceeds maximum token count
    max_tokens = 150  # Adjust based on desired summary length
    search_sentence_trimmed = ' '.join(search_sentence.split()[:max_tokens])

    messages = [
        {"role": "system", "content": "You are a helpful PDF summarization assistant."},
        {"role": "user", "content": f"Summarize this along with proper details and provide numeric values if necessary: {search_sentence_trimmed}."}
    ]

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',  # Experiment with models for longer text
        messages=messages,
        max_tokens=max_tokens,
        stop=None,
        temperature=0.8  # Fine-tune for conciseness and factual accuracy
    )

    # Access generated summary
    summary_text = response.choices[0].message.content.strip()
    return summary_text, extracted_data

@app.route('/', methods=['GET', 'POST'])
def upload_or_display():
    if request.method == 'GET':
        # Display upload form
        return render_template('try.html', form=True)
    elif request.method == 'POST':
        if 'pdf_file' not in request.files:
            return render_template('try.html', message='No file uploaded!', form=True)
    
        pdf_file = request.files['pdf_file']
        pdf_content = pdf_file.read()

        search_sentence = request.form['sentence']

        summary_text, extracted_data = extract_and_summarize_pdf(pdf_content, search_sentence)

        return render_template('try.html', summary=summary_text, extracted_data=extracted_data)

if __name__ == '__main__':
    app.run(debug=True)



