from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class CommonInfo(models.Model):
    TITLE_CHOICES = (
        ('MR', 'Mr.'),
        ('MRS', 'Mrs.'),
        ('MS', 'Miss.'),
    )
    idno = models.CharField(max_length=30, unique=True)
    names = models.CharField(max_length=200, help_text='First Middle Surname')
    title = models.CharField(max_length=3, blank=True, choices=TITLE_CHOICES)
    phone = models.CharField(max_length= 30, unique=True, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    class meta:
        abstract = True


class Teacher(CommonInfo):

    def __str__(self):
        return '%s %s' % (self.get_title_display(), self.names.split()[1])

class Parent(CommonInfo):

    def __str__(self):
        return self.names

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    RELIGION_CHOICES = (
        ('CHR', 'Christian'),
        ('MUS', 'Muslim'),
        ('HIN', 'Hindu')
    )
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    YEAR_IN_SCHOOL_CHOICES = (
        (ONE, 'One'),
        (TWO, 'Two'),
        (THREE, 'Three'),
        (FOUR, 'Four'),
        (FIVE, 'Five'),
        (SIX, 'Six'),
        (SEVEN, 'Seven'),
        (EIGHT, 'Eight'),
    )
    adm_no = models.IntegerField(unique=True)
    names = models.CharField(max_length=200, help_text='First Middle Surname')
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    religion = models.CharField(max_length=3, choices=RELIGION_CHOICES, default='CHR')
    join_date = models.DateField()
    year_in_school = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, default=ONE)
    parent = models.ForeignKey(Parent, blank=True)
    
    def is_upperclass(self):
        return self.year_in_school in (self.FOUR, self.FIVE, self.SIX, self.SEVEN, self.EIGHT)

    def __str__(self):
        return '%s %s' % (self.adm_no, self.names)



class AcademicSession(models.Model):
    TERM_CHOICES = (
        ('1st', 'First'),
        ('2nd', 'Second'),
        ('3rd', 'Third')
    )
    STATUS_CHOICES = (
        ('o', 'Current'),
        ('c', 'Closed')
    )
    term = models.CharField(max_length=3, choices=TERM_CHOICES, default='1st')  
    opening_date = models.DateField(null=True)
    closing_date = models.DateField(null=True)
    slug = models.SlugField(unique=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='o')
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify('%s %s %s' % (self.term, 'term', str(self.opening_date.year)))
        super(AcademicSession, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def __str__(self):
        return  self.get_term_display() + ' term ' + str(self.opening_date.year)
        
    class Meta:
        unique_together = ("term", "opening_date")
        ordering = ['-opening_date',]


class ClassLevel(models.Model):
    LEVEL_CHOICES = (
        ('S1', 'Standard 1'),
        ('S2', 'Standard 2'),
        ('S3', 'Standard 3'),
        ('S4', 'Standard 4'),
        ('S5', 'Standard 5'),
        ('S6', 'Standard 6'),
        ('S7', 'Standard 7'),
        ('S8', 'Standard 8')
    )
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    
    def __str__(self):
        return  self.get_level_display()
        
    def save(self):
        self.slug = slugify(self.level)
        super(ClassLevel, self).save()
        
    class Meta:
        ordering = ['level',]

class Classroom(models.Model):
    STREAM_CHOICES = (
        ('S', 'South'),
        ('E', 'East'),
        ('N', 'North'),
        ('W', 'West')
    )
    level = models.ForeignKey(ClassLevel)
    stream = models.CharField(max_length=1, choices=STREAM_CHOICES)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    #capacity = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify('%s %s' % (self.level, self.stream))#.replace('-', "")
        super(Classroom, self).save(*args, **kwargs) # Call the "real" save() method., related_name="classrooms", to_field="level"
        
    def __str__(self):
        return '%s %s' % (self.level, self.stream)

class ClassSession(models.Model):
    academic_session = models.ForeignKey(AcademicSession)
    classroom = models.ForeignKey(Classroom)
    students = models.ManyToManyField(Student, blank=True)
    teacher = models.ForeignKey(Teacher, null=True, blank=True)
    slug = models.SlugField(unique=True, help_text='do not fill!', editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify('%s %s' % (self.classroom, self.academic_session.slug))
        super(ClassSession, self).save(*args, **kwargs) # Call the "real" save() method.

    def __str__(self):
        return '%s %s' % (self.classroom, self.academic_session)
        
    ordering = ['-academic_session',]



