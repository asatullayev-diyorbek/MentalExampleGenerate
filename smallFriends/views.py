import os
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import View
import datetime
from .htmlContent import html_content
from django.core.files.storage import default_storage
from weasyprint import HTML
from .models import Generate
from django.contrib.auth.mixins import LoginRequiredMixin
import base64


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
        column, size, count = request.POST.get('column'), request.POST.get('size'), request.POST.get('count')
        mode = "kichik-dust"

        f_name = f"{column}-ustun-{mode}-{size}-xona-{count}0-ta-" + str(int(datetime.datetime.now().timestamp()))
        title = f"{column} ustun {mode} {size} xona {count}0 ta"
        # HTML fayl yaratish
        hc = html_content(column=int(column), size=int(size), count=int(count), mode=mode)
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
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    return response
        return JsonResponse({'error': "Faylni yuklashda xatolik! qaytadan urinib ko'ring"})

# def download_message_file(request, file_id):
#     file_instance = get_object_or_404(Ticket, id=file_id)
#     if file_instance.message_file:
#         file_path = file_instance.message_file.path
#         if os.path.exists(file_path):
#             with open(file_path, 'rb') as fh:
#                 response = HttpResponse(fh.read(), content_type="application/octet-stream")
#                 response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
#                 return response
#     raise Http404("Fayl mavjud emas yoki topilmadi.")
        # # HTML fayl yaratish
        #     html_content = render_to_string('template.html', {'context_data': 'value'})
        #     html_path = default_storage.save('media/html_file.html', ContentFile(html_content))
        #
        #     # PDF fayl yaratish
        #     pdf_content = HTML(string=html_content).write_pdf()
        #     pdf_path = default_storage.save('media/pdf_file.pdf', ContentFile(pdf_content))
        #
        #     # Fayl yo'llarini Generate modeliga yozish
        #     generate_instance = Generate(html_file=html_path, pdf_file=pdf_path)
        #     generate_instance.save()
