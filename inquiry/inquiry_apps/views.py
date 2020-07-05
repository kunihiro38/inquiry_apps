import urllib.parse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.views.decorators.http import require_http_methods
from .forms import InquiryAddForm, InquiryFindForm, AddInquiryCommentForm
from .models import Inquiry, InquiryComment


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


def _paginator(request, qs):
    paginator = Paginator(qs, 5)
    page = request.GET.get('page', 1)

    try:
        inquiry_lists = paginator.page(page)
    except PageNotAnInteger:
        inquiry_lists = paginator.page(1)
    except EmptyPage:
        inquiry_lists = paginator.page(paginator.num_pages)
    return inquiry_lists



@require_http_methods(['GET'])
def comment_list(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    qs = InquiryComment.objects.filter(inquiry_id=inquiry_id).order_by('id').reverse()
    inquiry_comments = []
    for p in qs:
        inquiry_comments.append(p)
    
    inquiry_comments = _paginator(request, inquiry_comments)

    context = {
        'inquiry': inquiry,
        'inquiry_comments': inquiry_comments,
    }
    # html側でPICを表示できるように
    return render(request, 'inquiry_apps/comment_list.html', context)


@require_http_methods(['GET', 'POST'])
def comment_add(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    if request.method != 'POST':
        form = AddInquiryCommentForm()
    else:
        form = AddInquiryCommentForm(request.POST)
        if form.is_valid():
            inquiry_comment = InquiryComment(
                inquiry_id=inquiry_id,
                pic=form.cleaned_data['person_in_charge'],
                pic_email=form.cleaned_data['email'],
                inquiry_status=form.cleaned_data['inquiry_status'],
                comment=form.cleaned_data['comment'],
            )
            inquiry_comment.save()
            inquiry = Inquiry.objects.get(id=inquiry_id)
            inquiry.inquiry_status = form.cleaned_data['inquiry_status']
            inquiry.save()
            return HttpResponseRedirect(reverse('inquiry_apps:comment_add_success',
                                                args=(inquiry_id,)))

    context = {
        'inquiry': inquiry,
        'form': form,
    }
    template = loader.get_template('inquiry_apps/comment_add/comment_add.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/comment_add/comment_add.html', context)

def comment_add_success(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    # qs = InquiryComment.objects.order_by('updated_at').reverse()
    context = {
        'inquiry_id': inquiry_id,
        # 'comment_id': qs[0].id,
    }
    template = loader.get_template('inquiry_apps/comment_add/comment_add_success.html')
    return HttpResponse(template.render(context, request))


@require_http_methods(['GET', 'POST'])
def delete_comment(request, inquiry_id, comment_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    inquiry_comment = get_object_or_404(InquiryComment, id=comment_id)

    if inquiry.id != inquiry_comment.inquiry_id:
        raise Http404('No Inquiry matched the given query.')

    if request.method == 'POST':
        inquiry_comment.delete()
        return HttpResponseRedirect(reverse(
            'inquiry_apps:delete_comment_success',
            args=(inquiry_id,))
        )

    context = {
        'inquiry_comment': inquiry_comment 
    }
    template = loader.get_template('inquiry_apps/comment_delete/delete_comment.html')
    return HttpResponse(template.render(context, request))


@require_http_methods(['GET'])
def delete_comment_success(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    context = {
        'inquiry': inquiry,
    }

    return render(request, 'inquiry_apps/comment_delete/delete_comment_success.html', context)


@require_http_methods(['GET', 'POST'])
def edit_comment(request, inquiry_id, comment＿id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    inquiry_comment = get_object_or_404(InquiryComment, id=comment_id)
    if inquiry.id != inquiry_comment.inquiry_id:
        raise Http404('No Inquiry matched the given query')

    context = {
        'inquiry': inquiry,
    }

    return render(request, 'inquiry_apps/edit_comment/edit_comment.html', context)



