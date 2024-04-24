from ninja import Router, File, Form,UploadedFile
from django.contrib.auth.models import User
from ninja.errors import HttpError
from typing import List, Optional
from core.token import verify_token
from social.models import Commentaire, ImageMarkertPlace, ImageOffre, ImagePost, Like, MarkertPlace, NomDesFollower, NombreTotalDeFollower, Offre, PhotProfile, Post, Profile, ReponseCommentaire
from social.schemas import CommentSchema, FollowerSchema, GetProfileSchema, LikeSchema, PostSchema, ProfileSchema, ReplyCommentSchema, UpdateProfileSchema
import json
from django.http import JsonResponse
from ninja.pagination import paginate

router = Router()


# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =====================================================PROFILE=============================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================


# =============================AJOUTER UN PROFIL=================================================


@router.post('profile', tags=['CREATE PROFILES ROUTER'])
def profile(request, data: ProfileSchema,file: UploadedFile = File(...)):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        p = Profile.objects.create(
            user=u, nom_page=data.nom_page, pays=data.pays, ville=data.ville)
        NombreTotalDeFollower.objects.create(page=p)
        if file:
            PhotProfile.objects.create(profile=p, photo_profil=file)
        return 200
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")


# =============================AJOUTER UNE IMAGE AU PROFIL=================================================
@router.post('profile_image', tags=['ADD PROFILES IMAGE ROUTER'])
def profile_image(request, file: UploadedFile = File(...)):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        p = Profile.objects.filter(user=u).first()
        i = file
        PhotProfile.objects.create(profile=p, photo_profil=i)
        return 200
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")

# =============================RECUPERER UN PROFIL==============================================================



@router.get('infos_profile', tags=['INFORMATION PROFILES'])
def infos_profile(request):
    infos = []
    token = request.headers.get("Authorization").split(" ")[1]
    user_id = verify_token(token)
    u = User.objects.filter(id=user_id).first()
    page = Profile.objects.filter(user=u).first()
    image = PhotProfile.objects.filter(profile=page).first()
    post_count = Post.objects.filter(page=page).count()
    follower_count = NombreTotalDeFollower.objects.filter(page=page).count()
    info = {
        'nom_page': page.nom_page,
        'nombre_post': post_count,
        'follower': follower_count,
        'pays':page.pays,
        'ville':page.ville,
        'profile': image.photo_profil.url if image else None  # Handle case where image is not found
    }
    return JsonResponse({"data": info, "status": 200})


@router.get('get_profile', tags=['GET PROFILES ROUTER'])
def get_profile(request,current: int = 10, offset: int = 0):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        page = Profile.objects.filter(user = u).first()
        posts_with_images = []
        posts = Post.objects.filter(page = page)[offset:offset+current]
        if posts :
            print('current : ',current)
            for post in posts:
                profile = Profile.objects.get(id=post.page.id)
                images = [image.image.url for image in post.images.all()]
                is_liked = Like.objects.filter(user=u, post=post.id).exists()
                profile = Profile.objects.get(id=post.page.id)
                is_following = NomDesFollower.objects.filter(page=profile, user=u).exists()
                profile_data = {
                    "nom_page": profile.nom_page,
                    "number":profile.user.username,
                    'isFollow': is_following,
                    "photo_profil": profile.photoprofile.photo_profil.url if hasattr(profile, 'photoprofile') and profile.photoprofile else None
                }
                likes_count = post.likes.count()
                post_data = {
                    "id": post.id,
                    "page": profile_data,
                    "content": post.content,
                    "date_creation": post.date_creation,
                    "images": images,
                    'post_likes_count':likes_count,
                    'isLike': is_liked,
                }
                posts_with_images.append(post_data)
            return posts_with_images
        else:
            return []
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")
    

