from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ProjectElement, Material, QuotationRequest
from .forms import QuotationRequestForm
from django.contrib.auth.decorators import login_required
import logging
from .forms import ProjectElementForm, MaterialForm

logger = logging.getLogger(__name__)
@login_required
def add_project_element(request):
    if request.method == 'POST':
        form = ProjectElementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_project_materials_and_elements')  # Redirect after successful submission
    else:
        form = ProjectElementForm()
    return render(request, 'add_project_element.html', {'form': form})

@login_required
def add_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_project_materials_and_elements')  # Redirect after successful submission
    else:
        form = MaterialForm()
    return render(request, 'add_material.html', {'form': form})
@login_required
def all_project_materials_and_elements(request):
    # Prefetch related materials for each project element
    elements = ProjectElement.objects.prefetch_related('materials').all()
    return render(request, 'all_project_materials_and_elements.html', {'elements': elements})


@login_required
def list_of_my_quotes(request):
    # Retrieve all quotations requested by the logged-in user
    user_quotes = QuotationRequest.objects.filter(user=request.user)
    return render(request, 'homepage.html', {'user_quotes': user_quotes})



@login_required
def quotation_request(request):
    if request.method == 'POST':
        form = QuotationRequestForm(request.POST)
        if form.is_valid():
            element = form.cleaned_data['element']
            material = form.cleaned_data['material'] if 'material' in form.cleaned_data else None

            QuotationRequest.objects.create(
                user=request.user,
                project_element=element,
                material=material,
                status="Pending"
            )
            return redirect('homepage')
    else:
        form = QuotationRequestForm()

    elements = ProjectElement.objects.prefetch_related('materials').all()
    return render(request, 'quotation_request.html', {'form': form, 'project_elements': elements})

def load_materials(request):
    element_id = request.GET.get('element_id')
    materials = Material.objects.filter(project_element_id=element_id)
    return JsonResponse(list(materials.values('id', 'name')), safe=False)

def quotation_success(request):
    return render(request, 'quotation_success.html')
