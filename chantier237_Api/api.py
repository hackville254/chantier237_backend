from ninja import NinjaAPI
from core.token import verify_token
from core.views import router as coreRouter
from social.views import router as socialRouter
from ninja.security import HttpBearer

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        t = verify_token(token=token)
        return t



description = """
*Le but de Chantier237 est de mettre en relation des chercheurs de chantier avec les chefs de chantier. Cette plateforme vise à faciliter la recherche et la collaboration entre les personnes à la recherche de chantiers et les professionnels qui dirigent ces chantiers. Elle permet aux chercheurs de trouver des opportunités de chantier et de se connecter avec les chefs de chantier qui ont besoin de main-d'œuvre qualifiée. Les chefs de chantier peuvent également utiliser Chantier237 pour trouver des travailleurs compétents et expérimentés pour leurs projets.*

*Chantier237 agit comme un intermédiaire en fournissant une plateforme où les chercheurs de chantier peuvent présenter leurs compétences, leur expérience et leur disponibilité, tandis que les chefs de chantier peuvent publier des offres d'emploi et rechercher des profils correspondants. Cela facilite la mise en relation et la communication entre les deux parties, ce qui peut conduire à des opportunités de travail mutuellement bénéfiques*.
"""
app = NinjaAPI(
    title='Chantier237',
    version="1.0.0",
    description=description,
    auth=GlobalAuth(),
)

app.add_router("/authenticate/", coreRouter,tags=["AUTHENTIFICATION"])
app.add_router("/social/", socialRouter,tags=["PROFILE"])
