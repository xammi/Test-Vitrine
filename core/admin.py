from django.contrib import admin

from core.models import User, Location, Visit


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'registered', 'birth_date')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name')
    ordering = ('email',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'place')
    list_filter = ('country',)
    search_fields = ('city', 'place')
    ordering = ('country', 'city', 'place')


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'visited_at')
    list_filter = ('location__country',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('-visited_at',)