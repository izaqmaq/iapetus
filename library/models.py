from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from school.models import Student, ClassSession, Teacher

class Author(models.Model):
    names = models.CharField(max_length=200)
    credits = models.TextField()
    memo = models.TextField()
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.names)
        super(Author, self).save() 

    def __str__(self):
        return self.names


class Publisher(models.Model):
    names = models.CharField(max_length=300)
    contacts = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.names)
        super(Publisher, self).save()

    def __str__(self):
        return self.names


class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.name)
        super(Category, self).save()

    def __str__(self):
        return self.name


class CatalogEntry(models.Model):
    isbn = models.CharField(max_length=13, unique = True)
    title = models.CharField(max_length=300)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author)
    category = models.ForeignKey(Category)
    copies = models.IntegerField()
    date_published = models.DateField()
    sales_contacts = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.title)
        super(CatalogEntry, self).save()

    def __str__(self):
        return '%s %s' % (self.title, self.isbn)
    

class Book(models.Model):
    catalog_entry = models.ForeignKey(CatalogEntry)
    copy_no = models.IntegerField()
    barcode = models.CharField(max_length=13, unique = True)
    available = models.BooleanField(default=True)
    date_in = models.DateField(default=timezone.now(), editable=False)
    lost = models.BooleanField(default=False)
    replaced = models.NullBooleanField(editable=False)
    
    def __str__(self):
        return '%s %s' % (self.catalog_entry, self.barcode)

class Loan(models.Model):
    student = models.ForeignKey(Student, models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book)
    borrow_date = models.DateField(default=timezone.now(), editable=False)
    return_date = models.DateField()
    back_date = models.DateField(null=True, blank=True)
    overdue = models.IntegerField(default=0)
    class_session = models.ForeignKey(ClassSession, null=True, blank=True)
    
    def __str__(self):
        return '%s %s' % (self.student, self.book)
		
	#def save(self):
		

    
