import os
from weasyprint import HTML


def create_pdf(html_path):
    if os.path.exists(f"media/renders/html/{html_path}.html"):
        print("Bajarilmoqda...")
        HTML(f"media/renders/html/{html_path}.html").write_pdf(f'media/renders/pdf/{html_path}')
        print("saqlandi")
    else:
        print("File not found!")
