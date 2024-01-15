from django.urls import path
from fruitapp import views
from fruitstore import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home),
    path('login',views.ulogin),
    path('register',views.register),
    path('logout',views.ulogout),
    path('about',views.about),
    path('catfilter/<fv>',views.catfilter),
    path('juicecatfilter/<jv>',views.juicecatfilter),
    path('fruits',views.fruits),
    path('fruitdetails/<fid>',views.fruitdetails),
    path('juices',views.juices),
    path('juicedetails/<jid>',views.juicedetails),
    path('fruitaddcart/<pid>',views.fruitaddcart),
    path('juiceaddcart/<pid>',views.juiceaddcart),
    path('fruitcart',views.fruitcart),
    path('juicecart',views.juicecart),
    path('fruitremove/<cid>',views.fruitremove),
    path('updatefruitquantity/<qv>/<cid>',views.updatefruitquantity),
    path('juiceremove/<cid>',views.juiceremove),
    path('updatejuicequantity/<qv>/<cid>',views.updatejuicequantity),
    path('fruitplaceorder',views.fruitplaceorder),
    path('juiceplaceorder',views.juiceplaceorder),
    path('fruitmakepayment',views.fruitmakepayment),
    path('juicemakepayment',views.juicemakepayment),
    path('fruitsendusermail',views.fruitsendusermail),
    path('juicesendusermail',views.juicesendusermail),
    path('changepassword/<uid>',views.changepassword),
    path('changepassword',views.password),
    path('profile',views.user_profile),
    path('updateprofile/<uid>',views.update_profile),
    path('display_cart',views.display_cart),
    path('orderhistory',views.orderhistory),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)