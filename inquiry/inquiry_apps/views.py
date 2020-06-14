from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
from .forms import InquiryAddForm
from .models import Inquiry

@require_http_methods(['GET'])
def index(request):
    return render(request, 'inquiry_apps/index.html')


@require_http_methods(['GET', 'POST'])
def inquiry_add(request):
    if request.method == 'GET':
        items = {
            'name': '',
            'email': '',
            'subject': '',
            'message': 'input some words',
        }
        context = {
            'form': InquiryAddForm(initial=items),
        }
    
    else:
        # POST
        form = InquiryAddForm(request.POST)
        if form.is_valid():
            inquiry = Inquiry(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            inquiry.save()
            return render(request, 'inquiry_apps/inquiry_add/inquiry_add_success.html')
            
    template = loader.get_template('inquiry_apps/inquiry_add/inquiry_add.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/inquiry_add/inquiry_add.html')

@require_http_methods(['GET'])
def inquiry_add_success(request):
    return render(request, 'inquiry_apps/inquiry/inquiry_add/inquiry_add_success.html')

@require_http_methods(['GET'])
def inquiry_list(request):
    qs = Inquiry.objects.order_by('-updated_at')
    
    ここから再会
    form = InquiryFindForm(request.GET)

    if form.is_valid():



    context = {
        'inquiries_page': qs,
    }
    template = loader.get_template('inquiry_apps/inquiry_list.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/inquiry_list.html', context)