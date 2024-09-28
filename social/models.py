from django.db import models
from django.contrib.auth.models import User
import uuid
from uuid import uuid4
import os
# =============================================================================================================

def get_image_upload_path(instance, filename):
    # Récupérer le nom du modèle associé à l'instance
    model_name = instance.__class__.__name__.lower()
    # Créer un nouveau nom de fichier unique
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    # Retourner le chemin complet pour l'enregistrement de l'image
    return os.path.join('images', model_name, filename)




class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_page = models.CharField(
        ("Nom de la page de l'utilisateur"), max_length=50)
    pays = models.CharField(("pays de l'utilisateur"), max_length=50)
    ville = models.CharField(("ville de l'utilisateur"), max_length=50)
    date_creation = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.nom_page)

#ERREUR MAIS J'AI VU TROP TARD POUR MODIFIER DSL A CELUI QUI CONTINUE LE CODE NORMALEMENT IMAGE DEVAIS DIRECTEMENT ETRE DANS PROFILE AVEC UN NULL A TRUE
class PhotProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    photo_profil = models.ImageField(
        ("Photo de profils de l'utilisateur"), blank=True, null=True, upload_to='profil')


class NombreTotalDeFollower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.OneToOneField(Profile, on_delete=models.CASCADE)
    nombre_follower = models.IntegerField(default=0)

    @property
    def incrementer_follower(self):
        self.nombre_follower += 1
        self.save()

    @property
    def decrementer_follower(self):
        if self.nombre_follower > 0:
            self.nombre_follower -= 1
            self.save()

    def __str__(self):
        return str(self.page.nom_page)


class NomDesFollower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return str(self.page)

# =============================================================================================================


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    type = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.page)


class ImagePost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_upload_path)


class Commentaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='commentaires')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    @property
    def get_reponses(self):
        return ReponseCommentaire.objects.filter(commentaire=self)

    def __str__(self):
        return str(self.id)


class ReponseCommentaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentaire = models.ForeignKey(
        Commentaire, on_delete=models.CASCADE, related_name='reponses')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)



# =============================================OFFRES================================================================


class Offre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(Profile, on_delete=models.CASCADE)
    nom_offre = models.CharField((""), max_length=50)
    content = models.TextField(max_length=250)
    categorie = models.CharField(max_length=12)
    indisponible = models.BooleanField(default = False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.page)


class ImageOffre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    offre = models.ForeignKey(
        Offre, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_upload_path)



# =============================================MarkertPlace================================================================


class MarkertPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(Profile, on_delete=models.CASCADE)
    nom_produit = models.CharField((""), max_length=50)
    content = models.TextField(max_length=250) # description
    categorie = models.CharField(max_length=12)
    prix = models.CharField(max_length=8)
    prix_promotion = models.CharField(max_length=8,default="0")
    en_promotion = models.BooleanField(default = False)
    indisponible = models.BooleanField(default = False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.page)


class ImageMarkertPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    markertPlace = models.ForeignKey(
        MarkertPlace, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_upload_path)