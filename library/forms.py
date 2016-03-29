from django import forms
import datetime
from django.forms import fields
from django.forms.extras.widgets import SelectDateWidget
from library.models import Book, Student, Loan, Author, Teacher

from django.utils.translation import ugettext_lazy as _ 


class BorrowForm(forms.Form):
    reader = forms.ChoiceField(label=('Reader'), choices=[], required=False)
    return_date = forms.DateField(label=('Return date'), required=True, widget=forms.TextInput(attrs={'class': 'datepicker'}))

    def __init__(self, *args, **kwargs):
        self.barcode = kwargs.pop('barcode', None)
        super(BorrowForm, self).__init__(*args, **kwargs)
        self.bk = Book.objects.get(barcode=self.barcode)
        choices = []
        for obj1 in Student.objects.all():
            choices.append((obj1.adm_no, obj1.names))
        for obj2 in Teacher.objects.all():
            choices.append((obj2.idno, obj2.names))
        self.fields['reader'].choices = choices
    
    
    def clean_reader(self):
            try:
                    reader = Student.objects.get(adm_no=self.cleaned_data['reader'])
                    loan = Loan.objects.filter(student=reader).filter(back_date__isnull=True)
            except:
                    reader = Teacher.objects.get(idno=self.cleaned_data['reader'])
                    loan = Loan.objects.filter(teacher=reader).filter(back_date__isnull=True)
            if not loan.exists():
                    return reader
            elif loan.count()>=4:
                    raise forms.ValidationError(_("The reader has already borrowed maximum allowed!"))
            else:
                    return reader
    
    def clean_return_date(self):
            return_date = self.cleaned_data['return_date']
            if return_date < datetime.date.today():
                    raise forms.ValidationError(_("This is an earlier date!"))
            return return_date
                    

                    
class ReturnForm(forms.Form):
    reader = forms.CharField(label=('Reader'), required=True)
    return_date = forms.DateField(label=('Return date'), required=True)
    overdue = forms.IntegerField(label=('Overdue'), required=False)

    def __init__(self, *args, **kwargs):
        self.barcode = kwargs.pop('barcode', None)
        super(ReturnForm, self).__init__(*args, **kwargs)
        self.bk = Book.objects.get(barcode=self.barcode)