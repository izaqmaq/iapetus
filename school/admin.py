from django.contrib import admin
from school.models import *

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(AcademicSession)
admin.site.register(ClassSession)
admin.site.register(ClassLevel)
admin.site.register(Classroom)

