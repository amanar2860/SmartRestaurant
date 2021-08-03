from django.contrib import admin
from .models import Item, CartItems, Reviews, Category, Feedback, TableOrders
from django.db import models

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [

        ("Created By", {'fields': ["created_by"]}),
        ("Title", {'fields': ["title"]}),
        ("Image", {'fields': ["image"]}),
        ("Description", {'fields': ["description"]}),
        ("Price", {'fields': ["price"]}),
        ("Pieces", {'fields': ["pieces"]}),
        ("Instructions", {'fields': ["instructions"]}),
        ("Labels", {'fields': ["labels"]}),
        ("Label Colour", {'fields': ["label_colour"]}),
        ("Slug", {'fields': ["slug"]}),
        ("Category", {'fields': ["category"]}),
    ]
    list_display = ('id','created_by','title','description','price','labels')
    list_filter = ( 'created_by', 'title', 'labels')

class CartItemsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Order Status", {'fields' : ["status"]}),
        ("Donate Status", {'fields': ["donate_status"]}),
        ("Delivery Date", {'fields': ["delivery_date"]})

    ]
    list_display = ('id','user','item','quantity','ordered','ordered_date','delivery_date','status','donate_status')
    list_filter = ('ordered','ordered_date','status')

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user','item','review','posted_on')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoryname')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','message','date')
    list_filter = ('name', 'date')


class TableOrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','phoneno','onDate','onTime','totalperson','table_orderno','description','status','booked_on')
    list_filter = ('user', 'onDate', 'onTime','table_orderno','status')


admin.site.register(Item,ItemAdmin)
admin.site.register(CartItems,CartItemsAdmin)
admin.site.register(Reviews,ReviewsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(TableOrders,TableOrdersAdmin)


