from django.contrib import admin
from library.models import *


#admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Category)

admin.site.register(Author)
admin.site.register(CatalogEntry)


class ClassInline(admin.StackedInline):
    model = ClassSession
    #fields = ('name', 'description')
    #prepopulated_fields = {'slug': ('name',)}
    extra = 0

class LoanInline(admin.TabularInline):
    model = Loan
    fields = ('student', 'teacher', 'book', 'back_date')
    #prepopulated_fields = {'slug': ('name',)}
    extra = 0


class BookAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'slug': ('name',)}
    #exclude = ('slug',), ClassInline
    inlines = [LoanInline]

    list_display = ('catalog_entry', 'copy_no', 'barcode', 'available')

    list_filter = ['catalog_entry' ]

    search_fields = ['barcode']
 
admin.site.register(Book, BookAdmin)


class LoanAdmin(admin.ModelAdmin):
	list_display = ('student', 'teacher', 'book', 'back_date')
	list_filter = ['class_session']
	search_fields = ['book']

admin.site.register(Loan, LoanAdmin)