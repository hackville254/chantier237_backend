from ninja import Schema
from pydantic import validator
from ninja.errors import HttpError


class ResetPSchema(Schema):
    username: str


class LoginSchemas(Schema):
    username: str
    motPasse: str


class RegisterSchemas(Schema):
    nom: str
    username: str
    motPasse: str
    CmotPasse: str
    
    @validator('motPasse')
    def validate_motPasse(cls, motPasse):
        if len(motPasse) < 5:
            raise HttpError(
                status_code=400, message="Le mot de passe doit contenir au moins 5 caractères.")
        if not any(char.isupper() for char in motPasse) or not any(char.islower() for char in motPasse):
            raise HttpError(
                status_code=400, message="Le mot de passe doit contenir des caractères en majuscules et en minuscules.")
        return motPasse

    @validator('CmotPasse')
    def validate_CmotPasse(cls, CmotPasse, values, **kwargs):
        if 'motPasse' in values and CmotPasse != values['motPasse']:
            raise HttpError(status_code=400,
                            message="Les mots de passe ne correspondent pas.")
        return CmotPasse
