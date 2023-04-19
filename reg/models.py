from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, username=None, password=None,*args,**kwargs):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")
        user= self.model(
            username=username,
            *args,
            **kwargs)
        user.set_password(password)
        user.is_active=True
        user.save()
        return user

    def create_superuser(self, username, password,email):
        user = self.create_user(
            username=username,
            password=password,
            email=email,
            role=1, 
            is_staff=True,
        )
        user.is_superuser = True
        user.save()
        return user

ROLE_CHOICES = [
    (1, 'Admin'),
    (2, 'Company'),
    (3, 'Applicant')
]

class CustomUser(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def _str_(self):
        return self.username


# Applicant Details
class ApplicantProfile(models.Model):

    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHERS', 'Others'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    ]

    WORK_STATUS_CHOICES = [
        ('Experienced', 'I have work experience'),
        ('Fresher', 'I am a fresher'),
    ]

    fk_user=models.OneToOneField(CustomUser,on_delete=models.CASCADE) 
    photo=models.ImageField(upload_to='Profile_Photo/')
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    gender=models.CharField( max_length=50,choices=GENDER_CHOICES)
    marital_status=models.CharField(max_length=50,choices=MARITAL_STATUS_CHOICES)
    dob=models.DateField()
    address=models.TextField()
    phone=models.CharField(max_length=12)
    workstatus=models.CharField(max_length=100,choices=WORK_STATUS_CHOICES)
    # career_obj=models.TextField()
    jobrole=models.CharField(max_length=100)
    # resume=models.FileField(upload_to='Applicant_Resume/')
    # projects=models.CharField(max_length=150)


class Resume(models.Model):
    fk_user=models.OneToOneField(CustomUser,on_delete=models.CASCADE) 
    resume=models.FileField(upload_to='Resume/')

class Projects(models.Model):
    fk_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_name=models.CharField(max_length=100)
    project_description=models.TextField()
    project_link=models.URLField()

class CareerObj(models.Model):
    fk_user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    career_obj=models.TextField()



class Education(models.Model):
    LEVEL_CHOICES = (
        ('HighSchool', 'High School'),
        ('HigherSecondarySchool', 'Higher Secondary'),
        ('Graduation/Diploma', 'Graduation/Diploma'),
        ('PostGraduation', 'Post Graduation'),
        ('PhD', 'PhD'),
    )
    fk_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES)
    school_or_university = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    additional_details = models.TextField()


class ApplicantAuth(models.Model):
    fk_user_auth=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fk_user_auth.username


#company details

class CompanyAuth(models.Model):
    fk_company_auth=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fk_company_auth.username

class CompanyProfile(models.Model):
    fk_company=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='Company_Logos/')
    description = models.TextField(null=True)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    website = models.URLField()
    industry = models.CharField(max_length=100)
    company_status=models.BooleanField(default=False) #change

class KeySkills(models.Model):
    fk_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    key_skills=models.CharField(max_length=100)

class Languages(models.Model):
    PROFICIENCY=(
        ('BEGINNER','BEGINNER'),
        ('PROFICIENT','PROFICIENT'),
        ('EXPERT','EXPERT'),
    )
    fk_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    languages=models.CharField(max_length=100)
    proficiency=models.CharField(max_length=100,choices=PROFICIENCY)
    read=models.BooleanField(default=False,null=True)
    write=models.BooleanField(default=False,null=True)
    speak=models.BooleanField(default=False,null=True)


class Experience(models.Model):
    PERIOD=(
        ('15_Days_and_less','15_Days_and_less'),
        ('1Month','1Month'),
        ('2Month','2Month'),
        ('3Month','3Month'),
        ('MoreThan3Month','MoreThan3Month'),
        ('ServingNoticePeriod','ServingNoticePeriod'),
    )
    fk_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_this_current_emp=models.BooleanField(default=False,null=True)
    current_company_name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    doj=models.DateField()
    current_salary=models.PositiveIntegerField()
    job_profile=models.TextField()
    notice_period=models.CharField(max_length=50,choices=PERIOD)
    dol=models.DateField()

class JobAdd(models.Model):
    JOBTYPE=(
        ('Full_Time','Fulltime'),
        ('Part_time','Part_time'),
        ('Contract','Contract'),
        ('Internship','Internship'),
    )
    fk_company_pro=models.ForeignKey(CompanyProfile, on_delete=models.CASCADE) #companyprofile FK_company
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    job_type = models.CharField(max_length=100,choices=JOBTYPE)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_fields=models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    education_requirements = models.CharField(max_length=100)
    experience_requirements = models.CharField(max_length=100)
    skills_and_qualifications = models.TextField()
    application_deadline = models.DateTimeField()
    filled=models.BooleanField(default=False)
    vacancy=models.IntegerField(default=1)
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)
    # company_name = models.CharField(max_length=100)
    # company_description = models.TextField()

class Application(models.Model):
    fk_user_pro=models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE)# employee
    fk_company_job=models.ForeignKey(JobAdd, on_delete=models.CASCADE)# employer
    resume=models.FileField(upload_to='latest_Resume/',null=True)
    status=models.CharField(max_length=20,null=True)

class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    subject=models.CharField(max_length=250)
    message=models.TextField()

    def __str__(self):
        return self.name
