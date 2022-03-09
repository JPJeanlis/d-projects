from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.views.generic import RedirectView


# Use include() to add URLS from the inventoryApp application and authentication system
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns += [
    path('inventoryApp/', include('inventoryApp.urls')),

]


# Use static() to add url mapping to serve static files during development (only)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Add URL maps to redirect the base URL to our application
urlpatterns += [
    path('', RedirectView.as_view(url='/inventoryApp/', permanent=True)),
]


# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]