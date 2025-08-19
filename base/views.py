from django.shortcuts import render,redirect,get_object_or_404
from .forms import CropForm,OrderForm,CategoryForm,OrderStatusForm
from .models import Crop,Order,Category
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.
def home(request):
    return render(request, 'home.html')


def unauthorized_view(request):
    return render(request, 'unauthorized.html')


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success('Category Created Successfuliy')

            return redirect('category_list')
        
    else:
        form = CategoryForm()
    return render(request,'create_category.html',{'form':form})
@login_required
def category_list(request):
    data=Category.objects.all()
    return render(request,'category_list.html',{'data':data})
@login_required
def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST,request.FILES)
        if form.is_valid():
            crop= form.save(commit=False)
            crop.farmer = request.user 
            crop.save()
            messages.success(request, "Crop added successfully.")
            return redirect('crop_list')
    else:
        form=CropForm()
    return render(request,'add_crop.html',{'form':form})
# @login_required
# def crop_list(request):
#     cid= request.GET.get('category_id')
#     data=Category.objects.all()
#     if cid:
#         data1=Crop.objects.filter(category_id=cid)
#     else:
#         data1=Crop.objects.all()
#     return render (request,'crop_list.html',{'data':data,'data1':data1})


# @login_required
# def crop_list(request):
#     if not request.user.is_farmer:
#         return render(request, 'unauthorized.html') 

#     cid = request.GET.get('category_id')
#     data = Category.objects.all()

#     if cid:
#         data1 = Crop.objects.filter(category_id=cid)
#     else:
#         data1= Crop.objects.filter(farmer=request.user, is_deleted=False)

#     return render(request, 'crop_list.html', {
#         'data': data,
#         'data1': data1})

@login_required
def crop_list(request):
    farmer = request.user
    category_id = request.GET.get('category_id')

    categories = Category.objects.all()
    crops = Crop.objects.filter(farmer=farmer)

    if category_id:
        crops = crops.filter(category_id=category_id)

    return render(request, 'crop_list.html', {
        'categories': categories,
        'crops': crops,
    })






@login_required
def crop_update(request,pid):
    data=get_object_or_404(Crop,id=pid)
    if request.method=='POST':
        form=CropForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Crop updated successfully.")
            return redirect('crop_list')
    else:
        form=CropForm(instance=data)
    return render(request,'crop_update.html',{'form':form})
@login_required
def crop_delete(request,pid):
    data=get_object_or_404(Crop,id=pid)
    if request.method=='POST':
        data.is_deleted=True
        data.deleted_at=timezone.now()
        data.save()
        messages.success(request, "Crop deleted successfully.")
        return redirect('crop_list')
    return render(request,'crop_delete.html',{'data':data})
@login_required
def crop_history(request):
    data=Crop.objects.filter(is_deleted=True)
    return render(request,'crop_history.html',{'data':data})
@login_required
def restore(request,pid):
    data=get_object_or_404(Crop,id=pid,is_deleted=True)
    if request.method=='POST':
        data.is_deleted=False
        data.deleted_at=None
        data.save()
        messages.success(request, "Crop restored successfully.")
        return redirect ('crop_history')
    return render(request,'restore.html',{'data':data})
@login_required
def permanent(request, pid):
    data = get_object_or_404(Crop, id=pid)
    if request.method == 'POST':
        data.delete()  # Permanently delete the photo from the database
        return redirect('crop_list')
    return render(request, 'permanent.html',{'data': data})


@login_required
def consumer_crop_list(request):
    if request.user.is_consumer:
        data = Crop.objects.filter(is_deleted=False)
        return render(request, 'consumer_crop_list.html', {'data': data})
    else:
        return render(request, 'unauthorized.html')

def crop_detail(request,pid):
    data=get_object_or_404(Crop,id=pid)
    return render (request,'crop_detail.html',{'data':data})

@login_required
def place_order(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.crop = crop
            order.consumer = request.user if request.user.is_authenticated else None
            order.total_price = crop.price_per_kg * Decimal(str(order.quantity_ordered))
            order.save()
            messages.success(request, "Order placed successfully.")

            # Create a notification for the farmer
            Notification.objects.create(
                farmer=crop.farmer,
                consumer=request.user,  # Set who placed the order
                crop=crop,
                order=order,
                message=f"{request.user.username} ordered {order.quantity_ordered}kg of {crop.name}.",
                link=f"/farmer/orders/"
            )

            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'place_order.html', {'form': form, 'data': crop})

@login_required
def order_success(request):
    return render(request, 'order_success.html')

@login_required
def consumer_orders(request):
    orders = Order.objects.filter(consumer=request.user).order_by('-id')
    #orders = Order.objects.filter(consumer=request.user)
    return render(request, 'consumer_orders.html', {'orders': orders})


@login_required
def delivery_agent_orders(request):
    orders = Order.objects.exclude(status='delivered')
    return render(request, 'delivery_orders.html', {'orders': orders})

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()  # 🔥 This must be present!
            messages.success(request, "Order status updated successfully.")
            return redirect('farmer_orders')
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'update_order_status.html', {'form': form, 'order': order})

@login_required
def farmer_dashboard(request):
    crops = Crop.objects.filter(farmer=request.user)  # ✅ fixed
    notifications = Notification.objects.filter(farmer=request.user).order_by('-created_at')  # ✅ fixed

    return render(request, 'farmer_dashboard.html', {
        'crops': crops,
        'notifications': notifications
    })

def view_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()

    consumer = notification.consumer  # or notification.order.consumer
    return render(request, 'notification_detail.html', {
        'notification': notification,
        'consumer': consumer
    })


@login_required
def farmer_orders(request):
    if not request.user.is_farmer:
        return render(request, 'unauthorized.html')

    crops = Crop.objects.filter(farmer=request.user)
    orders = Order.objects.filter(crop__in=crops).select_related('consumer', 'crop')

    return render(request, 'farmer_orders.html', {
        'orders': orders
    })


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.crop.farmer != request.user:
        return render(request, 'unauthorized.html')

    return render(request, 'order_detail.html', {'order': order})