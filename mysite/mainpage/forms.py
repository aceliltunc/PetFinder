from django import forms
from .models import Pet, AdoptionRequest, Tag
import datetime

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

class PetForm(forms.ModelForm):
    tags_text = forms.CharField(required=False, help_text="Etiketleri virgülle ayırarak yazın.")
    tags = forms.ModelMultipleChoiceField(
           queryset=Tag.objects.all(),
           widget=forms.CheckboxSelectMultiple,
           required=False,
           label="Etiketler",
           help_text="Mevcut etiketlerden seçin veya yeni etiket ekleyin."
       )
    class Meta:
        model = Pet
        fields = [
            'name', 'species', 'breed', 'age', 'gender',
            'description', 'last_seen_location', 'last_seen_date',
            'image', 'status', 'tags' ,'tags_text'
        ]
        widgets = {
            'last_seen_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_last_seen_date(self):
        last_seen_date = self.cleaned_data['last_seen_date']
        if last_seen_date and last_seen_date > datetime.date.today():
            raise forms.ValidationError("Son görülme tarihi gelecekte olamaz.")
        return last_seen_date
        
    
    def save(self, commit=True):
           pet = super().save(commit=False)
           if commit:
               pet.save()
               pet.tags.set(self.cleaned_data.get('tags'))  # Seçilen etiketleri ayarla
               tags_str = self.cleaned_data.get('tags_text', '')
               tags_names = [t.strip() for t in tags_str.split(',') if t.strip()]
               for tag_name in tags_names:
                   tag, created = Tag.objects.get_or_create(name=tag_name)
                   pet.tags.add(tag)
           return pet

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['message']
        labels = {
            'message': 'Mesaj',
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Etiket Adı',
        }
