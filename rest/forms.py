from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='select a CSV file')

    