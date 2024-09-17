from django.contrib import admin
from payments.models import Purchase, PurchaseProduct, BankDetails

class PurchaseProductInline(admin.TabularInline):
    model = PurchaseProduct
    extra = 0
    readonly_fields = ['product', 'quantity']

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'amount', 'user', 'status', 'created_at')
    search_fields = ('order_number', 'user__username')
    list_filter = ('status', 'created_at')
    readonly_fields = ['order_number', 'amount', 'user', 'created_at']
    inlines = [PurchaseProductInline]

admin.site.register(Purchase, PurchaseAdmin)


@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'account_number']