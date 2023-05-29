import PyPDF2
import win32api
import win32print


def send_print(file_name):
    pdf_file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_content = page.extract_text()
        print(page_content)
        win32api.ShellExecute(
            0,
            "print",
            file_name,
            f'/d:"{win32print.GetDefaultPrinter()}"',
            ".",
            0
        )
    pdf_file.close()


# PASSWORD = "123"
# file = "image-based-pdf-sample.pdf"
# enter_pass = input("password to print: ")
# if enter_pass == PASSWORD:
#     send_print(file)

