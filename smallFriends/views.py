import os
from django.core.files.base import ContentFile
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
import datetime
from .htmlContent import html_content
from django.core.files.storage import default_storage
from weasyprint import HTML
from .models import Generate, Telegram
from django.contrib.auth.mixins import LoginRequiredMixin
from telebot import TeleBot

METHOD = {
    'parallel': 'Parallel',
    'mixed': 'Aralash',
    'tenner': "O'nlik"
}


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
        start = datetime.datetime.now()
        column, digits, count = request.POST.get('column'), request.POST.get('digits'), request.POST.get('count')
        requirement, method = request.POST.get('requirement'), request.POST.get('method')
        mode = "Kichik do'st"

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
                    'title': "Kichik do'st",
                    'section': "Kichik do'st sonlar",
                    'file_id': generate_instance.id,
                }
                end = datetime.datetime.now()
                print(f"Generatsiya vaqti: {end-start}")
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
                response['Content-Disposition'] = f'attachment; filename={file_instance.title}.pdf'
                return response
    raise Http404("Fayl mavjud emas yoki topilmadi.")


def send_to_telegram(request, file_id):
    chats_id = Telegram.objects.filter(user=request.user).values_list('chat_id', flat=True)

    if not chats_id.exists():
        return JsonResponse({"status": "error", "message": "Sizda ushbu funksiyadan foydalanish huquqi yo'q"})

    bot_token = "8069358924:AAG9egNic3bx6wHBvD5Eqepl9RDDdRNcpTQ"
    admin_chat_id = '5547740249'


    file_instance = Generate.objects.get(id=file_id)

    if file_instance.file_pdf:
        file_path = file_instance.file_pdf.path

        # Fayl mavjudligini tekshirish
        if not os.path.exists(file_path):
            return JsonResponse({"status": "error", "message": "Fayl yo'q."}, status=404)

        bot = TeleBot(token=bot_token)
        caption_text = f"Sarlavha: {file_instance.title}"
        caption_text_admin = f"#Admin uchun xabar\nGeneratsiya qildi: {request.user.get_full_name()}\nSarlavha: {file_instance.title}"

        # Foydalanuvchilarga fayl va matnni bitta xabarda yuborish
        for chat_id in chats_id:
            try:
                with open(file_path, 'rb') as pdf_file:
                    bot.send_document(chat_id=chat_id, document=pdf_file, caption=caption_text)
            except Exception as e:
                print(f"Foydalanuvchiga yuborishda xato: {str(e)}")
                return JsonResponse({"status": "error",
                                     "message": "Telegramdan <a href='https://t.me/yulduzchageneratebot' target=_blank'>@yulduzchageneratebot</a> ga a'zo bo'lmagansiz."})

        # Adminga fayl va matnni bitta xabarda yuborish
        try:
            with open(file_path, 'rb') as pdf_file:
                bot.send_document(chat_id=admin_chat_id, document=pdf_file, caption=caption_text_admin)
        except Exception as e:
            print(f"Adminga yuborishda xato: {str(e)}")
            return JsonResponse({"status": "error", "message": "Adminga fayl yuborishda xato."})

        return JsonResponse({"status": "success", "message": "Fayl Telegram orqali muvaffaqiyatli yuborildi."})

    return JsonResponse({"status": "error", "message": "Fayl mavjud emas yoki topilmadi."}, status=404)

