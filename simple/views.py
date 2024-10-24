import datetime
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views.generic import View
from weasyprint import HTML

from simple.htmlContent import html_content
from smallFriends.models import Generate
from smallFriends.views import METHOD


class Simple(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'title': "Oddiy",
            'section': "Oddiy sonlar",
        }
        return render(request, 'simple.html', context)

    def post(self, request):
        column, digits, count = request.POST.get('column'), request.POST.get('digits'), request.POST.get('count')
        method = request.POST.get('method')
        mode = "Oddiy"

        f_name = f"{column} ustun {mode} {digits} xona {count}0 ta {METHOD[method]} " + str(int(datetime.datetime.now().timestamp()))
        title = f"{column} ustun {mode} {digits} xona {count}0 ta {METHOD[method]}"

        # HTML fayl yaratish
        hc = html_content(column=int(column), digits=int(digits), count=int(count), method=method, title=title)


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
                    'title': "Oddiy",
                    'section': "Oddiy sonlar",
                    'file_id': generate_instance.id,
                }
                return render(request, 'simple.html', context)
        context = {
            'title': "Oddiy",
            'section': "Oddiy sonlar",
            'error': "Qandaydur xatolik yuz berdi!"
        }
        return render(request, 'simple.html', context)
