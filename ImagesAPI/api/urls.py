from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('image/', views.ImageView.as_view({'post': 'create'}), name='image-images'),
    path('account/', views.AccountView.as_view({'get': 'get'}), name='account-accounts'),
    path('account/<int:pk>', views.AccountDetailView.as_view({'get':'get_one'}), name='account-single-account'),
]

