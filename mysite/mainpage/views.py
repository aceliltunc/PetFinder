from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Pet, AdoptionRequest, PetSighting
from .forms import PetForm, AdoptionRequestForm,PetSightingForm
from django.db.models import Q

def pet_search(request):
    query_name = request.GET.get('name', '')
    query_species = request.GET.get('species', '')
    query_age = request.GET.get('age', '')

    pets = Pet.objects.filter(status='Lost')

    if query_name:
        pets = pets.filter(name__icontains=query_name)
    if query_species:
        pets = pets.filter(species__icontains=query_species)
    if query_age:
        pets = pets.filter(age=query_age)

    return render(request, 'mainpage/pet_search.html', {
        'pets': pets,
        'name': query_name,
        'species': query_species,
        'age': query_age,
    })

# Tüm kayıp hayvan ilanlarını listele
def pet_list(request):
    pets = Pet.objects.filter(status='Lost').order_by('-date_reported')
    return render(request, 'mainpage/pet_list.html', {'pets': pets})

# Detay sayfası
@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    # Sadece sahibi görsün
    sightings = pet.sightings.all().order_by('-date_seen') if request.user == pet.owner else None

    return render(request, 'mainpage/pet_detail.html', {
        'pet': pet,
        'sightings': sightings,
    })

# Yeni kayıp bildirimi oluştur
@login_required
def pet_report(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()          # Önce kaydet
            form.save_m2m()     # Sonra ManyToMany ilişkileri kaydet
            return redirect('mainpage:pet_detail', pk=pet.pk)
    else:
        form = PetForm()
    return render(request, 'mainpage/pet_form.html', {'form': form})


# Güncelleme
@login_required
def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('mainpage:pet_detail', pk=pk)
    else:
        form = PetForm(instance=pet)
    return render(request, 'mainpage/pet_form.html', {'form': form})

# Silme
@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        return redirect('mainpage:pet_list')
    return render(request, 'mainpage/pet_confirm_delete.html', {'pet': pet})

import csv
from io import TextIOWrapper
from .forms import CSVImportForm

@login_required
def import_pets(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='windows-1254')
            reader = csv.DictReader(csv_file)

            for row in reader:
                Pet.objects.create(
                    name=row['name'],
                    species=row['species'],
                    breed=row['breed'],
                    age=int(row['age']),
                    gender=row['gender'],
                    description=row['description'],
                    status=row['status'],
                    owner=request.user,
                    # image alanı göz ardı ediliyor
                )
            return redirect('mainpage:pet_list')
    else:
        form = CSVImportForm()
    return render(request, 'mainpage/import_pets.html', {'form': form})


from django.http import HttpResponse

@login_required
def export_pets(request):
    pets = Pet.objects.filter(owner=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_pets.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'species', 'breed', 'age', 'gender', 'description', 'status'])

    for pet in pets:
        writer.writerow([
            pet.name,
            pet.species,
            pet.breed,
            pet.age,
            pet.gender,
            pet.description,
            pet.status,
        ])

    return response
#Kayıp hayvanı gördüm bildirimi
@login_required
def report_pet_sighting(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = PetSightingForm(request.POST, request.FILES, pet=pet, reporter=request.user)
        if form.is_valid():
            form.save()
            return redirect('mainpage:pet_detail', pk=pet_id)
        else:
            print(form.errors)  # Hataları görmek için
    else:
        form = PetSightingForm(pet=pet, reporter=request.user)

    return render(request, 'mainpage/report_sighting.html', {'form': form, 'pet': pet})






