from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources
from import_export.fields import Field
from rangefilter.filters import DateRangeFilter

from parser.models import Task, ParsePeriodicTask, Product


class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'created_at', 'status')
    search_fields = ('name',)
    fields = ('name', 'created_at', 'status', 'errors')
    readonly_fields = ('created_at', 'status', 'errors')


class ParsePeriodicTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time')
    search_fields = ('name',)
    fields = ('name', 'time', 'day_of_week', 'month_of_year')


class ProductResource(resources.ModelResource):
    product_id = Field(attribute="product_id", column_name="Код_товара")
    product_name = Field(attribute="product_name", column_name="Название_позиции")
    product_name_uk = Field(attribute="product_name_uk", column_name="Название_позиции_укр")
    search_requests = Field(attribute="search_requests", column_name="Поисковые_запросы")
    search_requests_uk = Field(attribute="search_requests_uk", column_name="Поисковые_запросы_укр")
    description = Field(attribute="description", column_name="Описание")
    description_uk = Field(attribute="description_uk", column_name="Описание_укр")
    product_type = Field(attribute="product_type", column_name="Тип_товара")
    price = Field(attribute="price", column_name="Цена")
    currency = Field(attribute="currency", column_name="Валюта")
    unit_of_measurement = Field(attribute="unit_of_measurement", column_name="Единица_измерения")
    image_link = Field(attribute="image_link", column_name="Ссылка_изображения")
    availability = Field(attribute="availability", column_name="Наличие")
    group_name = Field(attribute="group_name", column_name="Название_группы")
    packing_method = Field(attribute="packing_method", column_name="Способ_упаковки")
    packing_method_uk = Field(attribute="packing_method_uk", column_name="Способ_упаковки_укр")
    unique_identificator = Field(attribute="unique_identificator", column_name="Уникальный_идентификатор")
    product_identificator = Field(attribute="product_identificator", column_name="Идентификатор_товара")
    vendor = Field(attribute="vendor", column_name="Производитель")
    html_header = Field(attribute="html_header", column_name="HTML_заголовок")
    html_header_uk = Field(attribute="html_header_uk", column_name="HTML_заголовок_укр")
    html_description = Field(attribute="description", column_name="HTML_описание")
    html_description_uk = Field(attribute="description_uk", column_name="HTML_описание_укр")
    html_keywords = Field(attribute="html_keywords", column_name="HTML_ключевые_слова")
    html_keywords_uk = Field(attribute="html_keywords_uk", column_name="HTML_ключевые_слова_укр")
    weight = Field(attribute="weight", column_name="Вес,кг")
    width = Field(attribute="width", column_name="Ширина,см")
    height = Field(attribute="height", column_name="Высота,см")
    length = Field(attribute="length", column_name="Длина,см")

    class Meta:
        model = Product
        exclude = ('id', 'task', 'created_at')


class ProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('product_name', 'created_at')
    search_fields = ('product_name',)
    list_filter = (('created_at', DateRangeFilter,),)
    readonly_fields = ('created_at',)
    resource_class = ProductResource

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in Product._meta.fields]


admin.site.register(Task, TaskAdmin)
admin.site.register(ParsePeriodicTask, ParsePeriodicTaskAdmin)
admin.site.register(Product, ProductAdmin)
