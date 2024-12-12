from django.shortcuts import render
import requests

import PyPDF2, pdfplumber
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure

import os, re 


def extract_table(pdf_path, page_num, table_num):
    # Открываем файл pdf
    pdf = pdfplumber.open(pdf_path)
    # Находим исследуемую страницу
    table_page = pdf.pages[page_num]
    # Извлекаем соответствующую таблицу
    table = table_page.extract_tables()[table_num]
    return table

# Преобразуем таблицу в соответствующий формат
def table_converter(table):
    table_string = ''
    # Итеративно обходим каждую строку в таблице
    for row_num in range(len(table)):
        row = table[row_num]
        # Удаляем разрыв строки из текста с переносом
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        # Преобразуем таблицу в строку
        table_string+=('|'+'|'.join(cleaned_row)+'|'+'\n')
    # Удаляем последний разрыв строки
    table_string = table_string[:-1]
    return table_string

def text_extraction(element):
    # Извлекаем текст из вложенного текстового элемента
    line_text = element.get_text()
    
    # Находим форматы текста
    # Инициализируем список со всеми форматами, встречающимися в строке текста
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Итеративно обходим каждый символ в строке текста
            for character in text_line:
                if isinstance(character, LTChar):
                    # Добавляем к символу название шрифта
                    line_formats.append(character.fontname)
                    # Добавляем к символу размер шрифта
                    line_formats.append(character.size)
    # Находим уникальные размеры и названия шрифтов в строке
    format_per_line = list(set(line_formats))
    
    # Возвращаем кортеж с текстом в каждой строке вместе с его форматом
    return (line_text, format_per_line)

pdf_path = 'pdf_test\\golang.pdf'

# создаём объект файла PDF
pdfFileObj = open(pdf_path, 'rb')
# создаём объект считывателя PDF
pdfReaded = PyPDF2.PdfReader(pdfFileObj)

# Создаём словарь для извлечения текста из каждого изображения
text_per_page = {}

# Извлекаем страницы из PDF
for pagenum, page in enumerate(extract_pages(pdf_path)):

    # Initialize the variables needed for the text extraction from the page
    pageObj = pdfReaded.pages[pagenum]
    page_text = []
    line_format = []
    text_from_images = []
    text_from_tables = []
    page_content = []
    # Initialize the number of the examined tables
    table_in_page= -1
    # Open the pdf file
    pdf = pdfplumber.open(pdf_path)
    # Find the examined page
    page_tables = pdf.pages[pagenum]
    # Find the number of tables in the page
    tables = page_tables.find_tables()
    if len(tables)!=0:
        table_in_page = 0

    # Extracting the tables of the page
    for table_num in range(len(tables)):
        # Extract the information of the table
        table = extract_table(pdf_path, pagenum, table_num)
        # Convert the table information in structured string format
        table_string = table_converter(table)
        # Append the table string into a list
        text_from_tables.append(table_string)

    # Find all the elements
    page_elements = [(element.y1, element) for element in page._objs]
    # Sort all the element as they appear in the page 
    page_elements.sort(key=lambda a: a[0], reverse=True)


    # Find the elements that composed a page
    for i,component in enumerate(page_elements):
        # Extract the element of the page layout
        element = component[1]


            

        # Check if the element is text element
        if isinstance(element, LTTextContainer):
            # Use the function to extract the text and format for each text element
            (line_text, format_per_line) = text_extraction(element)
            # Append the text of each line to the page text
            page_text.append(line_text)
            # Append the format for each line containing text
            line_format.append(format_per_line)
            page_content.append(line_text)


            


    # Create the key of the dictionary
    dctkey = 'Page_'+str(pagenum)
    # Add the list of list as value of the page key
    text_per_page[dctkey]= [page_text, line_format, text_from_images,text_from_tables, page_content]

# Close the pdf file object
pdfFileObj.close()
# # Display the content of the page
# result = ''.join(text_per_page['Page_0'][4])
# print(text_per_page)
# print(result)

new_arr = []

def read_page():
    for page in text_per_page.values():
        value_page = ''.join(page[4])
        result = re.sub(r"\n"," ", value_page)
        new_arr.append(result)
    
    return new_arr
        
print(read_page())



def chat_view(request):
    messages = []
    response = None
    if request.method == 'POST':
        user_question = request.POST.get('question')
        answer = get_answer_from_api(user_question)
        messages.append({'user': 'user', 'text': user_question})
        messages.append({'user': 'bot', 'text': answer})
    
    return render(request, 'chat.html', {'messages': messages})

def get_answer_from_api(question):
    api_url = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    headers = {"Authorization": "Bearer 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"}
    context = [
        'Привет - Привет!',
        'Ты - HR-ассистент Хьюстон',
    ]
    combined_context = " ".join(context)
    data = {
        "inputs": {
            "question": question,
            "context": combined_context
        }
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        answer = response.json()
        return answer.get('answer', 'Ответ не найден.')
    else:
        return "Ошибка обращения к API"
