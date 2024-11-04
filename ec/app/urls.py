from django.urls import path,include
from . import views
from  django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordResetForm, MypasswordChangeForm,MySetPasswordForm
from .views import CustomAdminView
from app.views import CustomAdminView

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('product-detail/<int:pk>/', views.product_detail, name='product-detail'),
    # Login redirect path
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('category-title/<val>/', views.CategoryTitle.as_view(), name='category-title'),

    # Update address
    path('updateAddress/<int:pk>/', views.updateAddress.as_view(), name='updateAddress'),

    # Registration
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    # Login process
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),

    # Password reset & forgetpassword
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/passwordreset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordresetconfirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordresetcomplete.html'),name='password_reset_complete'),
 
    #add to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    #path('paymentdone/',views.payment_done,name='paymentdone'),
     path('orders/', views.orders, name='orders'),
     path('product-detail/<int:product_id>/', views.product_detail, name='product-detail'),

     #payment_success
     path('payment-success/', views.payment_success, name='payment_success'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
#Wishlist
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist),
    
#search
    path('search/',views.search,name='search'),


    #logout
   path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Password change
     path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MypasswordChangeForm,success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    #ADMIN
    path('admin/', admin.site.urls),
    path('custom-admin/', CustomAdminView.as_view(), name='custom_admin'),

    path('wishlist/', views.wishlist_view, name='wishlist'),  # Wishlist page
    path('plus_wishlist/', views.plus_wishlist, name='plus_wishlist'),
    path('minus_wishlist/', views.minus_wishlist, name='minus_wishlist'),

#admin
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/update/<int:pk>/', views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/update/<int:pk>/', views.customer_update, name='customer_update'),
    path('customers/delete/<int:pk>/', views.customer_delete, name='customer_delete'),

    path('carts/', views.cart_list, name='cart_list'),
    path('carts/add/', views.cart_add, name='cart_add'),
    path('carts/edit/<int:pk>/', views.cart_edit, name='cart_edit'),
    path('carts/delete/<int:pk>/', views.cart_delete, name='cart_delete'),

    path('order/', views.order_list, name='order_list'),
    path('orders/add/', views.order_add, name='order_add'),
    path('orders/edit/<int:pk>/', views.order_edit, name='order_edit'),
    path('orders/delete/<int:pk>/', views.order_delete, name='order_delete'),

    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_add, name='payment_add'),
    path('payments/edit/<int:pk>/', views.payment_edit, name='payment_edit'),
    path('payments/delete/<int:pk>/', views.payment_delete, name='payment_delete'), 

    path('dashboard/', views.dashboard, name='dashboard'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header='Stationary Shop'
admin.site.site_title='Stationary Shop'
admin.site.site_index_title='Welcome to Stationary Shop'