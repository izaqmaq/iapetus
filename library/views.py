from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from library.models import *
import library.forms
import account.views
from library.mixins import AjaxTemplateMixin
from django.views.generic import DetailView, ListView, FormView 
from django.views.generic.list import MultipleObjectMixin
from django_searchbar.mixins import SearchBarViewMixin 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime


from django.utils.translation import ugettext_lazy as _


class LoginView(account.views.LoginView):
    form_class = account.forms.LoginEmailForm

class CatalogEntryList(SearchBarViewMixin, ListView):
    searchbar_fields = ['isbn']
    template_name = 'library/catalogentry_list.html'
    model = CatalogEntry
    context_object_name = "catalog_list"
    paginate_by = 7

    def get_queryset(self, **kwargs):
        return super(CatalogEntryList, self).get_queryset(**kwargs).all()
        
    def get_context_data(self, **kwargs):
        context = super(CatalogEntryList, self).get_context_data(**kwargs)
        context['no_of_entries'] = self.object_list.count()
        return context
		
class CategoryEntryList(SearchBarViewMixin, ListView):
    searchbar_fields = ['isbn']
    template_name = 'library/Categoryentry_list.html'
    model = CatalogEntry
    context_object_name = "Category_list"
    paginate_by = 6

    def get_queryset(self, **kwargs):
        return super(CategoryEntryList, self).get_queryset(**kwargs).filter(category__slug=self.kwargs['slug'])
        
    def get_context_data(self, **kwargs):
        context = super(CategoryEntryList, self).get_context_data(**kwargs)
        context['category'] = self.kwargs['slug']
        context['no_of_entries'] = self.object_list.count()
        return context
		
		

class CatalogEntryDetail(DetailView):
    template_name = 'library/catalogentry_detail.html'
    model = CatalogEntry

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CatalogEntryDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_copies'] = Book.objects.filter(catalog_entry__slug=self.kwargs['slug'])
        print(context['book_copies'] )
        return context


class BookList(SearchBarViewMixin, ListView):
    searchbar_fields = ['barcode']
    template_name = 'library/book_list.html'
    model = Book
    context_object_name = "book_list"
    paginate_by = 6

    def get_queryset(self, **kwargs):
        return super(BookList, self).get_queryset(**kwargs).order_by('-available', 'catalog_entry', 'copy_no')
        
    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['no_of_entries'] = self.object_list.count()
        return context

class LoanHistory(SearchBarViewMixin, ListView):
    searchbar_fields = ['barcode']
    template_name = 'library/loan_history.html'
    model = Loan
    context_object_name = "loan_history"

    def get_queryset(self, **kwargs):
        return super(LoanHistory, self).get_queryset(**kwargs).filter(book__barcode=self.kwargs['barcode']).order_by('-borrow_date', '-back_date')
        
    def get_context_data(self, **kwargs):
        context = super(LoanHistory, self).get_context_data(**kwargs)
        context['book'] = Book.objects.get(barcode=self.kwargs['barcode'])
        context['no_of_entries'] = self.object_list.count()
        return context

class PublisherList(ListView):
    template_name = 'library/publisher_list.html'
    model = Publisher
    context_object_name = 'my_favorite_publishers'
    paginate_by = 1



class PublisherDetail(DetailView):
    template_name = 'library/publisher_detail.html'
    model = Publisher
    context_object_name = 'my_publications'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PublisherDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print(self.kwargs['slug'], 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        context['centry_list'] = CatalogEntry.objects.filter(publisher__slug=self.kwargs['slug'])
        return context

class AuthorList(ListView):
    template_name = 'library/author_list.html'
    model = Author
    context_object_name = 'my_favorite_authors'
    paginate_by = 1



class AuthorDetail(DetailView):
    template_name = 'library/author_detail.html'
    model = Author
    context_object_name = 'my_writtings'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print(self.kwargs['slug'], 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        context['centry_list'] = CatalogEntry.objects.filter(author__slug=self.kwargs['slug'])
        return context
		
class BorrowView(FormView):
    form_class = library.forms.BorrowForm
    template_name = 'library/book_loan.html'
    success_url = None
    messages = {
        "book_borrowed": {
            "level": messages.WARNING,
            "text": _("Book successful borrowed.")
        },
    }
    
    def get_success_url(self):
        return reverse('book-list')
    
    def get_form_kwargs(self):
        kwargs = super(BorrowView, self).get_form_kwargs()
        kwargs['barcode'] = self.kwargs['barcode']
        return kwargs

    def get_form_class(self):
        # this only works with a FormView)
        self.bk = Book.objects.get(barcode=self.kwargs['barcode'])
        return super(BorrowView, self).get_form_class()
    
    def get_initial(self):
        initial = super(BorrowView, self).get_initial()
        return initial

    def get_context_data(self, **kwargs):
        context = super(BorrowView, self).get_context_data(**kwargs)
        context['book_info'] = Book.objects.get(barcode=self.kwargs['barcode'])
        context['borrowing'] = True
        return context
    
    def borrow_book(self, form):
        rdr = form.cleaned_data['reader']
        rd = form.cleaned_data['return_date']
        try:
            csn = rdr.classsession_set.all().first()
            loan = Loan.objects.create(student=rdr, book=self.bk, return_date=rd, class_session=csn)
        except:
            loan = Loan.objects.create(teacher=rdr, book=self.bk, return_date=rd)
            
        self.bk.available = False
        self.bk.save()
        if self.messages.get("book_borrowed"):
            messages.add_message(
                self.request,
                self.messages["book_borrowed"]["level"],
                self.messages["book_borrowed"]["text"]
            )

    def form_valid(self, form):
        self.borrow_book(form)
        return super(BorrowView, self).form_valid(form)

		
class ReturnView(FormView):
    form_class = library.forms.ReturnForm
    template_name = 'library/book_loan.html'
    success_url = None
    messages = {
        "book_returned": {
            "level": messages.SUCCESS,
            "text": _("Book successful returned.")
        },
    }
    
    def get_success_url(self):
        return reverse('book-list')
    
    def get_form_kwargs(self):
        kwargs = super(ReturnView, self).get_form_kwargs()
        kwargs['barcode'] = self.kwargs['barcode']
        return kwargs

    def get_form_class(self):
        self.bk = Book.objects.get(barcode=self.kwargs['barcode'])
        return super(ReturnView, self).get_form_class()
    
    def get_initial(self):
        initial = super(ReturnView, self).get_initial()
        self.ln = Loan.objects.filter(book=self.bk).exclude(back_date__isnull=False).first()
        if self.ln.student == None:
            initial['reader'] = self.ln.teacher.names
        else:
            initial['reader'] = self.ln.student.names
        initial['return_date'] = self.ln.return_date
        today = datetime.date.today()
        initial['overdue'] = (today - self.ln.return_date).days
        print(initial)
        return initial

    
    def get_context_data(self, **kwargs):
        context = super(ReturnView, self).get_context_data(**kwargs)
        context['book_info'] = Book.objects.get(barcode=self.kwargs['barcode'])
        context['returning'] = True
        return context
    
    def return_book(self, form):
        self.ln.back_date = timezone.now()
        self.ln.overdue = form.cleaned_data['overdue']
        self.ln.save()
        self.bk.available = True
        self.bk.save()
        if self.messages.get("book_returned"):
            messages.add_message(
                self.request,
                self.messages["book_returned"]["level"],
                self.messages["book_returned"]["text"]
            )

    def form_valid(self, form):
        self.return_book(form)
        return super(ReturnView, self).form_valid(form)