#DSL A CELUI OU CELLE QUI VAS MODIFIER LE CODE SI C'EST PAS MOI IL FAUT SEPARER LES RESPONSABILITER DU PUT ET DU POST JE ME SUIS RENDU COMPTE DE CELA A LA FIN DU PROJET
# =============================MODIFIER LE PROFIL=================================================
@router.post('modifier_profile', tags=['MODIFIE PROFILES ROUTER'])
def modifier_profile(request, nom_page: str = Form(...), pays: str = Form(...), ville: str = Form(...), file: UploadedFile = None):
    token = request.headers.get("Authorization").split(" ")[1]
    user_id = verify_token(token)
    u = User.objects.filter(id=user_id).first()
    print('nom_page=',nom_page, 'pays=',pays, 'ville=',ville)
    profile, created = Profile.objects.get_or_create(user=u,nom_page= nom_page, pays=pays, ville=ville)
    if not created:
        if nom_page:
            profile.nom_page = nom_page
        if pays:
            profile.pays = pays
        if ville:
            profile.ville = ville
        profile.save()

    if file:
        photo, created = PhotProfile.objects.get_or_create(profile=profile)
        photo.photo_profil = file
        photo.save()

    profile.save()
    is_Page = Profile.objects.filter(user = u).exists()
    return {"status": 200,'is_Page':is_Page}



# =============================MODIFIER UNE IMAGE DE PROFIL=================================================


@router.put('modifier_profile_image', tags=['MODIFIE PROFILES IMAGE ROUTER'])
def modifier_profile_image(request, file: UploadedFile = None):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        p = Profile.objects.filter(user=u).first()
        if p:
            photo = PhotProfile.objects.filter(profile=p).first()
            photo.photo_profil = file
            photo.save()
            return 200
        else:
            raise HttpError(status_code=404, message="ce profil n'existe pas")
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")


# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =====================================================FOLLOWER============================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================


# =============================AJOUTER FOLLOWER=====================================================================


@router.post('ajouter_follower', tags=['ADD FOLLOWER ROUTER'])
def ajouter_follower(request, data: FollowerSchema):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        p = Profile.objects.filter(nom_page=data.nom_page).first()
        NomDesFollower.objects.create(
            page=p,user=u)

        return 200
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite++")


# =============================RETIRER FOLLOWER=====================================================================


@router.post('retirer_follower', tags=['REMOVE FOLLOWER ROUTER'])
def retirer_follower(request, data: FollowerSchema):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        p = Profile.objects.filter(nom_page=data.nom_page).first()
        NombreTotalDeFollower.objects.filter(
            page=p).first().decrementer_follower
        NomDesFollower.objects.filter(
            page=p, nom_follower=u.first_name, user_id=user_id).first().delete()

        return 200
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")


# =============================RECUPERER LES FOLLOWER=====================================================================


@router.get('recuperer_follower', tags=['GET FOLLOWER ROUTER'])
def recuperer_follower(request, data: FollowerSchema):
    token = request.headers.get("Authorization").split(" ")[1]
    user_id = verify_token(token)
    u = User.objects.filter(id=user_id).first()
    p = Profile.objects.filter(nom_page=data.nom_page).first()
    totals = NombreTotalDeFollower.objects.filter(
        page=p).first()
    noms = NomDesFollower.objects.filter(
        page=p)
    response_data = {
        'totals': totals.nombre_follower,
        'noms': [nom.nom_follower for nom in noms]
    }

    return JsonResponse({"data": response_data, "status": 200})


# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =====================================================POST============================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================


# ===========================================SAVE POST=====================================================================
@router.post('save_post', tags=['SAVE POST ROUTER'])
def save_post(request, type: str = Form(...),description: str = Form(...), files: List[UploadedFile] = None):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        p = Profile.objects.filter(user=u).first()
        if p:
            post = Post.objects.create(page=p, content=description,type=type)
            if files:
                for file in files:
                    ImagePost.objects.create(post=post, image=file)
        return 200
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")

# ===========================================GET POST=====================================================================
@router.get('get_post', tags=['GET POST ROUTER'])
def get_post(request,current: int = 10, offset: int = 0):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        posts_with_images = []
        posts = Post.objects.all()[offset:offset+current]
        if posts :
            print('current : ',current)
            for post in posts:
                profile = Profile.objects.get(id=post.page.id)
                images = [image.image.url for image in post.images.all()]
                is_liked = Like.objects.filter(user=u, post=post.id).exists()
                profile = Profile.objects.get(id=post.page.id)
                is_following = NomDesFollower.objects.filter(page=profile, user=u).exists()
                profile_data = {
                    "nom_page": profile.nom_page,
                    "number":profile.user.username,
                    'isFollow': is_following,
                    "photo_profil": profile.photoprofile.photo_profil.url if hasattr(profile, 'photoprofile') and profile.photoprofile else None
                }
                likes_count = post.likes.count()
                post_data = {
                    "id": post.id,
                    "page": profile_data,
                    "content": post.content,
                    "date_creation": post.date_creation,
                    "images": images,
                    'post_likes_count':likes_count,
                    'isLike': is_liked,
                }
                posts_with_images.append(post_data)
            return posts_with_images
        else:
            return []
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")


