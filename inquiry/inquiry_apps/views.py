from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
from .forms import InquiryAddForm

@require_http_methods(['GET'])
def index(request):
    return render(request, 'inquiry_apps/index.html')


@require_http_methods(['GET', 'POST'])
def inquiry_add(request):
    if request.method == 'GET':
        template = loader.get_template('inquiry_apps/inquiry_add/inquiry_add.html')
        form = InquiryAddForm()
        context = {
            'form': form,
        }
        return HttpResponse(template.render(context, request))
        # return render(request, 'inquiry_apps/inquiry_add/inquiry_add.html')

# @require_http_methods(['GET'])
# def inquiry_add_success(request):
#     return 
