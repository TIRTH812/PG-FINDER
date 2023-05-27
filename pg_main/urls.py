from django.contrib import admin
from django.urls import path
from .views import FacilityCreateView,FacilityDeleteView,FacilityUpdateView,FacilityListView
from .views import PGCreateView,PGListView,PGDeleteView,PGUpdateView,PGDetailView, PGAmenitiesAddView, PGAmenitiesUpdateView, PGAmenitiesDetailView, PGImagesAddView, PGCommentView, PGCommentsDeleteView, ContactOwnerView,AdminPGListView ,ContactOwnerSuccessView,PGImagesListView,PGImagesDeleteView



urlpatterns = [    
    path('facility/create',FacilityCreateView.as_view(),name = 'facility_create'),    
    path('facility/list',FacilityListView.as_view(),name = 'facility_list'),    
    path('facility/delete/<int:pk>',FacilityDeleteView.as_view(),name = 'facility_delete'),    
    path('facility/update/<int:pk>',FacilityUpdateView.as_view(),name = 'facility_update'),    

    path('pg/create',PGCreateView.as_view(),name = 'pg_create'),
        
    path('admin/pg/list',AdminPGListView.as_view(),name = 'admin_pg_list'),

    path('pg/list',PGListView.as_view(),name = 'pg_list'),    
    path('pg/update/<int:pk>',PGUpdateView.as_view(),name = 'pg_update'),
    path('pg/delete/<int:pk>',PGDeleteView.as_view(),name = 'pg_delete'),
    path('pg/details/<int:pk>',PGDetailView.as_view(),name = 'pg_details'),
        
    path('pg/contact_owner/<int:pk>',ContactOwnerView.as_view(),name = 'contact_owner'),
    path('pg/contact_owner/success',ContactOwnerSuccessView.as_view(),name = 'contact_owner_success'),

    path('pg/amenities/add/<int:pk>',PGAmenitiesAddView.as_view(),name = 'add_pg_amenities'),
    path('pg/amenities/update/<int:pk>',PGAmenitiesUpdateView.as_view(),name = 'update_pg_amenities'),
    path('pg/amenities/detail/<int:pk>',PGAmenitiesDetailView.as_view(),name = 'detail_pg_amenities'),

    path('pg/images/<int:pk>',PGImagesListView.as_view(),name = 'view_pg_images'),
    path('pg/images/add/<int:pk>',PGImagesAddView.as_view(),name = 'add_pg_images'),
    path('pg/images/delete/<int:pk>',PGImagesDeleteView.as_view(),name = 'delete_pg_images'),
    
    path('pg/comments/<int:pk>',PGCommentView.as_view(),name = 'pg_comments'),
    path('pg/comments/delete/<int:pk>',PGCommentsDeleteView.as_view(),name = 'pg_comments_delete'),


]

