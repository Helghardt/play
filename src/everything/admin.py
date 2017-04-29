from django.contrib import admin

# Register your models here.
from everything.models import Text, Rating, InputType, Recipe, RecipeInput, LogInput, Log


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)


class TextAdmin(CustomModelAdmin):
    pass


class RatingAdmin(CustomModelAdmin):
    pass


class InputTypeAdmin(CustomModelAdmin):
    pass


class RecipeAdmin(CustomModelAdmin):
    pass


class RecipeInputAdmin(CustomModelAdmin):
    pass


class LogAdmin(CustomModelAdmin):
    pass


class LogInputAdmin(CustomModelAdmin):
    pass


admin.site.register(Text, TextAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(InputType, InputTypeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeInput, RecipeInputAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(LogInput, LogInputAdmin)