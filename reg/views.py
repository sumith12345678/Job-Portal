from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseForbidden
import uuid
from django.conf import settings
from django.core.mail import send_mail
# from django.contrib.auth.decorators import login_required

def all_login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not request.POST.get('remember_me',None): #remember me
            request.session.set_expiry(0)
        user=authenticate(username=username,password=password)
        if user is not None:
            request.session['user']=user.username # remember me
            login(request,user)
            if user.role == 1 :
                return redirect ('admin_home')
            elif user.role == 2 :
                return redirect ('company_home')
            elif user.role == 3 :
                return redirect ('jobs_list')
        else:
            return redirect ('/')
    return render (request,'base/login.html')


def logoutall(request):
    logout(request)
    return redirect ('/')

# def index(request):
    # return render(request,'base/index.html')



#APPLICANT

def applicant_register(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        if password1==password2:
            user=CustomUser.objects.create_user(
                username=username,
                password=password1,
                email=email,
                role=3, 
            )
            auth_token = str(uuid.uuid4())
            applicant_obj = ApplicantAuth.objects.create(fk_user_auth = user , auth_token = auth_token)
            applicant_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('token_send')
            # return redirect ('all_login')
        else:
            messages.error(request,'incorrect password')
    return render(request,'applicant/register.html')


def applicant_profile(request):
    if request.method == 'POST':
        user=request.user
        photo=request.FILES.get('photo')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        gender=request.POST.get('gender')
        marital_status=request.POST.get('marital_status')
        dob=request.POST.get('dob')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        workstatus=request.POST.get('workstatus')
        career_obj=request.POST.get('career_obj')
        resume=request.FILES.get('resume')
        jobrole=request.POST.get('jobrole')
    
        ApplicantProfile.objects.create(
                fk_user=user,
                photo=photo,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                marital_status=marital_status,
                dob=dob,
                address=address,
                phone=phone,
                workstatus=workstatus,
                jobrole=jobrole,
        )
        Resume.objects.create(
            fk_user=user,
            resume=resume,
        )
        CareerObj.objects.create(
            fk_user=user,
            career_obj=career_obj,
        )
        return redirect ('applicant_home')
    return render(request,'applicant/profile.html')

def applicant_projects(request):
    if request.method == 'POST':
        user=request.user
        project_name=request.POST.get('project_name')
        project_description=request.POST.get('project_description')
        project_link=request.POST.get('project_link')
        Projects.objects.create(
            fk_user=user,
            project_name=project_name,
            project_description=project_description,
            project_link=project_link,
        )
        return redirect ('applicant_home')
    return render(request,'applicant/projects.html')

def edit_project(request,id):
    proj=Projects.objects.get(id=id)
    if request.method == 'POST':
        project_name=request.POST.get('project_name')
        project_description=request.POST.get('project_description')
        project_link=request.POST.get('project_link')
        proj.project_name=project_name
        proj.project_description=project_description
        proj.project_link=project_link
        proj.save()
        return redirect ('applicant_home')
    return render(request,'applicant/editproject.html',{'proj':proj})

def deleteproject(request,id):
    proj=Projects.objects.get(id=id)
    proj.delete()
    return redirect('applicant_home')

def edit_resume(request,id):
    res=Resume.objects.get(id=id)
    if request.method == 'POST':
        resume=request.FILES.get('resume')
        res.resume=resume
        res.save()
        return redirect ('applicant_home')
    return render(request,'applicant/editresume.html',{'res':res})


def edit_careerobj(request,id):
    career=CareerObj.objects.get(id=id)
    if request.method == 'POST':
        career_obj=request.POST.get('career_obj')
        career.career_obj=career_obj
        career.save()
        return redirect ('applicant_home')
    return render(request,'applicant/editcareerobj.html',{'career':career})


def applicant_education(request):
    if request.method == 'POST':
        user=request.user
        level = request.POST.get('level')
        school_or_university = request.POST.get('school_or_university')
        course = request.POST.get('course')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        additional_details = request.POST.get('additional_details')
        Education.objects.create(
            fk_user=user,
            level = level,
            school_or_university = school_or_university,
            course = course,
            start_date = start_date,
            end_date = end_date,
            additional_details = additional_details,
        )
        return redirect ('applicant_home')
    return render(request,'applicant/education.html')

def applicant_keyskills(request):
    if request.method == 'POST':
        user=request.user
        key_skills=request.POST.get('key_skills')
        KeySkills.objects.create(
            fk_user=user,
            key_skills=key_skills,
        )
        return redirect ('applicant_home')
    return render(request,'applicant/keyskills.html')


def applicant_languages(request):
    if request.method == 'POST':
        user=request.user
        languages =request.POST.get('languages')
        proficiency =request.POST.get('proficiency')
        read =request.POST.get('read')
        write =request.POST.get('write')
        speak = request.POST.get('speak')
        Languages.objects.create(
            fk_user=user,
            languages=languages,
            proficiency=proficiency,
            read=read,
            write=write,
            speak=speak,
        )
        return redirect ('applicant_home')
    return render(request,'applicant/languages.html')


def applicant_experience(request):
    if request.method == 'POST':
        user=request.user
        is_this_current_emp=request.POST.get('is_this_current_emp')
        current_company_name=request.POST.get('current_company_name')
        location=request.POST.get('location')
        doj=request.POST.get('doj')
        current_salary=request.POST.get('current_salary')
        job_profile=request.POST.get('job_profile')
        notice_period=request.POST.get('notice_period')
        dol=request.POST.get('dol')
        Experience.objects.create(
            fk_user=user,
            is_this_current_emp=is_this_current_emp,
            current_company_name=current_company_name,
            location=location,
            doj=doj,
            current_salary=current_salary,
            job_profile=job_profile,
            notice_period=notice_period,
            dol=dol,
        )
        return redirect ('applicant_home')
    return render(request,'applicant/experience.html')


def applicant_home(request):
    user=request.user
    if request.user.is_authenticated:
        profile=ApplicantProfile.objects.filter(fk_user=user)
        if not profile.exists():
            return redirect('applicant_profile')
        profiles=ApplicantProfile.objects.get(fk_user=user)
        resume=Resume.objects.filter(fk_user=user)
        career=CareerObj.objects.filter(fk_user=user)
        projects=Projects.objects.filter(fk_user=user)
        education=Education.objects.filter(fk_user=user)
        key_skills=KeySkills.objects.filter(fk_user=user)
        languages=Languages.objects.filter(fk_user=user)
        experience=Experience.objects.filter(fk_user=user)
        context={
        'profile':profile,
        'education':education,
        'key_skills':key_skills,
        'languages':languages,
        'experience':experience,
        'profiles':profiles,
        'projects':projects,
        'career':career,
        'resume':resume,
        }
    return render(request,'applicant/home.html',context)

def jobs_list(request):
    user=request.user
    if request.user.is_authenticated:
        profile=ApplicantProfile.objects.filter(fk_user=user)
        if not profile.exists():
            return redirect('applicant_profile')
        all=Application.objects.filter(fk_user_pro__fk_user=request.user)
        jobs=JobAdd.objects.filter(filled=False).order_by('-id')
        if request.method == 'POST':
            jobname=request.POST.get('jobname')
            jobloc = request.POST.get('jobloc')
            if jobname:
                jobs=jobs.filter(job_title__icontains=jobname)
            if jobloc:
                jobs=jobs.filter(location__icontains=jobloc)
    return render(request,'applicant/jobs_list.html',{'jobs':jobs,'all':all})



def apply(request,id):
    user=ApplicantProfile.objects.get(fk_user=request.user)
    job=JobAdd.objects.get(id=id)
    application=Application.objects.filter(fk_user_pro=user,fk_company_job=job)
    if request.method == 'POST':
        resume=request.FILES.get('resume')
        Application.objects.create(
            fk_user_pro=user,
            fk_company_job=job,
            resume=resume,
            status='pending',
        )
        return redirect('jobs_list')
    return render(request,'applicant/apply.html',{'job':job,'user':user ,'application':application})


def notifications(request):
    all=Application.objects.filter(fk_user_pro__fk_user=request.user).order_by('-id')
    return render (request,'applicant/notification.html',{'all':all})

def edit_keyskills(request,id):
    skills=KeySkills.objects.get(id=id)
    if request.method == 'POST':
        skill=request.POST.get('key_skills')
        skills.key_skills=skill
        skills.save()
        return redirect ('applicant_home')
    return render (request,'applicant/edit_keyskills.html',{'skills':skills})

def delete_keyskills(request,id):
    skills=KeySkills.objects.get(id=id)
    skills.delete()
    return redirect ('applicant_home')

def edit_profile(request,id):
    profile=ApplicantProfile.objects.get(id=id)
    if request.method == 'POST':
        photo=request.FILES.get('photo')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        gender=request.POST.get('gender')
        marital_status=request.POST.get('marital_status')
        dob=request.POST.get('dob')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        workstatus=request.POST.get('workstatus')
        jobrole=request.POST.get('jobrole')
        profile.photo=photo
        profile.firstname=firstname
        profile.lastname=lastname
        profile.gender=gender
        profile.marital_status=marital_status
        profile.dob=dob
        profile.address=address
        profile.phone=phone
        profile.workstatus=workstatus
        profile.jobrole=jobrole
        profile.save()
        return redirect ('applicant_home')
    return render (request,'applicant/editprofile.html',{'profile':profile})


def edit_education(request,id):
    education=Education.objects.get(id=id)
    if request.method == 'POST':
        level = request.POST.get('level')
        school_or_university = request.POST.get('school_or_university')
        course = request.POST.get('course')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        additional_details = request.POST.get('additional_details')
        education.level = level
        education.school_or_university = school_or_university
        education.course = course
        education.start_date = start_date
        education.end_date = end_date
        education.additional_details = additional_details
        education.save()
        return redirect ('applicant_home')
    return render (request,'applicant/editeducation.html',{'education':education})


def delete_education(request,id):
    edu=Education.objects.get(id=id)
    edu.delete()
    return redirect ('applicant_home')


def edit_experience(request,id):
    experience=Experience.objects.get(id=id)
    if request.method == 'POST':
        current_company_name=request.POST.get('current_company_name')
        location=request.POST.get('location')
        doj=request.POST.get('doj')
        current_salary=request.POST.get('current_salary')
        job_profile=request.POST.get('job_profile')
        notice_period=request.POST.get('notice_period')
        dol=request.POST.get('dol')
        experience.current_company_name=current_company_name
        experience.location=location
        experience.doj=doj
        experience.current_salary=current_salary
        experience.job_profile=job_profile
        experience.notice_period=notice_period
        experience.dol=dol
        experience.save()
        return redirect ('applicant_home')
    return render (request,'applicant/editexperience.html',{'experience':experience})


def delete_experience(request,id):
    exp=Experience.objects.get(id=id)
    exp.delete()
    return redirect ('applicant_home')


def edit_languages(request,id):
    language=Languages.objects.get(id=id)
    if request.method == 'POST':
        languages =request.POST.get('languages')
        proficiency =request.POST.get('proficiency')
        read =request.POST.get('read')
        write =request.POST.get('write')
        speak = request.POST.get('speak')
        language.languages=languages
        language.proficiency=proficiency
        language.read=read
        language.write=write
        language.speak=speak
        language.save()
        return redirect ('applicant_home')
    return render (request,'applicant/editlanguage.html',{'language':language})

def delete_languages(request,id):
    lang=Languages.objects.get(id=id)
    lang.delete()
    return redirect ('applicant_home')

#COMPANY
 
def company_register(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        company_name = request.POST.get('company_name')
        logo = request.FILES.get('logo')
        description = request.POST.get('description')
        location = request.POST.get('location')
        phone_number = request.POST.get('phone_number')
        website = request.POST.get('website')
        industry = request.POST.get('industry')

        if password1==password2:

            user =CustomUser.objects.create_user(
                username=username,
                password=password1,
                email=email,
                role=2, 
            )
            CompanyProfile.objects.create(
                fk_company=user,
                company_name=company_name,
                logo=logo,
                description=description,
                location=location,
                phone_number=phone_number,
                website=website,
                industry=industry,
                company_status=False, #change
            )
            auth_token = str(uuid.uuid4())
            company_obj = CompanyAuth.objects.create(fk_company_auth = user, auth_token = auth_token)
            company_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('token_send')

            # message: please wait admin will approve soon.
            # return redirect ('all_login')
        else:
            messages.error(request,'incorrect password')
    return render(request,'company/register.html')


def company_home(request):
    company=CompanyProfile.objects.get(fk_company=request.user)

    if not company.company_status:          
         return HttpResponseForbidden("Your account is not yet approved by the admin.")  #change

    companydetail=CompanyProfile.objects.filter(fk_company=request.user)
    job=JobAdd.objects.filter(fk_company_pro__fk_company=request.user)
    fill=JobAdd.objects.filter(filled=False)
    live=fill.filter(fk_company_pro__fk_company=request.user)
    users=ApplicantProfile.objects.all()
    applications=Application.objects.filter(fk_company_job__fk_company_pro__fk_company=request.user)
    selected=applications.filter(status='Accepted')
    context={
        'companydetail':companydetail,
        'company':company,
        'job':job,
        'live':live,
        'users':users,
        'selected':selected,
    }
    return render(request,'company/home.html',context)


def add_job(request):
    if request.method == 'POST':
        user=CompanyProfile.objects.get(fk_company=request.user)
        job_title =request.POST.get('job_title')
        job_description =request.POST.get('job_description')
        job_type = request.POST.get('job_type')
        industry = request.POST.get('industry')
        location = request.POST.get('location')
        job_fields=request.POST.get('job_fields')
        salary = request.POST.get('salary')
        education_requirements = request.POST.get('education_requirements')
        experience_requirements = request.POST.get('experience_requirements')
        skills_and_qualifications = request.POST.get('skills_and_qualifications')
        application_deadline = request.POST.get('application_deadline')
        vacancy=request.POST.get('vacancy')
        JobAdd.objects.create(
            fk_company_pro=user,
            job_title=job_title,
            job_description=job_description,
            job_type=job_type,
            industry=industry,
            location=location,
            job_fields=job_fields,
            salary=salary,
            education_requirements=education_requirements,
            experience_requirements=experience_requirements,
            skills_and_qualifications=skills_and_qualifications,
            application_deadline=application_deadline,
            filled=False,
            vacancy=vacancy,
        )
        return redirect ('company_joblist')
    return render(request,'company/addjob.html')


def joblist(request):
    user=CompanyProfile.objects.get(fk_company=request.user)
    job_lists=JobAdd.objects.filter(fk_company_pro=user)
    return render (request,'company/joblist.html',{'job_lists':job_lists})


def checkfill(request, id):
    job = JobAdd.objects.get(id=id)
    if job:
        job.filled = not job.filled
        job.save()
        return redirect('company_joblist')
    return render(request,'company/joblist.html')


def job_applicants(request):
    user=request.user
    all=Application.objects.filter(fk_company_job__fk_company_pro__fk_company=user)
    return render (request,'company/applicants.html',{'all':all})


def job_delete(request,id):
    user=JobAdd.objects.filter(id=id)
    user.delete()
    return redirect('company_joblist')


def job_edit(request,id):
    job=JobAdd.objects.get(id=id)
    if request.method == 'POST':
        job_title =request.POST.get('job_title')
        job_description =request.POST.get('job_description')
        job_type = request.POST.get('job_type')
        industry = request.POST.get('industry')
        location = request.POST.get('location')
        job_fields=request.POST.get('job_fields')
        salary = request.POST.get('salary')
        education_requirements = request.POST.get('education_requirements')
        experience_requirements = request.POST.get('experience_requirements')
        skills_and_qualifications = request.POST.get('skills_and_qualifications')
        application_deadline = request.POST.get('application_deadline')
        vacancy=request.POST.get('vacancy')
        job.job_title=job_title
        job.job_description=job_description
        job.job_type=job_type
        job.industry=industry
        job.location=location
        job.job_fields=job_fields
        job.salary=salary
        job.education_requirements=education_requirements
        job.experience_requirements=experience_requirements
        job.skills_and_qualifications=skills_and_qualifications
        job.application_deadline=application_deadline
        job.vacancy=vacancy
        job.save()
        return redirect('company_joblist')
    return render(request,'company/job_edit.html',{'job':job})


def company_edit(request,id):
    company=CompanyProfile.objects.get(id=id)
    if request.method == 'POST':
        logo = request.FILES.get('logo')
        description = request.POST.get('description')
        location = request.POST.get('location')
        phone_number = request.POST.get('phone_number')
        website = request.POST.get('website')
        industry = request.POST.get('industry')
        company.logo=logo
        company.description=description
        company.location=location
        company.phone_number=phone_number
        company.website=website
        company.industry=industry
        company.save()
        return redirect('company_home')
    return render(request,'company/company_edit.html',{'company':company})

def change_status(request,id):
    change_status=Application.objects.get(id=id)
    if request.method == 'POST':
        s=request.POST.get('status')
        change_status.status=s
        change_status.save()
        return redirect('job_applicants')
    return render(request,'company/status.html',{'change':change_status})

def all_users(request):
    profile=ApplicantProfile.objects.all()
    if request.method == 'POST':
        jobrole=request.POST.get('jobrole')
        if jobrole:
            profile=profile.filter(jobrole__icontains=jobrole)
    context={
        'profile':profile,
        }
    return render(request,'company/allusers.html',context)



#ADMIN

def admin_home(request):
    company=CompanyProfile.objects.all()
    profile=ApplicantProfile.objects.all()
    job=JobAdd.objects.all()
    live=JobAdd.objects.filter(filled=False)
    latest_companies = CompanyProfile.objects.order_by('-id')[:10]
    filtered_companies = CompanyProfile.objects.filter(id__in=[c.id for c in latest_companies]).order_by('-id')
    latest_applicants = ApplicantProfile.objects.order_by('-id')[:10]
    filtered_applicants = ApplicantProfile.objects.filter(id__in=[a.id for a in latest_applicants]).order_by('-id')
    context={
        'company':company,
        'profile':profile,
        'job':job,
        'live':live,
        'filtered_companies':filtered_companies,
        'filtered_applicants':filtered_applicants,
    }
    return render(request,'admin/home.html',context)

def admin_job_details(request):
    job=JobAdd.objects.all()
    context={
         'job':job,}
    return render(request,'admin/job_details.html',context)

def admin_live_jobs(request):
    live=JobAdd.objects.filter(filled=False)
    context={
         'live':live,}
    return render(request,'admin/live_jobs.html',context)

def admin_companies(request):
    company=CompanyProfile.objects.all()
    if request.method == 'POST':
        company_name=request.POST.get('company_name')
        if company_name:
            company=company.filter(company_name__icontains=company_name)
    context={
        'company':company,
        }
    return render(request,'admin/companies.html',context)
        
def admin_applicants(request):
    profile=ApplicantProfile.objects.all()
    if request.method == 'POST':
        firstname=request.POST.get('firstname')
        if firstname:
            profile=profile.filter(firstname__icontains=firstname)
    context={
        'profile':profile,
        }
    return render(request,'admin/applicants.html',context)

def user_delete(request,id):
    user=CustomUser.objects.filter(id=id)
    user.delete()
    return redirect('admin_applicants')

def company_delete(request,id):
    user=CustomUser.objects.filter(id=id)
    user.delete()
    return redirect('admin_companies')


def admin_job_delete(request,id):
    user=JobAdd.objects.filter(id=id)
    user.delete()
    return redirect('admin_job_details')

    
def company_view(request,id):
    company=CompanyProfile.objects.filter(id=id)
    context={'company':company}
    return render(request,'admin/company_view.html',context)

def user_view(request,id):
    user=ApplicantProfile.objects.filter(id=id)
    context={'user':user}
    return render(request,'admin/user_view.html',context)

def job_view(request,id):
    job=JobAdd.objects.filter(id=id)
    context={'job':job}
    return render(request,'admin/job_view.html',context)

def admin_approve(request):
    if request.method == 'POST':
        company_id=request.POST.get('approve')
        company=CompanyProfile.objects.get(id=company_id)
        company.company_status = True
        company.save()
        return redirect ('admin_home')
    unapproved= CompanyProfile.objects.filter(company_status=False)
    context={ 
        'unapproved':unapproved
    }
    return render(request,'admin/approve.html',context) 
    # change

#Auth Email

def error(request):
    return render (request,'base/error.html')

def success(request):
    return render(request,'base/success.html')

def token_send(request):
    return render(request,'base/token_send.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print(email)
    print(token)
    send_mail(subject, message , email_from ,recipient_list )

def verify(request , auth_token):
    try:
        applicant_obj = ApplicantAuth.objects.filter(auth_token = auth_token).first()
        company_obj=CompanyAuth.objects.filter(auth_token = auth_token).first()
    
        if applicant_obj:
            if applicant_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                print(applicant_obj.auth_token)
                return redirect('all_login')
            applicant_obj.is_verified = True
            applicant_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('success')
        if company_obj:
            if company_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                print(company_obj.auth_token)
                return redirect('all_login')
            company_obj.is_verified = True
            company_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('success')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')



def index(request):
    jobs=JobAdd.objects.filter(filled=False).order_by('-id')
    if request.method == 'POST':
        jobname=request.POST.get('jobname')
        if jobname:
            jobs=jobs.filter(job_title__icontains=jobname)
    context={'jobs':jobs}
    return render(request,'base2/index2.html',context)

def about(request):
    return render(request,'base2/about.html')

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        messages.success(request,'Your message has been sent. Thank you!')
        return redirect('contact')
    return render(request,'base2/contact.html')

def FAQs(request):
    return render(request,'base2/faqs.html')