from django.db import models
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_UPDATE
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, PeriodicTasks
from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule
from django_celery_beat import validators
from multiselectfield import MultiSelectField

from parser.tasks import fetch_and_save_to_db


class Task(LifecycleModel, models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0, "Pending"
        PROCESSING = 10, "Processing"
        FINISHED = 20, "Finished"
        FAILED = 30, "Failed"

    class Meta:
        ordering = ("-created_at",)

    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.PENDING)
    periodic_task = models.ForeignKey("ParsePeriodicTask", on_delete=models.SET_NULL, blank=True, null=True)
    errors = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Task created {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @hook(AFTER_CREATE)
    def start_celery_task(self):
        self.status = self.Status.PROCESSING
        self.save()
        return fetch_and_save_to_db.apply_async(args=[self.id], countdown=2)


class ParsePeriodicTask(LifecycleModel, models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = '1', _('Monday')
        TUESDAY = '2', _('Tuesday')
        WEDNESDAY = '3', _('Wednesday')
        THURSDAY = '4', _('Thursday')
        FRIDAY = '5', _('Friday')
        SATURDAY = '6', _('Saturday')
        SUNDAY = '0', _('Sunday')
        ALL = '*', _('All')

    class MonthOfYear(models.TextChoices):
        JANUARY = '1', _('January')
        FEBRUARY = '2', _('February')
        MARCH = '3', _('March')
        APRIL = '4', _('April')
        MAY = '5', _('May')
        JUNE = '6', _('June')
        JULY = '7', _('July')
        AUGUST = '8', _('August')
        SEPTEMBER = '9', _('September')
        OCTOBER = '10', _('October')
        NOVEMBER = '11', _('November')
        DECEMBER = '12', _('December')
        ALL = '*', _('All')

    name = models.CharField(max_length=200, unique=True)
    time = models.TimeField()
    day_of_week = MultiSelectField(
        max_length=24, choices=DayOfWeek.choices,
        verbose_name='Day(s) Of The Week',
        default=DayOfWeek.ALL, validators=[validators.day_of_week_validator])
    month_of_year = MultiSelectField(
        max_length=64, default=MonthOfYear.ALL,
        verbose_name=_('Month(s) Of The Year'), choices=MonthOfYear.choices,
        validators=[validators.month_of_year_validator],
    )
    created_at = models.DateTimeField(auto_now=True)
    periodic_task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    @hook(AFTER_CREATE)
    def setup_task(self):
        self.periodic_task = PeriodicTask.objects.create(
            name=self.name,
            task='parser.tasks.create_task',
            crontab_id=self.crontab_schedule,
            args=[self.id],
            start_time=timezone.now()
        )
        self.periodic_task.save()
        self.save()

    @property
    def crontab_schedule(self):
        cron, _ = CrontabSchedule.objects.get_or_create(
            hour=self.time.strftime("%H"),
            minute=self.time.strftime("%M"),
            day_of_week=','.join(self.day_of_week),
            month_of_year=','.join(self.month_of_year)
        )
        return cron.id

    def delete(self, *args, **kwargs):
        if self.periodic_task is not None:
            self.periodic_task.delete()
            PeriodicTasks.changed(self.periodic_task)
        return super().delete(*args, **kwargs)


class Product(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, related_name='products')
    created_at = models.DateTimeField(auto_now=True)
    product_id = models.PositiveIntegerField()
    product_name = models.TextField()
    product_name_uk = models.TextField(blank=True, null=True)
    search_requests = models.CharField(max_length=255, blank=True, null=True)
    search_requests_uk = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_uk = models.TextField(blank=True, null=True)
    product_type = models.CharField(max_length=10, default="r", blank=True, null=True)
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default="UAH", blank=True, null=True)
    unit_of_measurement = models.CharField(max_length=10, default="шт.", blank=True, null=True)
    image_link = models.TextField(blank=True, null=True)
    availability = models.CharField(max_length=10, default="+", blank=True, null=True)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    packing_method = models.CharField(max_length=255, blank=True, null=True)
    packing_method_uk = models.CharField(max_length=255, blank=True, null=True)
    vendor = models.CharField(max_length=255, blank=True, null=True)
    html_header = models.TextField(blank=True, null=True)
    html_header_uk = models.TextField(blank=True, null=True)
    html_keywords = models.CharField(max_length=255, blank=True, null=True)
    html_keywords_uk = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    width = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    length = models.CharField(max_length=50, blank=True, null=True)
    unique_identificator = models.PositiveIntegerField(default=0)
    product_identificator = models.PositiveIntegerField(default=0)
