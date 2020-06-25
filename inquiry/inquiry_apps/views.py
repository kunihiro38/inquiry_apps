import urllib.parse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.views.decorators.http import require_http_methods
from .forms import InquiryAddForm, InquiryFindForm, CommentAddForm
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
            'message': '',
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
            # inquiry.save()
            # return render(request, 'inquiry_apps/inquiry_add/inquiry_add_success.html')
            return HttpResponseRedirect(reverse('inquiry_apps:inquiry_add_success'))
            
    template = loader.get_template('inquiry_apps/inquiry_add/inquiry_add.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/inquiry_add/inquiry_add.html')

@require_http_methods(['GET'])
def inquiry_add_success(request):
    qs = Inquiry.objects.order_by('created_at').reverse()
    context = {
        'posted_inquiry_id': qs[0].id,
    }
    return render(request, 'inquiry_apps/inquiry_add/inquiry_add_success.html', context)



def _some_page_href(id, email, current_page, word):
    params = []
    if id:
        params.append('id=%s' % urllib.parse.quote(str(id)))
    if email:
        params.append('email=%s' % urllib.parse.quote(email))
    if current_page:
        params.append('page=%s' % urllib.parse.quote(str(current_page)))
    if word:
        params.append('word=%s' % urllib.parse.quote(word))
    return '?' + '&'.join(params)


@require_http_methods(['GET'])
def inquiry_list(request):
    qs = Inquiry.objects.order_by('-updated_at')
    form = InquiryFindForm(request.GET)
    if not form.is_valid():
        return render(request, 'inquiry_apps/inquiry_list.html', {'form': form})

    if form.is_valid():
        id_int = form.cleaned_data['id']
        email_str = form.cleaned_data['email']
        page_int = form.cleaned_data['page']
        word_str = form.cleaned_data['word']

    if email_str is not None:
        qs = qs.filter(email__contains=email_str)

    if id_int is not None:
        qs = qs.filter(id=id_int)

    if word_str is not None:
        qs = qs.filter(Q(subject__contains=word_str) |
                        Q(message__contains=word_str))

    # making next page parameter
    next_page_href = _some_page_href(id_int, email_str, page_int+1, word_str)
    # making prev page parameter
    prev_page_href = _some_page_href(id_int, email_str, page_int-1, word_str)

    paginator = Paginator(qs, 5)
    try:
        inquiries_page = paginator.page(page_int)
    except EmptyPage:
        raise Http404('Page does not exist')


    context = {
        'form': form,
        'inquiries_page': inquiries_page,
        'search_email': email_str,
        'next_page_href': next_page_href,
        'prev_page_href': prev_page_href,
    }

    template = loader.get_template('inquiry_apps/inquiry_list.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/inquiry_list.html', context)

@require_http_methods(['GET'])
def comment_list(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    context = {
        'inquiry': inquiry,
    }
    return render(request, 'inquiry_apps/comment_list.html', context)


@require_http_methods(['GET'])
def comment_add(request, inquiry_id):
    if request.method == 'GET':
        inquiry = get_object_or_404(Inquiry, id=inquiry_id)
        form = CommentAddForm()

    else:
        form = CommentAddForm(request.POST)
        if form.is_valid():
            inquiry_comment = InquiryComment(
                person_in_charge=form.cleaned_data['person_in_charge'],
                email=form.cleaned_data['email'],
                comment=form.cleaned_data['comment'],
            )
            # inquiry_comment.save()
            return HttpResponseRedirect(reverse('inquiry_apps:comment_add_success'))

    context = {
        'inquiry': inquiry,
        'form': form,
    }
    template = loader.get_template('inquiry_apps/comment_add/comment_add.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/comment_add/comment_add.html', context)