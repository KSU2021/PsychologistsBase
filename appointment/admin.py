from django import forms
from django.contrib import admin

from appointment.models import Appointment, AppointmentItem
from psychologists.models import Psychologist


class AppointmentAdminForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('status', 'user')


class AppointmentItemsInLine(admin.TabularInline):
    model = AppointmentItem
    extra = 1

class TotalSumFilter(admin.SimpleListFilter):
    title = 'Фильтрация по сумме заказа'
    parameter_name = 'total_sum'

    def lookups(self, request, model_admin):
        return (
            ('0to50000', 'от 0 до 50000'),
            ('50000to100000', 'от 50,000 до 100,000'),
            ('100000to150000', 'от 100,000 до 150,000'),
            ('from150000', 'от 150,000 и выше'),
        )
    def queryset(self, request, queryset): #список в листинге
        if self.value() == '0to50000':
            return queryset.filter(total_sum__lte=50000)
        elif self.value() == '50000to100000':
            return queryset.filter(total_sum__range=[50000, 100000])
        elif self.value() == '100000to150000':
            return queryset.filter(total_sum__range=[100000, 150000])
        elif self.value() == 'from150000':
            return queryset.filter(total_sum__gte=150000)
        else:
            return queryset


class AppointmentAdmin(admin.ModelAdmin):
    inlines = [
        AppointmentItemsInLine
    ]
    exclude = ('psychologist', )
    form = AppointmentAdminForm
    readonly_fields = ['user', 'total', 'created_at']
    list_display = ['id', 'status', 'total', 'created_at']
    list_filter = ['status', 'psychologist', TotalSumFilter]
    search_fields = ['psychologist__last_name' , 'psychologist__name']
    list_display_links = ['id', 'status']


    def save_model(self, request, obj, form, change): #change - change - true, create - false
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        total = 0
        for inline_form in formset:
            if inline_form.cleaned_data:
                price_online = inline_form.cleaned_data['psychologist'].price_per_hour_online
                hours_online = inline_form.cleaned_data['hours_online']
                price_offline = inline_form.cleaned_data['psychologist'].price_per_hour_offline
                hours_offline = inline_form.cleaned_data['hours_offline']
                total += price_online * hours_online + price_offline * hours_offline
                # date = inline_form.cleaned_data['date']
                # time = inline_form.cleaned_data['time']
        form.instance.total_sum = total
        form.instance.save()
        formset.save()

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(AppointmentItem)


