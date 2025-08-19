from django.urls import path
from . import views
from .views import view_notification


urlpatterns=[
    path('',views.home,name='home'),
    path('crop_list', views.crop_list, name='crop_list'),
    path('create_category', views.create_category,name='create_category'),
    path('catrgory_list', views.category_list,name='category_list'),
    path('add_crop', views.add_crop, name='add_crop'),
    path('crop_update/<int:pid>/', views.crop_update, name='crop_update'),
    path('crop_delete/<int:pid>/', views.crop_delete, name='crop_delete'),
    path('crop_history',views.crop_history,name='crop_history'),
    path('restore/<int:pid>', views.restore, name='restore'),
    path('permanent/<int:pid>',views.permanent,name='permanent'),
    path('cansumer_crop_list',views.consumer_crop_list,name='consumer_crop_list'),
    path('crop/<int:pid>/',views.crop_detail, name='crop_detail'),
    path('farmer_dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
    path('view_notification/<int:notification_id>/', view_notification, name='view_notification'),
    path('farmer/orders/', views.farmer_orders, name='farmer_orders'),
    path('farmer/order/<int:order_id>/', views.order_detail, name='order_detail'),
   
    path('order/<int:crop_id>', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    # 👤 Consumer
    path('my-orders/', views.consumer_orders, name='consumer_orders'),

    # 👨‍🌾 Farmer
    path('farmer/update-order/<int:order_id>/', views.update_order_status, name='update_order_status'),

  

    # 🚚 Delivery Agent
    path('delivery-orders/', views.delivery_agent_orders, name='delivery_agent_orders'),
]