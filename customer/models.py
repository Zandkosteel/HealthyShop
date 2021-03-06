from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from country.models import Country, State, City

class Guest_Profile(models.Model):
    """ Profile for quest user """
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'guest email: {}'.format(self.email)



class Profile(models.Model):
    """Profile for auth user"""
    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        related_name='user_profile',
        on_delete=models.CASCADE)
    first_name = models.CharField("Имя", max_length=120, default="")
    last_name = models.CharField("Фамилия", max_length=120, default="")
    company_name = models.CharField("Компания", max_length=120, blank=True, default="")
    country = models.ForeignKey(
        Country,
        verbose_name='Страна',
        default="1",
        #blank =True,
        null=True,
        on_delete=models.SET_NULL)
    state = models.ForeignKey(
        State,
        verbose_name='Республика/Штат',
        default="1",
        null=True,
        #blank=True,
        on_delete=models.SET_NULL)
    city = models.ForeignKey(
        City,
        verbose_name='Город',
        default="1",
        null=True,
        #blank=True,
        on_delete=models.SET_NULL)
    address = models.CharField("Адрес", max_length=250, default="")
    second_address = models.CharField("second_address", max_length=250, default="")
    email = models.EmailField(max_length=250, default="")
    postcode = models.CharField("Индекс", max_length=120, default="")
    phone = models.IntegerField("Телефон", default=790000000)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return "Id:{}, {} {}".format(self.id, self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.user.id})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя при регистрации"""
    if created:
        Profile.objects.create(user=instance, id=instance.id)

@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
