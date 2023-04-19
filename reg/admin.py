from django.contrib import admin
from .models import *
class CustomAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','role','is_staff') 

class CustomApplicant(admin.ModelAdmin):
    list_display = ('id','fk_user','firstname','lastname','gender','dob','phone','address','workstatus')

class CustomEducation(admin.ModelAdmin):
    list_display=('id','fk_user','level','school_or_university','course')

class CustomCompany(admin.ModelAdmin):
    list_display=('id','fk_company','company_name','logo','description','location','phone_number','website','industry')

class CustomExperience(admin.ModelAdmin):
    list_display=('id','fk_user','current_company_name','location','doj','dol','current_salary','notice_period')

class CustomKeyskills(admin.ModelAdmin):
    list_display=('id','fk_user','key_skills')

class CustomLanguages(admin.ModelAdmin):
    list_display=('id','fk_user','languages','proficiency')

class CustomJobadd(admin.ModelAdmin):
    list_display=('id','fk_company_pro','job_title','job_type','industry','location','job_fields','vacancy','salary','education_requirements','experience_requirements')

class CustomApplication(admin.ModelAdmin):
    list_display=('id','fk_user_pro','fk_company_job',)

class CustomResume(admin.ModelAdmin):
    list_display=('id','fk_user','resume')

class CustomProjects(admin.ModelAdmin):
    list_display=('id','fk_user','project_name','project_description','project_link')

class CustomCareerObj(admin.ModelAdmin):
    list_display=('id','fk_user','career_obj')




admin.site.register(CustomUser,CustomAdmin)
admin.site.register(ApplicantProfile,CustomApplicant)
admin.site.register(Education,CustomEducation)
admin.site.register(CompanyProfile,CustomCompany)
admin.site.register(Experience,CustomExperience)
admin.site.register(KeySkills,CustomKeyskills)
admin.site.register(Languages,CustomLanguages)
admin.site.register(JobAdd,CustomJobadd)
admin.site.register(Application,CustomApplication)
admin.site.register(CareerObj,CustomCareerObj)
admin.site.register(Resume,CustomResume)
admin.site.register(Projects,CustomProjects)
admin.site.register(CompanyAuth)
admin.site.register(ApplicantAuth)
admin.site.register(ContactUs)
