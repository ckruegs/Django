from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_user', views.process_user),
    path('login_user', views.login_user),
    path('dashboard', views.dashboard),
    path('process_quote', views.process_quote),
    path('quotes/<int:id>/edit', views.quote_edit),
    path('quotes/<int:id>/update', views.quote_update),
    path('users/<int:id>', views.show_user),
    path('quotes/<int:id>/delete', views.quote_delete),
    path('logout', views.logout),
]