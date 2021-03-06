from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import Card, Interception, Message, Player


class PlayerCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    # The method clean_username is just copied as is from
    # django.contrib.auth.forms.UserCreationForm because we have to patch
    # the User class to the Player class in line 101 and 102.
    # TODO: Refactor this when upgrading to Django >= 1.8

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            Player._default_manager.get(username=username)
        except Player.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username')


class PlayerAdmin(UserAdmin):
    """
    Customized admin for the player model.
    """
    add_form = PlayerCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'description', 'is_staff')}),
    )
    list_display = ('username', 'score', 'playable_cards', 'is_staff')
    list_filter = ('is_staff',)
    ordering = ()
    search_fields = []


class CardAdmin(admin.ModelAdmin):
    """
    Customized admin for the card model.
    """
    list_display = ('name', 'owner', 'target', 'value', 'used')


admin.site.register(Player, PlayerAdmin)
admin.site.register(Message)
admin.site.register(Interception)
admin.site.register(Card, CardAdmin)
admin.site.unregister(Group)
