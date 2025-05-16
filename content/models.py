from django.db import models


class Budget(models.Model):
    budgetid = models.AutoField(db_column='BudgetID', primary_key=True)
    totalamount = models.FloatField(db_column='TotalAmount')
    sales_percentage = models.FloatField(db_column='SalesPercentage', default=0)
    bonus_per_activity = models.FloatField(db_column='BonusPerActivity', default=0)

    class Meta:
        db_table = 'Budget'


from django.contrib.auth.models import User

class Employees(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column='UserID',
        related_name='employee_profile',
        blank=True,
        null=True,
    )
    employeeid = models.AutoField(db_column='EmployeeID', primary_key=True)
    fullname   = models.CharField(db_column='FullName',  max_length=100)
    positionid = models.ForeignKey('Positions', on_delete=models.CASCADE, db_column='PositionID')
    salary     = models.FloatField(db_column='Salary')
    address    = models.CharField(db_column='Address',   max_length=200, blank=True, null=True)
    phone      = models.CharField(db_column='Phone',     max_length=20,  blank=True, null=True)

    class Meta:
        db_table = 'Employees'

    def __str__(self):
        return self.fullname


class Finishedgoods(models.Model):
    productid = models.AutoField(db_column='ProductID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    unitid = models.ForeignKey('Units', on_delete=models.CASCADE, db_column='UnitID')
    unit_price = models.FloatField(db_column='UnitPrice')
    quantity = models.FloatField(db_column='Quantity')
    totalamount = models.FloatField(db_column='TotalAmount')

    class Meta:
        db_table = 'FinishedGoods'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    ingredientid = models.AutoField(db_column='IngredientID', primary_key=True)
    productid = models.ForeignKey(Finishedgoods, on_delete=models.CASCADE, db_column='ProductID')
    rawmaterialid = models.ForeignKey('Rawmaterials', on_delete=models.CASCADE, db_column='RawMaterialID')
    quantity = models.FloatField(db_column='Quantity')

    class Meta:
        db_table = 'Ingredients'
        unique_together = ('productid', 'rawmaterialid')

    def __str__(self):
        return f"{self.rawmaterialid.name} для {self.productid.name}"


class Positions(models.Model):
    positionid = models.AutoField(db_column='PositionID', primary_key=True)
    positionname = models.CharField(db_column='PositionName', max_length=50)

    class Meta:
        db_table = 'Positions'

    def __str__(self):
        return self.positionname


class Productproduction(models.Model):
    productionid = models.AutoField(db_column='ProductionID', primary_key=True)
    productid = models.ForeignKey(Finishedgoods, on_delete=models.CASCADE, db_column='ProductID')
    quantity = models.FloatField(db_column='Quantity')
    productiondate = models.DateField(db_column='ProductionDate')
    employeeid = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='EmployeeID')

    class Meta:
        db_table = 'ProductProduction'


class Productsales(models.Model):
    saleid = models.AutoField(db_column='SaleID', primary_key=True)
    productid = models.ForeignKey(Finishedgoods, on_delete=models.CASCADE, db_column='ProductID')
    quantity = models.IntegerField(db_column='Quantity')
    totalamount = models.FloatField(db_column='TotalAmount')
    saledate = models.DateField(db_column='SaleDate')
    employeeid = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='EmployeeID')

    class Meta:
        db_table = 'ProductSales'


class Rawmaterialpurchases(models.Model):
    purchaseid = models.AutoField(db_column='PurchaseID', primary_key=True)
    rawmaterialid = models.ForeignKey('Rawmaterials', on_delete=models.CASCADE, db_column='RawMaterialID')
    quantity = models.FloatField(db_column='Quantity')
    totalamount = models.FloatField(db_column='TotalAmount')
    purchasedate = models.DateField(db_column='PurchaseDate')
    employeeid = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='EmployeeID')

    class Meta:
        db_table = 'RawMaterialPurchases'


class Rawmaterials(models.Model):
    rawmaterialid = models.AutoField(db_column='RawMaterialID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    unitid = models.ForeignKey('Units', on_delete=models.CASCADE, db_column='UnitID')
    quantity = models.FloatField(db_column='Quantity')
    totalamount = models.FloatField(db_column='TotalAmount')

    class Meta:
        db_table = 'RawMaterials'

    def __str__(self):
        return self.name



class Units(models.Model):
    unitid = models.AutoField(db_column='UnitID', primary_key=True)
    unitname = models.CharField(db_column='UnitName', max_length=50)

    class Meta:
        db_table = 'Units'

    def __str__(self):
        return self.unitname


class Salaries(models.Model):
    salaryid = models.AutoField(primary_key=True)
    employeeid = models.ForeignKey('Employees', on_delete=models.CASCADE, db_column='employeeid')  # поле employeeid является внешним ключом
    year = models.IntegerField()
    month = models.IntegerField()
    purchase_count = models.IntegerField(default=0)
    production_count = models.IntegerField(default=0)
    sale_count = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    bonus_percent = models.FloatField(default=0.0)
    total_salary = models.FloatField(default=0.0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employeeid', 'year', 'month')

    def __str__(self):
        return f"Salary for {self.employeeid} - {self.year}-{self.month}"


class Credit(models.Model):
    creditid = models.AutoField(db_column='CreditID', primary_key=True)
    amount = models.FloatField(db_column='Amount')  # Сумма кредита
    interest = models.FloatField(db_column='Interest')  # Процент по кредиту
    credit_date = models.DateField(db_column='CreditDate')  # Дата получения кредита
    months = models.IntegerField(db_column='Months')  # Количество месяцев на погашение
    late_fee = models.FloatField(db_column='LateFee', default=0.0)  # Пени
    next_due = models.DateField(db_column='NextDue', null=True, blank=True)
    is_paid_off = models.BooleanField(db_column='IsPaidOff', default=False)
    initial_amount = models.FloatField(db_column='InitialAmount')

    class Meta:
        db_table = 'Credits'
        verbose_name = 'Кредит'
        verbose_name_plural = 'Кредиты'

    def __str__(self):
        return f"Кредит №{self.creditid}, сумма: {self.amount}, проценты: {self.interest}%"

class CreditPayment(models.Model):
    paymentid = models.AutoField(db_column='PaymentID', primary_key=True)
    creditid = models.ForeignKey(Credit, on_delete=models.CASCADE, db_column='CreditID')  # Внешний ключ на кредит
    payment_date = models.DateField(db_column='PaymentDate')  # Дата платежа
    credit_part = models.FloatField(db_column='CreditPart')  # Часть кредита
    interest = models.FloatField(db_column='Interest')  # Процент
    total_amount = models.FloatField(db_column='TotalAmount')  # Общая сумма
    remaining_credit = models.FloatField(db_column='RemainingCredit')  # Остаток кредита
    overdue_days = models.IntegerField(db_column='OverdueDays', default=0)  # Просроченные дни
    total_payment = models.FloatField(db_column='TotalPayment')  # Итого
    penalty = models.FloatField(db_column='Penalty', default=0)

    class Meta:
        db_table = 'CreditPayments'
        verbose_name = 'Платеж по кредиту'
        verbose_name_plural = 'Платежи по кредитам'

    def __str__(self):
        return f"Платеж по кредиту №{self.creditid.creditid} на сумму {self.total_payment} от {self.payment_date}"


