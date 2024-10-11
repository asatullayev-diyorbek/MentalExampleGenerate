import datetime
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views.generic import View
from weasyprint import HTML

from family.htmlContent import html_content
from smallFriends.models import Generate
from smallFriends.views import METHOD


class Family(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'title': "Oila",
            'section': "Oila sonlar",
        }
        return render(request, 'family.html', context)

    def post(self, request):
        start = datetime.datetime.now()
        column, digits, count = request.POST.get('column'), request.POST.get('digits'), request.POST.get('count')
        requirement, method = request.POST.get('requirement'), request.POST.get('method')
        mode = "Oila"

        f_name = f"{column} ustun {mode} {digits} xona {count}0 ta {requirement if digits == 1 else ''} {METHOD[method]} " + str(int(datetime.datetime.now().timestamp()))
        title = f"{column} ustun {mode} {digits} xona {count}0 ta {requirement if digits == 1 else ''} {METHOD[method]}"

        # HTML fayl yaratish
        hc = html_content(column=int(column), digits=int(digits), count=int(count), requirement=requirement, method=method, title=title)


        pdf_content = HTML(string=hc).write_pdf()
        pdf_path = default_storage.save(f'generate/pdf/{f_name}.pdf', ContentFile(pdf_content))

        generate_instance = Generate(
            title=title,
            file_html=pdf_path,
            file_pdf=pdf_path,
            user=request.user,
        )
        generate_instance.save()

        if generate_instance.file_pdf:
            file_path = generate_instance.file_pdf.path
            if os.path.exists(file_path):
                context = {
                    'title': "Oila",
                    'section': "Oila sonlar",
                    'file_id': generate_instance.id,
                }
                end = datetime.datetime.now()
                print(f"Generatsiya vaqti: {end-start}")
                return render(request, 'family.html', context)
        context = {
            'title': "Oila",
            'section': "Oila sonlar",
            'error': "Qandaydur xatolik yuz berdi!"
        }
        return render(request, 'family.html', context)
