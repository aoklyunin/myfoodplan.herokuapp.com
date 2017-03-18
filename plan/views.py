# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def generateWorkReport(request,work_repor_id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
   # p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    #p.showPage()
    # p.save()
    return response



'''def detailEquipment(request, equipment_id):
    EquipmentFormset = formset_factory(MoveEquipmentForm)
    MaterialFormset = formset_factory(MoveMaterialForm)
    DetailFormset = formset_factory(MoveDetailForm)
    AssemblyFormset = formset_factory(MoveAssemblyForm)
    StandartWorkFormset = formset_factory(MoveStandartWorkForm)

    eq = Equipment.objects.get(pk=equipment_id)

    if request.method == 'POST':
        equipment_formset = EquipmentFormset(request.POST, request.FILES, prefix='equipment')
        material_formset = MaterialFormset(request.POST, request.FILES, prefix='material')
        detail_formset = DetailFormset(request.POST, request.FILES, prefix='detail')
        assembly_formset = AssemblyFormset(request.POST, request.FILES, prefix='assembly')

        swork_formset = StandartWorkFormset(request.POST, request.FILES, prefix='standart_work')

        eq.addFromFormset(equipment_formset, True)
        eq.addFromFormset(material_formset)
        eq.addFromFormset(detail_formset)
        eq.addFromFormset(assembly_formset)
        eq.addFromFormset(swork_formset)

        # строим форму на основе запроса
        form = EquipmentForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = subdict(form, ("name", "dimension", "code", "needVIK"))
            Equipment.objects.filter(pk=equipment_id).update(**d)
            Equipment.objects.get(pk=equipment_id).scheme.clear()
            for e in form.cleaned_data["scheme"]:
                Equipment.objects.get(pk=equipment_id).scheme.add(
                    Scheme.objects.get(name=e)
                )
        return HttpResponseRedirect('/constructors/list/equipment/' + str(eq.equipmentType) + '/0/')

    c = {'equipment_formset': EquipmentFormset(initial=eq.generateDataFromNeedStructs(
        NeedEquipmentType=Equipment.TYPE_EQUIPMENT), prefix='equipment', ),
        'material_formset': MaterialFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_MATERIAL), prefix='material'),
        'detail_formset': DetailFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_DETAIL), prefix='detail', ),
        'assembly_formset': AssemblyFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_ASSEMBLY_UNIT), prefix='assembly', ),
        'swork_formset': StandartWorkFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_STANDART_WORK), prefix='standart_work', ),
        'login_form': LoginForm(),
        'one': '1',
        'form': EquipmentForm(instance=Equipment.objects.get(pk=equipment_id), prefix="main_form"),
        'eqType':eq.equipmentType,
    }

    return render(request, "constructors/detail.html", c)'''
