"""
URL configuration for project_candles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='product'),
    path('product/', views.product, name='product'),
    path('login/', views.login),
	path('logout/', views.logout),
    path('admin/', admin.site.urls),
    path('adduser/',views.adduser),
    path('adminmain/', views.adminmain, name='adminmain'),
    path('adminmain/<str:pageindex>/', views.adminmain),
    path('product_add/', views.product_add, name='product_add'),
    path('product_edit/<int:product_id>/', views.product_edit),
 	path('product_edit/<int:product_id>/<str:edittype>/', views.product_edit),
 	path('product_delete/<int:product_id>/', views.product_delete),
 	path('product_delete/<int:product_id>/<str:deletetype>/', views.product_delete),
    # path('admin/', admin.site.urls),
    path('albumindex/', views.albumindex),
    path('albumshow/<int:albumid>/', views.albumshow),
    path('albumphoto/<int:photoid>/<int:albumid>/', views.albumphoto),
    path('albumlogin/', views.albumlogin),
    path('albumlogout/', views.albumlogout),
    path('albumadminmain/', views.albumadminmain),
    path('albumadminmain/<int:albumid>/', views.albumadminmain),
    path('albumadminadd/', views.albumadminadd),
    path('albumadminfix/<int:albumid>/', views.albumadminfix),
    path('albumadminfix/<int:albumid>/<int:photoid>/', views.albumadminfix),
    path('albumadminfix/<int:albumid>/<int:photoid>/<str:deletetype>/', views.albumadminfix),
    # path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    # path('cartindex/', views.cartindex),
    path('detail/<int:product_id>/', views.detail),
    path('addtocart/<str:ctype>/', views.addtocart),
    path('addtocart/<str:ctype>/<int:product_id>/', views.addtocart),
    path('cart/', views.cart),
    path('cartorder/', views.cartorder),
    path('cartok/', views.cartok),
    path('cartordercheck/', views.cartordercheck),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)