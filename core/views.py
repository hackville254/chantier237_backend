from ninja import Router
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from core.code import generate_code
from core.models import Code
from core.schemas import LoginSchemas, RegisterSchemas, ResetPSchema
from core.token import create_token
from social.models import Profile

# Create your views here.

router = Router()


@router.post('register/', tags=['REGISTER ROUTER'], auth=None)
def register(request, data: RegisterSchemas):
    nom = data.nom
    username = data.username
    mdp = data.motPasse
    CmotPasse = data.CmotPasse
    u = User.objects.filter(username=username).exists()
    if u:
        raise HttpError(
            status_code=404, message=f"{username} existe déjà. Merci de changer")
    else:
        u = User.objects.create_user(
            username=username, password=mdp)
        u.first_name = nom
        u.save()
        token = create_token(u.id)
        is_Page = Profile.objects.filter(user = u).exists()
        return {"status": 201,"token": token,'is_Page':is_Page, "message": "votre compte a été créé avec succès"}

# sdfSDFdsgsez


@router.post('login/', tags=['LOGIN ROUTER'], auth=None)
def login(request, data: LoginSchemas):
    username = data.username
    mdp = data.motPasse
    user = authenticate(request, username=username, password=mdp)
    u = User.objects.filter(username=username).exists()
    if u:
        user = User.objects.get(username=username)
        t = user.check_password(mdp)
        print(t)
        if t:
            token = create_token(user.id)
            is_Page = Profile.objects.filter(user = user).exists()
            return {"token": token,'is_Page':is_Page}
        else:
            raise HttpError(status_code=404,
                            message="Le mot de passe fourni est incorrect. Veuillez vérifier vos informations d'identification et réessayer.")
    else:
        raise HttpError(status_code=404,
                        message="Le numéro de téléphone fourni est incorrect. Veuillez vérifier et réessayer.")


@router.post("envoyer_code", tags=['SEND CODE ROUTER'], auth=None)
def envoyer_code(request, data: ResetPSchema):
    try:
        username = data.username
        user = User.objects.get(username=username)
        code = generate_code()  # Générer le code à envoyer par SMS
        # Enregistrer le code dans la base de données
        Code.objects.create(user=user, code=code)
        # Envoyer le code par SMS à l'utilisateur
        # send_sms(user.phone_number, code)
        return {"status": 200, "message": "Code envoyé avec succès"}
    except User.DoesNotExist:
        return {"status": 404, "message": "Utilisateur non trouvé"}


@router.post("changer_code", tags=['VERIFIE CODE ROUTER'], auth=None)
def verifier_code(request, code: int):
    try:
        code = Code.objects.get(code=code)
        u = code.user
        return {"status": 200, "message": "ok", "data": {'user': u}}
    except User.DoesNotExist:
        return {"status": 404, "message": "Utilisateur non trouvé"}


# CHANGER LE MOT DE PASSE
