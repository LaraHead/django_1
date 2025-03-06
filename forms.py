from django import forms
#from .models import *

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Выберите XML файл')
    #all_files = forms.BooleanField(required=False, label='Обработать все файлы в папке?')