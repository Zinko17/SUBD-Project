from django.contrib import admin
from .models import Budget, Employees, Finishedgoods, Ingredients, Positions, Productproduction, Productsales, Rawmaterialpurchases, Rawmaterials, Units, Salaries

# Настройка отображения в админке для моделей
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('budgetid', 'totalamount')
    search_fields = ('budgetid',)

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('employeeid', 'fullname', 'get_positionname', 'salary', 'phone')  # используем метод get_positionname
    list_filter = ('positionid',)
    search_fields = ('fullname', 'phone')
    ordering = ('fullname',)

    def get_positionname(self, obj):
        return obj.positionid.positionname  # возвращаем название позиции
    get_positionname.short_description = 'Position'  # метка для столбца

class FinishedgoodsAdmin(admin.ModelAdmin):
    list_display = ('productid', 'name', 'get_unitname', 'quantity', 'totalamount')  # используем метод get_unitname
    list_filter = ('unitid',)
    search_fields = ('name',)

    def get_unitname(self, obj):
        return obj.unitid.unitname  # возвращаем название единицы измерения
    get_unitname.short_description = 'Unit'  # метка для столбца

class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('ingredientid', 'get_productname', 'get_rawmaterialname', 'quantity')  # используем методы для получения имен
    list_filter = ('productid', 'rawmaterialid')
    search_fields = ('productid__name', 'rawmaterialid__name')

    def get_productname(self, obj):
        return obj.productid.name  # возвращаем имя продукта
    get_productname.short_description = 'Product'  # метка для столбца

    def get_rawmaterialname(self, obj):
        return obj.rawmaterialid.name  # возвращаем имя сырья
    get_rawmaterialname.short_description = 'Raw Material'  # метка для столбца

class PositionsAdmin(admin.ModelAdmin):
    list_display = ('positionid', 'positionname')
    search_fields = ('positionname',)

class ProductproductionAdmin(admin.ModelAdmin):
    list_display = ('productionid', 'get_productname', 'quantity', 'productiondate', 'get_employeefullname')  # используем методы для получения имен
    list_filter = ('productiondate',)
    search_fields = ('productid__name', 'employeeid__fullname')

    def get_productname(self, obj):
        return obj.productid.name  # возвращаем имя продукта
    get_productname.short_description = 'Product'  # метка для столбца

    def get_employeefullname(self, obj):
        return obj.employeeid.fullname  # возвращаем полное имя сотрудника
    get_employeefullname.short_description = 'Employee'  # метка для столбца

class ProductsalesAdmin(admin.ModelAdmin):
    list_display = ('saleid', 'get_productname', 'quantity', 'totalamount', 'saledate', 'get_employeefullname')  # используем методы для получения имен
    list_filter = ('saledate',)
    search_fields = ('productid__name', 'employeeid__fullname')

    def get_productname(self, obj):
        return obj.productid.name  # возвращаем имя продукта
    get_productname.short_description = 'Product'  # метка для столбца

    def get_employeefullname(self, obj):
        return obj.employeeid.fullname  # возвращаем полное имя сотрудника
    get_employeefullname.short_description = 'Employee'  # метка для столбца

class RawmaterialpurchasesAdmin(admin.ModelAdmin):
    list_display = ('purchaseid', 'get_rawmaterialname', 'quantity', 'totalamount', 'purchasedate', 'get_employeefullname')  # используем методы для получения имен
    list_filter = ('purchasedate',)
    search_fields = ('rawmaterialid__name', 'employeeid__fullname')

    def get_rawmaterialname(self, obj):
        return obj.rawmaterialid.name  # возвращаем имя сырья
    get_rawmaterialname.short_description = 'Raw Material'  # метка для столбца

    def get_employeefullname(self, obj):
        return obj.employeeid.fullname  # возвращаем полное имя сотрудника
    get_employeefullname.short_description = 'Employee'  # метка для столбца

class RawmaterialsAdmin(admin.ModelAdmin):
    list_display = ('rawmaterialid', 'name', 'get_unitname', 'quantity', 'totalamount')  # используем метод get_unitname
    list_filter = ('unitid',)
    search_fields = ('name',)

    def get_unitname(self, obj):
        return obj.unitid.unitname  # возвращаем название единицы измерения
    get_unitname.short_description = 'Unit'  # метка для столбца

class UnitsAdmin(admin.ModelAdmin):
    list_display = ('unitid', 'unitname')
    search_fields = ('unitname',)

class SalariesAdmin(admin.ModelAdmin):
    list_display = ('get_employee_fullname', 'year', 'month', 'total_salary', 'is_paid')
    list_filter = ('year', 'month', 'is_paid')
    search_fields = ('employeeid__fullname',)  # Поиск по полю fullname

    def get_employee_fullname(self, obj):
        return obj.employeeid.fullname  # Используем внешний ключ для получения имени сотрудника
    get_employee_fullname.short_description = 'Employee'  # Заголовок столбца




# Регистрация моделей с улучшениями
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Finishedgoods, FinishedgoodsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Positions, PositionsAdmin)
admin.site.register(Productproduction, ProductproductionAdmin)
admin.site.register(Productsales, ProductsalesAdmin)
admin.site.register(Rawmaterialpurchases, RawmaterialpurchasesAdmin)
admin.site.register(Rawmaterials, RawmaterialsAdmin)
admin.site.register(Units, UnitsAdmin)
admin.site.register(Salaries, SalariesAdmin)
