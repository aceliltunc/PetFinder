from django import forms
from .models import Pet, AdoptionRequest, Tag, PetSighting,Message
from django.contrib.auth.models import User
import datetime
from django.forms import DateInput
class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

class AdminPetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'
        widgets = {
            'last_seen_date': forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}),
        }
class AdminTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class AdminPetSightingForm(forms.ModelForm):
    class Meta:
        model = PetSighting
        fields = '__all__'
        widgets = {
            'date_seen': forms.DateInput(attrs={'type': 'date'}),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AdminAdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = '__all__'
        widgets = {
            'request_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PetForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'id': 'id_tags', 'size': 8, 'class': 'select2'}),
        required=False,
        label="Etiketler",
        help_text="Mevcut etiketlerden seçin."
    )
    
    new_tags = forms.CharField(
        required=False,
        label="Yeni Etiketler",
        help_text="Virgül veya boşluk ile yeni etiketler yazın.",
        widget=forms.TextInput(attrs={'placeholder': 'Yeni etiketleri buraya yazın'})
    )

    class Meta:
        model = Pet
        fields = [
            'name', 'species', 'breed', 'age', 'gender',
            'description', 'last_seen_location', 'last_seen_date',
            'image', 'status', 'tags'
        ]
        widgets = {
            'last_seen_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_last_seen_date(self):
        last_seen_date = self.cleaned_data.get('last_seen_date')
        if last_seen_date and last_seen_date > datetime.date.today():
            raise forms.ValidationError("Son görülme tarihi gelecekte olamaz.")
        return last_seen_date

    def save(self, commit=True):
        pet = super().save(commit=False)
        if commit:
            pet.save()  # Önce kaydet ki pet.id oluşsun
            # ManyToMany işlemleri sadece pet kaydedildikten sonra yapılmalı
            selected_tags = self.cleaned_data.get('tags', [])
            new_tags_str = self.cleaned_data.get('new_tags', '')
            new_tag_names = [t.strip() for t in new_tags_str.replace(',', ' ').split() if t.strip()]
            new_tag_objs = []
            for name in new_tag_names:
                tag_obj, created = Tag.objects.get_or_create(name=name)
                new_tag_objs.append(tag_obj)
            all_tags = list(selected_tags) + new_tag_objs
            pet.tags.set(all_tags)
        else:
            # Eğer commit=False ise, ManyToMany ilişkisini bu aşamada atama
            # Çünkü pet henüz kaydedilmedi, id yok
            pass

        return pet



class PetSightingForm(forms.ModelForm):
    class Meta:
        model = PetSighting
        fields = ['location', 'date_seen', 'notes', 'contact_method', 'photo']
        widgets = {
            'date_seen': DateInput(
                attrs={'type': 'date'},  
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        self.pet = kwargs.pop('pet', None)
        self.user = kwargs.pop('reporter', None)
        super().__init__(*args, **kwargs)

        self.fields['date_seen'].input_formats = ['%Y-%m-%d'] 

        self.fields['contact_method'].required = True
        self.fields['date_seen'].required = True
        self.fields['location'].required = True

    def save(self, commit=True):
        sighting = super().save(commit=False)
        if self.pet:
            sighting.pet = self.pet
        if self.user:
            sighting.user = self.user
        if commit:
            sighting.save()
        return sighting




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

class UserSelectionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Kullanıcı Seçin")