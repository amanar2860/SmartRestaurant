from django.shortcuts import render, get_object_or_404, redirect


import qrcode
import qrcode.image.svg
from requests import session
from io import BytesIO
from django.core.files import File

from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .decorators import *
from django.db.models import Sum

class MenuListView(ListView):
    model = Item
    template_name = 'main/index.html'

# class home(ListView):
#     model = Item
#
#     template_name = 'main/home.html'
#     context_object_name = 'menu_items'


@login_required
def home(request):
    t_no =int(request.session.setdefault('tno', '0'))
    if (t_no > 0):
        categorys = Category.objects.all()
        model = Item.objects.all()
        context = {}
        context = {
            'categorys':categorys,
            'menu_items':model,
        }
        return render(request, 'main/home.html', context)
    else:
        return redirect("main:scan_qrcode")

def home_filter(request,catid):
    t_no = int(request.session.setdefault('tno', '0'))
    if (t_no > 0):
        categorys = Category.objects.all()
        item = Item.objects.filter( category=catid)
        context = {}
        context = {
            'categorys': categorys,
            'menu_items':item,
        }
        return render(request, 'main/home.html', context)
    else:
        return redirect("main:scan_qrcode")


def menuDetail(request, slug):
    item = Item.objects.filter(slug=slug).first()
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7] 
    context = {
        'item': item,
        'reviews': reviews,
    }
    return render(request, 'main/dishes.html', context)

@login_required
def add_reviews(request):
    if request.method == "POST":
        user = request.user
        rslug = request.POST.get("rslug")
        item = Item.objects.get(slug=rslug)
        review = request.POST.get("review")
        reviews = Reviews(user=user, item=item, review=review, rslug=rslug)
        reviews.save()
        messages.success(request, "Thank You for Reviewing this Item!!")
    return redirect(f"/dishes/{item.slug}")

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ('id','categoryname', 'imageurl')
    success_url = '/category_list/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@login_required(login_url='/accounts/login/')
@admin_required
def category_list(request):
    categorys = Category.objects.all()
    context = {
        'categorys':categorys

    }
    return render(request, 'main/category_list.html', context)

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['categoryname',' imageurl']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False


class TableOrdersCreateView(LoginRequiredMixin, CreateView):
    model = TableOrders
    fields = ('phoneno', 'onDate','onTime','totalperson','table_orderno','description',)

    #99template_name = '/successful.html'
    success_url = '/table-reserv-success'
    def form_valid(self, form):

        form.instance.created_by = self.request.user
        form.instance.user = self.request.user
        return super().form_valid(form)
    #return render(request,'main/tableorders_form.html')


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = ('name', 'message')
    #template_name = 'feedback_form.html'
    success_url = '/feedback/new'
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.user = self.request.user
        #session['msg'] = 'Successful send'
        return super().form_valid(form)
    #return render(request,'main/tableorders_form.html')

