from django.urls import path
from content.views import *

urlpatterns = [
    path('', home_page, name='home'),

    # Raw Materials
    path('rawmaterials/', raw_materials_list, name='rawmaterials_list'),
    path('rawmaterials/create/', raw_material_create, name='raw_material_create'),
    path('rawmaterials/<int:pk>/edit/', raw_material_update, name='raw_material_update'),
    path('rawmaterials/<int:pk>/delete/', raw_material_delete, name='raw_material_delete'),

    # Finished Goods
    path('finishedgoods/', finished_goods_list, name='finishedgoods_list'),
    path('finishedgoods/create/', finished_goods_create, name='finished_goods_create'),
    path('finishedgoods/<int:pk>/edit/', finished_goods_update, name='finished_goods_update'),
    path('finishedgoods/<int:pk>/delete/', finished_goods_delete, name='finished_goods_delete'),

    # Units
    path('units/', unit_list, name='units_list'),
    path('units/create/', unit_create, name='unit_create'),
    path('units/<int:pk>/edit/', unit_update, name='unit_update'),
    path('units/<int:pk>/delete/', unit_delete, name='unit_delete'),

    path('ingredients/', ingredient_list, name='ingredients_list'),
    path('ingredient/create/<int:product_id>/', ingredient_create, name='ingredient_create'),
    path('ingredients/<int:pk>/update/', ingredient_update, name='ingredient_update'),
    path('ingredients/<int:pk>/delete/', ingredient_delete, name='ingredient_delete'),
    path('product/<int:product_id>/ingredients/', product_ingredients, name='product_ingredients'),

    path('purchase/', purchase_raw_material_view, name='purchase_raw_material'),

    path('rawmaterialpurchases/', raw_material_purchases_list, name='rawmaterialpurchases_list'),

    path('budget/', budget_list, name='budget_list'),
    path('budget/edit/<int:budget_id>/', edit_budget, name='edit_budget'),

    path('produce_product/<int:product_id>/', produce_product, name='produce_product'),
    path('productions/', productproduction_list, name='productproduction_list'),

    path('sell_product/<int:product_id>/', sell_product, name='sell_product'),
    path('product_sales_list/', productsales_list, name='product_sales_list'),

    path('salary/', salary_view, name='salary_view'),
    path('salaries/', salary_list, name='salary_list'),
    # path('update_salary/<int:salary_id>/', update_salary, name='update_salary'),

    path('credits/', credit_list, name='credit_list'),
    path('credits/new/', credit_create, name='credit_create'),
    path('credits/<int:creditid>/', credit_detail, name='credit_detail'),

    path('login/',  login_view,  name='login'),
    path('logout/', logout_view, name='logout'),

    path('employee_list/', employee_list, name='employee_list'),
    path('position_list/', position_list, name='position_list'),

    path('reports/', report_view, name='report_view'),
]