# ===========================================GET POST WICH TYPES=====================================================================
@router.get('get_post_type', tags=['GET POST ROUTER'])
def get_post_type(request,type:str,current: int = 10, offset: int = 0):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        posts_with_images = []
        posts = Post.objects.filter(type__icontains = type)[offset:offset+current]
        if posts :
            print('current : ',current)
            for post in posts:
                profile = Profile.objects.get(id=post.page.id)
                images = [image.image.url for image in post.images.all()]
                is_liked = Like.objects.filter(user=u, post=post.id).exists()
                profile = Profile.objects.get(id=post.page.id)
                is_following = NomDesFollower.objects.filter(page=profile, user=u).exists()
                profile_data = {
                    "nom_page": profile.nom_page,
                    "number":profile.user.username,
                    'isFollow': is_following,
                    "photo_profil": profile.photoprofile.photo_profil.url if hasattr(profile, 'photoprofile') and profile.photoprofile else None
                }
                likes_count = post.likes.count()
                post_data = {
                    "id": post.id,
                    "page": profile_data,
                    "content": post.content,
                    "date_creation": post.date_creation,
                    "images": images,
                    'post_likes_count':likes_count,
                    'isLike': is_liked,
                }
                posts_with_images.append(post_data)
            return posts_with_images
        else:
            return []
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")

   
#############dELETE POST

@router.delete('delete_post/{id}/{type}',tags=["SUPPRIMER UN POST"])
def deletePOM(request,id:str,type:str):
    response = {}
    if type == "post":
        try:
            post = Post.objects.get(id=id)
            post.delete()
            response['message'] = 'Publication supprimée avec succès.'
            # response['items'] = list(Post.objects.filter())
        except Post.DoesNotExist:
            response['error'] = 'La publication n\'existe pas.'
    elif type == "offre":
        try:
            offre = Offre.objects.get(id=id)
            offre.delete()
            response['message'] = 'Offre supprimée avec succès.'
            # response['items'] = list(Offre.objects.all())
        except Offre.DoesNotExist:
            response['error'] = 'L\'offre n\'existe pas.'
    elif type == "marketplace":
        try:
            marketplace = MarkertPlace.objects.get(id=id)
            marketplace.delete()
            response['message'] = 'Place de marché supprimée avec succès.'
            # response['items'] = list(MarkertPlace.objects.all())
        except MarkertPlace.DoesNotExist:
            response['error'] = 'La place de marché n\'existe pas.'
    else:
        response['error'] = 'Type fourni invalide. Veuillez fournir "post", "offre" ou "marketplace".'

    return response



# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =====================================================COMMENTAIRE=========================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================


# ===========================================SAVE COMMENT==================================================================
@router.post('save_comment', tags=['SAVE COMMENT ROUTER'])
def save_comment(request, data: CommentSchema):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        post = Post.objects.filter(id=data.post_id).first()
        Commentaire.objects.create(user=u, post=post, contenu=data.content)
        return 200
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")


# ===========================================GET COMMENT==================================================================
@router.get('get_comment/{post_id}', tags=['GET WITCH REPLY COMMENT ROUTER'])
def get_comment(request, post_id: str):
    token = request.headers.get("Authorization").split(" ")[1]
    user_id = verify_token(token)
    u = User.objects.filter(id=user_id).first()
    post = Post.objects.filter(id=post_id).first()
    comments = Commentaire.objects.filter(post=post)
    responses = ReponseCommentaire.objects.filter(
        commentaire__post=post).order_by('date_creation')
    print([c.contenu for c in comments])
    # Prepare the response data
    response_data = {
        'post_id': post_id,
        'comments': [
            {
                'id': comment.id,
                'user': comment.user.username,
                'contenu': comment.contenu,
                'date_creation': comment.date_creation.strftime("%d-%m-%Y %H:%M:%S"),
                'responses': [
                    {
                        'id': response.id,
                        'user': response.user.username,
                        'contenu': response.contenu,
                        'date_creation': response.date_creation.strftime("%d-%m-%Y %H:%M:%S"),
                    }
                    for response in responses.filter(commentaire=comment)
                ]
            }
            for comment in comments
        ]
    }
    # Return the response data as JSON
    return JsonResponse(response_data, status=200)


# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =====================================================ReponseCommentaire=========================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================


# ===========================================SAVE REPLY==================================================================
@router.post('save_reply', tags=['SAVE REPLY ROUTER'])
def save_reply(request, data: ReplyCommentSchema):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        c = Commentaire.objects.filter(id=data.comment_id).first()
        ReponseCommentaire.objects.create(
            user=u, commentaire=c, contenu=data.content)
        return 200
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")


# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =====================================================Like=========================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================


# ===========================================SAVE LIKE==================================================================
@router.post('save_like', tags=['SAVE Like ROUTER'])
def save_like(request, data: LikeSchema):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        post = Post.objects.filter(id=data.post_id).first()
        isLike = Like.objects.filter(user=u, post=post).exists()
        if(isLike):
            Like.objects.filter(user=u, post=post).first().delete()
            return post.likes.count()
        else:
            Like.objects.create(user=u, post=post)
        return post.likes.count()
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")

# ===========================================DELETE LIKE==================================================================

# @router.delete('delete_like', tags=['DELETE Like ROUTER'])
# def save_delete(request, data: LikeSchema):
#     try:
#         token = request.headers.get("Authorization").split(" ")[1]
#         user_id = verify_token(token)
#         u = User.objects.filter(id=user_id).first()
#         post = Post.objects.filter(id=data.post_id).first()
#         Like.objects.filter(user=u, post=post).first().delete()
#         return 200
#     except:
#         raise HttpError(status_code=404, message="une erreur c'est produite")
    


# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =====================================================OFFRE============================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================


# ===========================================SAVE OFFRE=====================================================================
@router.post('save_offre', tags=['SAVE OFFRE ROUTER'])
def save_offre(request, nom_offre:str= Form(...),content: str = Form(...),categorie:str = Form(...), files: List[UploadedFile] = None):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        p = Profile.objects.filter(user=u).first()
        if p:
            offre = Offre.objects.create(page=p,nom_offre=nom_offre, content=content , categorie = categorie )
            if files:
                for file in files:
                    ImageOffre.objects.create(offre=offre, image=file)

        return 200
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")

# ===========================================GET OFFRE=====================================================================
@router.get('get_offres', tags=['GET OFFRE ROUTER'])
def get_offres(request,current: int = 10, offset: int = 0):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        offres_with_images = []
        offres = Offre.objects.all()[offset:offset+current]
        if offres :
            print('current : ',current)
            for offre in offres:
                profile = Profile.objects.get(id=offre.page.id)
                images = [image.image.url for image in offre.images.all()]
                profile = Profile.objects.get(id=offre.page.id)
                profile_data = {
                    "nom_page": profile.nom_page,
                    "number":profile.user.username,
                    "photo_profil": profile.photoprofile.photo_profil.url if hasattr(profile, 'photoprofile') and profile.photoprofile else None
                }
                offres_data = {
                    "id": offre.id,
                    "page": profile_data,
                    "content": offre.content,
                    "date_creation": offre.date_creation,
                    "images": images,
                }
                offres_with_images.append(offres_data)
            return offres_with_images
        else:
            return []
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")
    

# ===========================================GET OFFRE PROFIL=====================================================================
@router.get('get_offreprofils', tags=['GET OFFRE PROFIL ROUTER'])
def get_offreprofils(request,current: int = 10, offset: int = 0):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        offres_with_images = []
        page = Profile.objects.filter(user = u).first()
        offres = Offre.objects.filter(page = page)[offset:offset+current]
        if offres :
            print('current : ',current)
            for offre in offres:
                profile = Profile.objects.get(id=offre.page.id)
                images = [image.image.url for image in offre.images.all()]
                profile = Profile.objects.get(id=offre.page.id)
                profile_data = {
                    "nom_page": profile.nom_page,
                    "number":profile.user.username,
                    "photo_profil": profile.photoprofile.photo_profil.url if hasattr(profile, 'photoprofile') and profile.photoprofile else None
                }
                offres_data = {
                    "id": offre.id,
                    "page": profile_data,
                    "content": offre.content,
                    "date_creation": offre.date_creation,
                    "images": images,
                }
                offres_with_images.append(offres_data)
            return offres_with_images
        else:
            return []
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")
    




# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =====================================================MarkertPlace============================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================


