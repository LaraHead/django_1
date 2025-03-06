import os
from lxml import etree

from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Получите загруженный файл
            xml_file = request.FILES['file']

            fs = FileSystemStorage()
            filename = fs.save(xml_file.name, xml_file)
            file_path = fs.path(filename)
            #try:
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            xml_tree = etree.XML(xml_content)
            svul = xml_tree.findall('СвЮЛ')
            ogrn_value = None  # Инициализация переменной
            for sv in svul:
                ogrn_value = sv.get('ОГРН')

            # Логика выбора XSLT файла
            if len(ogrn_value) == 13:
                xslt_file = 'vo_rugf_asv.xsl'
            else:
                xslt_file = 'vo_rigf_asv.xsl'

            xslt_file_path = os.path.join(settings.MEDIA_ROOT, xslt_file)

            # Обработка XSLT и сохранение результата
            with open(xslt_file_path, 'rb') as f:
                xslt_content = f.read()

            xslt_tree = etree.XML(xslt_content)
            transform = etree.XSLT(xslt_tree)
            result_tree = transform(xml_tree)

            filename_without_extension = os.path.splitext(file_path)[0]
            filename_out = filename_without_extension + '.html'
            filename_out_path= os.path.join(settings.MEDIA_ROOT,filename_out)
            with open(filename_out_path, 'wb') as f:
                f.write(etree.tostring(result_tree, pretty_print=True, encoding='utf-8'))
            # Теперь мы можем рендерить HTML
            with open(filename_out_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

                return render(request, 'viptohmtl/display_html.html', {'html_content': html_content})


                #return HttpResponse(str(result_tree), content_type='text/html')

        #return render(request, 'viptohmtl/success.html', {'file_path': file_path})
            #except Exception as e:
            #    return HttpResponse(f"Произошла ошибка: {e}", status=500)

    else:
        form = UploadFileForm()

    return render(request, "viptohmtl/mainform.html", {"form": form})

