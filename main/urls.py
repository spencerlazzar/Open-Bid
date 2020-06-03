from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('con_home', views.con_home),
    path('contractor_reg_login', views.con_reg_form),
    path('con_register', views.con_register),
    path('con_login', views.con_login),
    path('customer_reg_login', views.cus_reg_form),
    path('cus_register', views.cus_register),
    path('cus_home', views.cus_home),
    path('cus_login', views.cus_login),
    path('logout', views.logout),
    path('specialty_add', views.specialty_add),
    path('submit_project', views.submit_project),
    path('cus_view_proj/<int:id>', views.project_info),
    path('cus_view_bid/<int:id>', views.cus_view_bid),
    path('bid_form/<int:id>', views.bid_form),
    path('place_bid', views.place_bid),
    path('edit_bid/<int:id>', views.edit_bid),
    path('process_edit', views.process_edit),
    path('accept_bid/<int:id>', views.accept_bid),
    path('project_complete/<int:id>',views.project_complete),
    path('project_complete_review',views.project_complete_review),
    path('add_img',views.add_img),
]

