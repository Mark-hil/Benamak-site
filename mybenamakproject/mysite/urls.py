from django.urls import path, include
# from .views import contact_thank_you, contact_view
from mybenamakproject import views



urlpatterns = [
    path('contact', views.contact_view, name='contact'),
    #  path('contact/', contact_view, name='contact'),
    path('contact/thank-you/', views.contact_thank_you, name='contact_thank_you'),
    
    # other url patterns
]