@login_required(login_url='/accounts/login/')
@admin_required
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    context = {
        'feedbacks': feedbacks
    }
    return render(request, 'main/feedback_list.html', context)


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['categoryname', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    success_url = '/item/new'
    fields = ['category','title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['category','title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/item_list'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_item = CartItems.objects.create(
        item=item,
        user=request.user,
        ordered=False,
    )
    messages.info(request, "Added to Cart!!Continue Shopping!!")
    return redirect("main:cart")

def add_session_value(request,tno):

    request.session['tno'] = str(tno)

    return redirect(reverse("main:home"))



@login_required
def get_cart_items(request):
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    bill = cart_items.aggregate(Sum('item__price'))
    number = cart_items.aggregate(Sum('quantity'))
    pieces = cart_items.aggregate(Sum('item__pieces'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    total_pieces = pieces.get("item__pieces__sum")
    context = {
        'cart_items':cart_items,
        'total': total,
        'count': count,
        'total_pieces': total_pieces
    }
    return render(request, 'main/cart.html', context)

class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItems
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user == cart.user:
            return True
        return False

@login_required
def order_item(request):
    # display_type = request.POST.get("digital", None)
    # if display_type in ["digital"]:
    #tableno,donate_status,payment_status,payment_Desc
    t_no= int(request.session.setdefault('tno', '0'))
    if(t_no>0):

        cart_items = CartItems.objects.filter(user=request.user,ordered=False)
        ordered_date=timezone.now()
        cart_items.update(ordered=True,ordered_date=ordered_date,table_orderno=t_no)

        messages.info(request, "Item Ordered")
        request.session['tno']=0
        return redirect("main:order_details")
    else:
        return redirect("main:scan_qrcode")
@login_required
def order_item(request,paymodeIsDonated):
    # display_type = request.POST.get("digital", None)
    # if display_type in ["digital"]:
    #tableno,donate_status,payment_status,payment_Desc
    t_no= int(request.session.setdefault('tno', '0'))
    if(t_no>0):
        x = paymodeIsDonated.split('&')
        cart_items = CartItems.objects.filter(user=request.user,ordered=False)
        ordered_date=timezone.now()
        cart_items.update(ordered=True,ordered_date=ordered_date,payment_status=x[0],donate_status=x[1],table_orderno=t_no)
        messages.info(request, "Item Ordered Successful Your Table No.: "+str(t_no))
        request.session['tno']=0
        return redirect("main:ordersuccess")
        #return redirect("main:order_details")


    else:
        return redirect("main:scan_qrcode")

def ordersuccess(request):
    # context = {
    #     'cart_items':cart_items,
    # }
    return render(request, 'main/payment_success.html')



@login_required
def order_details(request):
    items = CartItems.objects.filter(user=request.user, ordered=True,status="Active").order_by('-ordered_date')
    cart_items = CartItems.objects.filter(user=request.user, ordered=True,status="Delivered").order_by('-ordered_date')
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    pieces = items.aggregate(Sum('item__pieces'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    total_pieces = pieces.get("item__pieces__sum")
    context = {
        'items':items,
        'cart_items':cart_items,
        'total': total,
        'count': count,
        'total_pieces': total_pieces
    }
    return render(request, 'main/order_details.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def admin_view(request):
    cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True,status="Delivered").order_by('-ordered_date')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'main/admin_view.html', context)

def tablesuccess(request):

    return render(request, 'main/successful.html')


def payment_view(request):
    total=0.0
    context = {}
    if request.method == "POST":
        context = {
            'total': request.POST.get("finalamt", ""),
        }

    return render(request, 'main/payment.html',context)

def genrate_qrcode(request):
    context={}
    if request.method == "POST":
        num=request.POST.get("qr_text", "")
        qrcode_img = qrcode.make(request.POST.get("qr_text", ""))
        fname = f'qr_code_'+num+'.png'
        buffer = BytesIO()
        qrcode_img.save("media/qr_images/" + fname, File(buffer), save=True)
        context = {
            'qrimageurl': settings.MEDIA_URL+"/qr_images/" + fname,
        }

    return render(request, 'main/genrate_qrcode.html', context)


# def home_view(request):
#
#     return render(request,'main/home.html')


def aboutus_view(request):
    return render(request, 'main/aboutus.html')

def paymentchoise(request):

    return render(request, 'main/payment_choise.html')

def donate(request):
    return render(request, 'main/donate.html')



def scan_qrcode(request):

    return render(request, 'main/scanQrCode.html')


def contactus_view(request):
    return render(request, 'main/contactus.html')


@login_required(login_url='/accounts/login/')
@admin_required
def item_list(request):
    items = Item.objects.filter(created_by=request.user)
    context = {
        'items':items
    }
    return render(request, 'main/item_list.html', context)

@login_required
@admin_required
def update_status(request,pk):
    if request.method == 'POST':
        status = request.POST['status']
    cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True,status="Active",pk=pk)
    delivery_date=timezone.now()
    if status == 'Delivered':
        cart_items.update(status=status, delivery_date=delivery_date)

    items = CartItems.objects.filter(item__created_by=request.user, ordered=True, status="Active").order_by(
        '-ordered_date')
    context = {
        'items': items,
    }
    return render(request, 'main/pending_orders.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def pending_orders(request):
    items = CartItems.objects.filter(item__created_by=request.user, ordered=True,status="Active").order_by('-ordered_date')
    context = {
        'items':items,
    }
    return render(request, 'main/pending_orders.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def admin_dashboard(request):
    totalTable=TableOrders.objects.count()
    totalCategory =Category.objects.count()
    totalitem =Item.objects.count()
    pending_total = CartItems.objects.filter(item__created_by=request.user, ordered=True,status="Active").count()
    completed_total = CartItems.objects.filter(item__created_by=request.user, ordered=True,status="Delivered").count()
    count1 = CartItems.objects.filter(item__created_by=request.user, ordered=True,item="3").count()
    count2 = CartItems.objects.filter(item__created_by=request.user, ordered=True,item="4").count()
    count3 = CartItems.objects.filter(item__created_by=request.user, ordered=True,item="5").count()
    total = CartItems.objects.filter(item__created_by=request.user, ordered=True).aggregate(Sum('item__price'))
    income = total.get("item__price__sum")
    context = {
        'pending_total' : pending_total,
        'completed_total' : completed_total,
        'income' : income,
        'count1' : count1,
        'count2' : count2,
        'count3' : count3,
        'totalCategory':totalCategory,
        'totalItem': totalitem,
        'totalTable': totalTable,
    }
    return render(request, 'main/admin_dashboard.html', context)

