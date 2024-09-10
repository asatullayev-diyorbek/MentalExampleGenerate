import os
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
import datetime
from .htmlContent import html_content
from django.core.files.storage import default_storage
from weasyprint import HTML
from .models import Generate
from django.contrib.auth.mixins import LoginRequiredMixin


class Menu(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'title': 'Yulduzcha Generatsiyasi',
            'section': 'Yulduzcha Generatsiyasiga Xush Kelibsiz!',
        }
        return render(request, 'menu.html', context)


class SmallFriends(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'title': "Kichik do'st",
            'section': "Kichik do'st sonlar",
        }
        return render(request, 'smallFriends.html', context)

    def post(self, request):
        print("So'rov keldi")
        column, size, count = request.POST.get('column'), request.POST.get('size'), request.POST.get('count')
        requirement, method = request.POST.get('requirement'), request.POST.get('method')
        mode = "kichik-dust"

        f_name = f"{column} ustun {mode} {size} xona {count}0 ta {requirement} {'parallel' if method == 'parallel' else 'aralash'} " + str(int(datetime.datetime.now().timestamp()))
        title = f"{column} ustun {mode} {size} xona {count}0 ta {requirement} {'parallel' if method == 'parallel' else 'aralash'}"
        # HTML fayl yaratish
        hc = html_content(column=int(column), size=int(size), count=int(count), mode=mode, requirement=requirement, method=method)
        html_path = default_storage.save(f'generate/html/{f_name}.html', ContentFile(hc))

        pdf_content = HTML(f'media/{html_path}').write_pdf()
        pdf_path = default_storage.save(f'generate/pdf/{f_name}.pdf', ContentFile(pdf_content))

        generate_instance = Generate(
            title=title,
            file_html=html_path,
            file_pdf=pdf_path,
            user=request.user,
        )
        generate_instance.save()

        if generate_instance.file_pdf:
            file_path = generate_instance.file_pdf.path
            if os.path.exists(file_path):
                context = {
                    'title': "Kichik do'st",
                    'section': "Kichik do'st sonlar",
                    'file_id': generate_instance.id,
                }
                return render(request, 'smallFriends.html', context)
        context = {
            'title': "Kichik do'st",
            'section': "Kichik do'st sonlar",
            'error': "Qandaydur xatolik yuz berdi!"
        }
        return render(request, 'smallFriends.html', context)

def download_pdf(request, file_id):
    file_instance = get_object_or_404(Generate, id=file_id)
    if file_instance.file_pdf:
        file_path = file_instance.file_pdf.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
                return response
    raise Http404("Fayl mavjud emas yoki topilmadi.")

