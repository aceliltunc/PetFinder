from django import forms
from .models import Pet, AdoptionRequest
from django import forms

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'gender', 'description', 'image', 'status']

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['message']