# ===========================================SAVE MarkertPlace=====================================================================
@router.post('save_markertPlace', tags=['SAVE MarkertPlace ROUTER'])
def save_markertplace(request,nom_produit: str = Form(...),description: str = Form(...),categorie: str = Form(...),prix: str = Form(...),en_promotion: Optional[bool] = Form(None),prix_promotion: str = Form(None),files: List[UploadedFile] = File(...)):
    try:
        # Check for required fields
        if not (nom_produit and description and categorie and prix and files):
            raise HttpError(status_code=400, message="Tous les champs obligatoires doivent être fournis")

        # Your existing logic
        print("Nom du produit:", nom_produit)
        print("Description:", description)
        print("Catégorie:", categorie)
        print("Prix:", prix)
        print("Prix en promotion:", prix_promotion)
        print("En promotion:", en_promotion)
        if files:
            print("Images reçues:", files)

        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        p = Profile.objects.filter(user=u).first()
        if p:
            markertPlace = MarkertPlace.objects.create(page=p,nom_produit=nom_produit, content=description,categorie=categorie,prix = prix)
            if en_promotion:
                markertPlace.en_promotion = en_promotion
                markertPlace.prix_promotion = prix_promotion
                markertPlace.save()
            if files:
                for file in files:
                    ImageMarkertPlace.objects.create(markertPlace=markertPlace, image=file)
        return JsonResponse({"message": "Le produit a été ajouté avec succès sur la marketplace"}, status=200)
    except :
        raise HttpError(status_code=404, message="une erreur c'est produite")



# ===========================================GET MarkertPlace=====================================================================
@router.get('get_markertPlace', tags=['GET MarkertPlace ROUTER'])
def get_markertPlace(request,current: int = 10, offset: int = 0):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        markertPlace_with_images = []
        markertPlaces = MarkertPlace.objects.all()[offset:offset+current]
        if u :
            print('current : ',current)
            for markertPlace in markertPlaces:
                profile = Profile.objects.get(id=markertPlace.page.id)
                images = [image.image.url for image in markertPlace.images.all()]
                profile = Profile.objects.get(id=markertPlace.page.id)
                profile_data = {
                    "nom_page": profile.nom_page,
                    "number":profile.user.username,
                    "photo_profil": profile.photoprofile.photo_profil.url if hasattr(profile, 'photoprofile') and profile.photoprofile else None
                }
                markertPlaces = {
                    "id": markertPlace.id,
                    "page": profile_data,
                    "content": markertPlace.content,
                    "prix_promotion":markertPlace.prix_promotion,
                    "prix":markertPlace.prix,
                    "en_promotion":markertPlace.en_promotion,
                    "date_creation": markertPlace.date_creation,
                    "images": images,
                }
                markertPlace_with_images.append(markertPlaces)
            return markertPlace_with_images
        else:
            return []
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")
    

# ===========================================GET MarkertPlace Profile=====================================================================
@router.get('get_markertPlaceProfile', tags=['GET MarkertPlace ROUTER'])
def get_markertPlaceProfile(request,current: int = 10, offset: int = 0):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = verify_token(token)
        u = User.objects.filter(id=user_id).first()
        markertPlace_with_images = []
        page = Profile.objects.filter(user = u).first()
        markertPlaces = MarkertPlace.objects.filter(page = page)[offset:offset+current]
        if u :
            print('current : ',current)
            for markertPlace in markertPlaces:
                profile = Profile.objects.get(id=markertPlace.page.id)
                images = [image.image.url for image in markertPlace.images.all()]
                profile = Profile.objects.get(id=markertPlace.page.id)
                profile_data = {
                    "nom_page": profile.nom_page,
                    "number":profile.user.username,
                    "photo_profil": profile.photoprofile.photo_profil.url if hasattr(profile, 'photoprofile') and profile.photoprofile else None
                }
                markertPlaces = {
                    "id": markertPlace.id,
                    "page": profile_data,
                    "content": markertPlace.content,
                    "prix_promotion":markertPlace.prix_promotion,
                    "prix":markertPlace.prix,
                    "en_promotion":markertPlace.en_promotion,
                    "date_creation": markertPlace.date_creation,
                    "images": images,
                }
                markertPlace_with_images.append(markertPlaces)
            return markertPlace_with_images
        else:
            return []
    except:
        raise HttpError(status_code=404, message="une erreur c'est produite")