
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from mybenamakproject import settings
from mysite import views

from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('newsletter_subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    # path('portfolio/', views.portfolio_view, name='portfolio'),
    path('manage_designs/', views.manage_designs, name='manage_designs'),
    path('delete-design/<int:item_id>/', views.delete_design, name='delete_design'),
    path('design/', views.design_page, name='design_page'),
    path('save-design/', views.save_design, name='save_design'),
    path('edit-portfolio-item/<int:item_id>/', views.edit_portfolio_item, name='edit_portfolio_item'),
    path('upload/', views.upload_portfolio_item, name='upload_portfolio_item'),

    path(r'signup/', accounts_views.signup, name='signup'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
