import urllib.parse
import datetime
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.views.decorators.http import require_http_methods
from .forms import InquiryAddForm, InquiryFindForm, AddInquiryCommentForm, EditInquiryCommentForm, LoginForm, EditProfileForm, AddUserForm
from .models import Inquiry, InquiryComment

# login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



@require_http_methods(['GET', 'POST'])
def inquiry_login(request):
    # user = User.objects.create_user('test_user', 'test@example.com', 'testuser')
    
    if request.method != 'POST':
        if str(request.user) != 'AnonymousUser':
            form = ''
        else:
            form = LoginForm()
    
    else:

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('inquiry_apps:inquiry_list'))
            else:
                pass
    context = {
        'form': form,
    }
    return render(request, 'inquiry_apps/login.html', context)



def inquiry_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('inquiry_apps:index'))


@require_http_methods(['GET'])
def index(request):
    print(User.objects.all())
    
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


@require_http_methods(['GET', 'POST'])
def user_add(request):
    # if request.method != 'POST':
    #     form = AddUserForm()
    # else:
    #     form = AddUserForm(request.POST)
    #     if form.is_valid():
    #         user = User.objects.create_user(
    #             username=form.cleaned_data['username'],
    #             email=form.cleaned_data['email'],
    #             password=form.cleaned_data['password']
    #         )
    
    # context = {
    #     'form' : form
    # }
    # template = loader.get_template('inquiry_apps/user_add//user_add.html')
    # return HttpResponse(template.render(context, request))

    form = AddUserForm()
    return render(request, 'inquiry_apps/user_add/user_add.html', context={'form': form})




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



@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET', 'POST'])
def edit_profile(request):
    user = User.objects.get(id=request.user.id)
    
    if request.method != 'POST':
        form = EditProfileForm(
            initial={
                'username': user.username,
                'email': user.email,
            }
        )
    else:
        form = EditProfileForm(data=request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.save()

    
    context = {
        'form': form,
    }
    template = loader.get_template('inquiry_apps/edit_profile/edit_profile.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/edit_profile/edit_profile.html')


@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET', 'POST'])
def edit_name(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user,
        # 'form': form,
    }
    template = loader.get_template('inquiry_apps/edit_profile/edit_name.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/edit_profile/edit_name.html')



@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET', 'POST'])
def edit_email(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user,
    }
    template = loader.get_template('inquiry_apps/edit_profile/edit_email.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/edit_email.html')


@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET', 'POST'])
def edit_password(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user,
    }
    template = loader.get_template('inquiry_apps/edit_profile/edit_password.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/edit_password.html')


@login_required(login_url='/inquiry/login/')
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

@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET'])
def inquiry_list_ajax(request):
    return render(request, 'inquiry_apps/inquiry_list_ajax/inquiry_list_ajax.html')

@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET'])
def inquiry_list_ajax_response(request):
    qs = Inquiry.objects.order_by('updated_at').reverse()
    form = InquiryFindForm(request.GET)
    if form.is_valid():
        id_int = form.cleaned_data['id']
        email_str = form.cleaned_data['email']
        page_int = form.cleaned_data['page']
        word_str = form.cleaned_data['word']

    if email_str != None and email_str != '':
        qs = qs.filter(email__contains=email_str)

    if id_int is not None:
        qs = qs.filter(id=id_int)

    if word_str is not None:
        qs = qs.filter(message__contains=word_str)
    
    paginator = Paginator(qs, 5)
    try:
        inquiries_page = paginator.page(page_int)
    except:
        raise Http404('Page does not exist')
    
    context = {
        'inquiries_page': inquiries_page,
    }
    template = loader.get_template('inquiry_apps/inquiry_list_ajax/inquiry_list_ajax_response.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'inquiry_apps/inquiry_list_ajax/inquiry_list_ajax_response.html', context)

@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET'])
def comment_list(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    
    comment_list = []
    qs = InquiryComment.objects.filter(inquiry_id=inquiry_id).order_by('id').reverse()

    for inquiry_comment in qs:
        user = User.objects.get(id=inquiry_comment.user_id)
        inquiry_comment_dict = {
            'id': inquiry_comment.id,
            'user_id': inquiry_comment.user_id,
            'user': user.username,
            'email': user.email,
            'updated_at': inquiry_comment.updated_at,
            'comment': inquiry_comment.comment,
            'inquiry_status': inquiry_comment.inquiry_status_as_str(),
        }
        comment_list.append(inquiry_comment_dict)
    
    comment_list = _paginator(request, comment_list)

    context = {
        'inquiry': inquiry,
        'comment_list': comment_list,
    }
    # html側でPICを表示できるように
    return render(request, 'inquiry_apps/comment_list.html', context)


@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET', 'POST'])
def comment_add(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    request_data = User.objects.get(username=request.user)
    
    if request.method != 'POST':
        form = AddInquiryCommentForm()
    else:
        form = AddInquiryCommentForm(request.POST)
        if form.is_valid():
            inquiry_comment = InquiryComment(
                inquiry_id=inquiry_id,
                user_id=request_data.id,
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

@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET'])
def comment_add_success(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    # qs = InquiryComment.objects.order_by('updated_at').reverse()
    context = {
        'inquiry_id': inquiry_id,
        # 'comment_id': qs[0].id,
    }
    template = loader.get_template('inquiry_apps/comment_add/comment_add_success.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/inquiry/login/')
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


@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET'])
def delete_comment_success(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    context = {
        'inquiry': inquiry,
    }

    return render(request, 'inquiry_apps/comment_delete/delete_comment_success.html', context)

@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET', 'POST'])
def edit_comment(request, inquiry_id, comment＿id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    inquiry_comment = get_object_or_404(InquiryComment, id=comment_id)
    if inquiry.id != inquiry_comment.inquiry_id:
        raise Http404('No Inquiry matched the given query')

    if request.method != 'POST':
        item = {
            'inquiry_status': inquiry_comment.inquiry_status,
            'comment': inquiry_comment.comment,
        }
        form = EditInquiryCommentForm(
            inquiry_id=inquiry.id,
            comment_id=inquiry_comment.id,
            initial=item)


    else:
        form = EditInquiryCommentForm(
            inquiry_id=inquiry_id,
            comment_id=comment_id,
            data=request.POST)
        if form.is_valid():
            inquiry_comment = InquiryComment.objects.get(id=comment_id)
            inquiry_comment.inquiry_status = form.cleaned_data['inquiry_status']
            inquiry_comment.comment = form.cleaned_data['comment']

            inquiry_comment.save()


            inquiry.inquiry_status = form.cleaned_data['inquiry_status']
            inquiry.save()
            return HttpResponseRedirect(reverse(
                'inquiry_apps:edit_comment_success', args=(inquiry_id, comment_id,)))


    context = {
        'form': form,
        'inquiry': inquiry,
        'inquiry_comment': inquiry_comment,
    }

    return render(request, 'inquiry_apps/edit_comment/edit_comment.html', context)

@login_required(login_url='/inquiry/login/')
@require_http_methods(['GET'])
def edit_comment_success(request, inquiry_id, comment_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    context = {
        'inquiry': inquiry,
    }
    return render(request, 'inquiry_apps/edit_comment/edit_comment_success.html', context)
