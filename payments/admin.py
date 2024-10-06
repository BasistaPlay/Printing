from django.contrib import admin
from payments.models import Purchase, PurchaseProduct, BankDetails, GiftCode

class PurchaseProductInline(admin.TabularInline):
    model = PurchaseProduct
    extra = 0
    readonly_fields = ['product', 'quantity']

@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'account_number']


@admin.register(GiftCode)
class GiftCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'min_order_amount', 'is_valid', 'start_date', 'end_date', 'quantity', 'unlimited_usage')
    list_filter = ('is_valid', 'discount_type', 'unlimited_usage', 'start_date', 'end_date')
    search_fields = ('code',)
    ordering = ('-start_date',)

    fieldsets = (
        (None, {
            'fields': ('code', 'discount_type', 'discount_value', 'min_order_amount', 'start_date', 'end_date', 'quantity', 'unlimited_usage')
        }),
        ('Status', {
            'fields': ('is_valid',),
        }),
    )  # Ja vēlies, lai administrators nevarētu manuāli mainīt 'is_valid' statusu, bet tas būtu atkarīgs no loģikas.


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'amount', 'discount_amount', 'status', 'is_paid', 'payment_method', 'delivery_method', 'created_at')
    list_filter = ('status', 'is_paid', 'payment_method', 'delivery_method', 'created_at')
    search_fields = ('order_number', 'user__username', 'full_name', 'company_name')
    ordering = ('-created_at',)
    inlines = [PurchaseProductInline]

    fieldsets = (
        (None, {
            'fields': ('order_number', 'user', 'amount', 'discount_amount', 'payment_method', 'delivery_method', 'status', 'is_paid', 'created_at')
        }),
        ('Buyer Information', {
            'fields': ('full_name', 'phone_number', 'email', 'comments', 'company_name', 'company_registration_number', 'company_vat_number', 'company_address'),
        }),
        ('Gift Code', {
            'fields': ('gift_code',),
        }),
    )
    readonly_fields = ('created_at', 'order_number', 'discount_amount')  # Ja vēlies, lai šie lauki būtu tikai lasāmi.

    def has_add_permission(self, request):
        # Ja vēlies liegt jaunu pirkumu pievienošanu tieši no admina
        return False
