from datetime import date
from django.utils.timezone import now
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from content.models import *

class RawmaterialsForm(forms.ModelForm):
    class Meta:
        model = Rawmaterials
        exclude = ['quantity', 'totalamount']

class FinishedgoodsForm(forms.ModelForm):
    class Meta:
        model = Finishedgoods
        exclude = ['quantity', 'totalamount']

class UnitsForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = '__all__'

from django import forms
from .models import Ingredients


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['productid', 'rawmaterialid', 'quantity']

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        if product_id:
            self.fields['productid'].initial = product_id
            self.fields['productid'].widget.attrs['readonly'] = True


class RawMaterialPurchaseForm(forms.ModelForm):
    unit_price = forms.FloatField(label="Цена за единицу", min_value=0)  # Добавляем поле

    class Meta:
        model = Rawmaterialpurchases
        fields = ['rawmaterialid', 'quantity', 'unit_price', 'purchasedate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rawmaterialid'].queryset = Rawmaterials.objects.all()
        self.fields['purchasedate'].initial = date.today()

    def clean(self):
        cleaned_data = super().clean()
        raw_material = cleaned_data.get("rawmaterialid")
        quantity = cleaned_data.get("quantity")
        unit_price = cleaned_data.get("unit_price")

        if raw_material and quantity and unit_price:
            budget = Budget.objects.first()
            cost = unit_price * quantity  # Считаем стоимость закупки

            if budget and budget.totalamount < cost:
                raise ValidationError(f'Недостаточно средств в бюджете! Требуется {cost}, доступно {budget.totalamount}.')

        return cleaned_data


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['totalamount', 'sales_percentage']
        labels = {'totalamount': 'Общая сумма', 'sales_percentage': 'Процент продажи'}

        sales_percentage = forms.FloatField(
            validators=[MinValueValidator(0), MaxValueValidator(300)],
            label="Процент наценки"
        )


class ProductProductionForm(forms.ModelForm):
    class Meta:
        model = Productproduction
        fields = ['productid', 'quantity', 'productiondate', 'employeeid']
        labels = {
            'productid': 'Продукт',
            'quantity': 'Количество',
            'productiondate': 'Дата производства',
            'employeeid': 'Сотрудник',
        }


class ProductProductionForm(forms.ModelForm):
    class Meta:
        model = Productproduction
        fields = ['quantity', 'productiondate']  # Убираем поле 'employeeid' из формы
        widgets = {
            'productiondate': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем сегодняшнюю дату по умолчанию
        self.fields['productiondate'].initial = timezone.now().date()

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Количество должно быть больше 0.")
        return quantity



class ProductSaleForm(forms.ModelForm):
    class Meta:
        model = Productsales
        fields = ['productid', 'quantity', 'saledate']
        labels = {
            'productid': 'Продукт',
            'quantity': 'Количество',
            'saledate': 'Дата продажи',
        }
        widgets = {
            'saledate': forms.DateInput(attrs={'type': 'date'}),
        }

    quantity = forms.IntegerField(
        validators=[MinValueValidator(1)],
        label="Количество",
        help_text="Введите целое число больше 0"
    )

    saledate = forms.DateField(
        initial=now().date(),
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата продажи"
    )

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)

        if product_id:
            self.fields['productid'].queryset = Finishedgoods.objects.filter(productid=product_id)
            self.fields['productid'].initial = product_id
            self.fields['productid'].widget.attrs['readonly'] = True


class CreditForm(forms.Form):
    amount      = forms.FloatField(label="Сумма кредита")
    interest    = forms.FloatField(label="Годовая ставка (%)")
    credit_date = forms.DateField(label="Дата получения", widget=forms.DateInput(attrs={'type':'date'}))
    months      = forms.IntegerField(label="Срок (мес.)")
    late_fee    = forms.FloatField(label="Ставка пени (%/день)")

class PaymentDateForm(forms.Form):
    payment_date = forms.DateField(
        label="Дата платежа",
        widget=forms.DateInput(attrs={'type':'date'})
    )

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


REPORT_CHOICES = [
    ('purchases',   'Закупки сырья'),
    ('production',  'Производство'),
    ('sales',       'Продажи'),
    ('salaries',    'Выплаченные зарплаты'),
    ('credit_pay',  'Платежи по кредитам'),
]

REPORT_CHOICES = [
    ('purchases', 'Отчёт о закупках сырья'),
    ('sales', 'Отчёт о продажах продукции'),
    ('production', 'Отчет о производстве продуктов'),
    ('salaries', 'Отчет о зарлпатах'),
    ('credit_pay', 'Отчет о платежах по кредитам'),
    # Добавьте сюда нужные типы
]

REPORT_LABELS = dict(REPORT_CHOICES)

class ReportForm(forms.Form):
    report_type = forms.ChoiceField(choices=REPORT_CHOICES, label="Тип отчёта")
    start_date  = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Начальная дата')
    end_date    = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Конечная дата')

    def get_report_label(self):
        report_type = self.cleaned_data.get('report_type')
        return REPORT_LABELS.get(report_type, 'Отчёт')