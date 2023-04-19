from django.urls import path
from .views import *

urlpatterns = [
   path('',index,name='index'),

   path('about/',about,name='about'),
   path('contact/',contact,name='contact'),
   path('faqs/',FAQs,name='faqs'),

   path('all_login/',all_login,name='all_login'),
   path('logout/',logoutall,name='logout'),
   path('error/',error,name='error'),
   path('success/',success,name='success'),
   path('token_send/',token_send,name='token_send'),
   path('verify/<auth_token>',verify,name="verify"),


   path('applicant_register/',applicant_register,name='applicant_register'),
   path('applicant_profile/',applicant_profile,name='applicant_profile'),
   path('applicant_home/',applicant_home,name='applicant_home'),
   path('applicant_education/',applicant_education,name='applicant_education'),
   path('applicant_experience/',applicant_experience,name='applicant_experience'),
   path('applicant_keyskills/',applicant_keyskills,name='applicant_keyskills'),
   path('applicant_languages/',applicant_languages,name='applicant_languages'),
   path('applicant_projects',applicant_projects,name='applicant_projects'),
   path('jobs_list',jobs_list,name='jobs_list'),
   path('apply/<int:id>/',apply,name='apply'),
   path('notifications/',notifications,name='notifications'),
   path('edit_keyskills/<int:id>/',edit_keyskills,name='edit_keyskills'),
   path('delete_keyskills/<int:id>/',delete_keyskills,name='delete_keyskills'),
   path('edit_education/<int:id>/',edit_education,name='edit_education'),
   path('delete_education/<int:id>/',delete_education,name='delete_education'),
   path('edit_experience/<int:id>/',edit_experience,name='edit_experience'),
   path('delete_experience/<int:id>/',delete_experience,name='delete_experience'),
   path('edit_languages/<int:id>/',edit_languages,name='edit_languages'),
   path('delete_languages/<int:id>/',delete_languages,name='delete_languages'),
   path('edit_project/<int:id>/',edit_project,name='edit_project'),
   path('deleteproject/<int:id>/',deleteproject,name='deleteproject'),
   path('edit_careerobj/<int:id>/',edit_careerobj,name='edit_careerobj'),
   path('edit_resume/<int:id>/',edit_resume,name='edit_resume'),
   path('edit_profile/<int:id>/',edit_profile,name='edit_profile'),


   path('company_register/',company_register,name='company_register'),
   path('company_home/',company_home,name='company_home'),
   path('company_edit/<int:id>/',company_edit,name='company_edit'),
   path('addjob/',add_job,name='addjob'),
   path('joblist',joblist,name='company_joblist'),
   path('checkfill/<int:id>/',checkfill,name='checkfill'),
   path('job_edit/<int:id>/',job_edit,name='job_edit'),   
   path('job_delete/<int:id>/',job_delete,name='job_delete'),
   path('job_applicants',job_applicants,name='job_applicants'),
   path('change_status/<int:id>/',change_status,name='change_status'),
   path('all_users/',all_users,name='all_users'),


   path('admin_home/',admin_home,name='admin_home'),
   path('admin_companies/',admin_companies,name='admin_companies'),
   path('company_view/<int:id>/',company_view,name='company_view'),
   path('company_delete/<int:id>/',company_delete,name='company_delete'),
   path('admin_applicants/',admin_applicants,name='admin_applicants'),
   path('user_delete/<int:id>/',user_delete,name='user_delete'),
   path('user_view/<int:id>/',user_view,name='user_view'),
   path('admin_job_details/',admin_job_details,name='admin_job_details'),
   path('admin_job_delete/<int:id>/',admin_job_delete,name='admin_job_delete'),
   path('job_view/<int:id>/',job_view,name='job_view'),
   path('admin_live_jobs/',admin_live_jobs,name='admin_live_jobs'),
   path('admin_approve/',admin_approve,name='admin_approve'),
   # change

]