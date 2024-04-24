from django.contrib import admin
from .models import MarkertPlace,ImageMarkertPlace,Offre,ImageOffre,Commentaire, ImagePost, Like, Profile, PhotProfile, NomDesFollower, NombreTotalDeFollower, Post, ReponseCommentaire
# Register your models here.


class ImagePostInline(admin.StackedInline):
    model = ImagePost
    extra = 1

class ImageOffreInline(admin.StackedInline):
    model = ImageOffre
    extra = 1


class ImageMarkertPlaceInline(admin.StackedInline):
    model = ImageMarkertPlace
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImagePostInline]
    # Ajout de 'page_name'
    list_display = ('page_name', 'content', 'date_creation')

    def page_name(self, obj):
        return obj.page.nom_page  # Récupération du nom de la page liée
    page_name.short_description = "Nom de la page"


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    inlines = [ImageOffreInline]
    # Ajout de 'page_name'
    list_display = ('page_name', 'content', 'date_creation')

    def page_name(self, obj):
        return obj.page.nom_page  # Récupération du nom de la page liée
    page_name.short_description = "Nom de la page"



@admin.register(MarkertPlace)
class MarkertPlaceAdmin(admin.ModelAdmin):
    inlines = [ImageMarkertPlaceInline]
    # Ajout de 'page_name'
    list_display = ('page_name', 'content', 'date_creation')

    def page_name(self, obj):
        return obj.page.nom_page  # Récupération du nom de la page liée
    page_name.short_description = "Nom de la page"



admin.site.register(Profile)
admin.site.register(PhotProfile)
admin.site.register(NomDesFollower)
admin.site.register(NombreTotalDeFollower)
admin.site.register(ImagePost)
admin.site.register(Commentaire)
admin.site.register(ReponseCommentaire)
admin.site.register(Like)
