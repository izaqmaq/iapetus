from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from library import views
from django.views.decorators.http import require_http_methods, require_POST
urlpatterns = patterns('',
    # Examples:studentresults
    # url(r'^$', 'management.views.home', name='home'),

	
    url(r'^category/entry/(?P<slug>[-\w]+)/$', views.CategoryEntryList.as_view(), name='category'),
	
    url(r'^catalog/entries/$', views.CatalogEntryList.as_view(), name='catalog'),
    url(r'^entry/(?P<slug>[-\w]+)/$', views.CatalogEntryDetail.as_view(), name='catalogentry-detail'),
	
    url(r'^books/$', views.BookList.as_view(), name='book-list'),
    url(r'^book/(?P<barcode>\d+)/borrowing/$', views.BorrowView.as_view(), name='borrow-book'),
    url(r'^book/(?P<barcode>\d+)/returning/$', views.ReturnView.as_view(), name='return-book'),
	
    url(r'^book/(?P<barcode>\d+)/loan/history/$', views.LoanHistory.as_view(), name='loan-history'),

    url(r'^authors/$', views.AuthorList.as_view(), name = 'author-list'),
    url(r'^author/(?P<slug>[-\w]+)/$', views.AuthorDetail.as_view(), name='author-detail'),

    url(r'^publishers/$', views.PublisherList.as_view(), name = 'publisher-list'),
    url(r'^publisher/(?P<slug>[-\w]+)/$', views.PublisherDetail.as_view(), name='publisher-detail'),
	
)

