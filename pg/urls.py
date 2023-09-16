from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
     path('',views.test),
     path('home',views.home,name='home'),
     path('about',views.about),
     path('contact',views.contact),
     path('service',views.service),
     path('show_pg/service',views.service),
     # pg owner
     path('pgowner_login',views.pg_owner_login),
     path('pg_owner_registration',views.pg_owner_registration),
     path('plogout',views.plogout,name='plogout'),

     #user
     path('userreg',views.userreg),
     path('ulogin',views.ulogin,name='ulogin'),
     path('ulogout',views.ulogout,name='ulogout'),
     
     # path('change_password',views.change_password,name='change_password'),
     path('change_password',views.change_password,name='change_password'),
     path('passwordchange', views.passwordchange, {'user_type': 'User'}, name='changepassword_user'),
     path('passwordchange', views.passwordchange, {'user_type': 'PGOwner'}, name='changepassword_pgowner'),


     path('popertylist',views.popertylist),
     path('listing',views.listing),
     path('add_pg', views.create_pg),
     path('pg_search',views.pg_search),
     path('show_pg/<int:pg_id>', views.show_pg, name='show_pg'),
     path('show_pg/book_details', views.book_details, name='book_details'),
     path('status',views.payment_status, name='payment_status'),

     path('bookinglist',views.bookinglist, name='bookinglist'),

     path('forgot_password/customer', views.forgot_password_customer, name='forgot_password_customer'),
     path('forgot_password/pg_lister', views.forgot_password_pg_lister, name='forgot_password_pg_lister'),
     path('reset_password/customer', views.reset_password_customer, name='reset_password_customer'),
     path('reset_password/pg_lister', views.reset_password_pg_lister, name='reset_password_pg_lister'),
     path('password_reset_confirmation', views.password_reset_confirmation, name='password_reset_confirmation'),


     path('profile', views.profile),
     path('pgowner_profile', views.pgowner_profile),

     path('pgowner_booking',views.pgowner_booking),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
