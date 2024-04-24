import random

def generate_code():
    code = ""
    for _ in range(6):
        code += random.choice("0123456789")  # Générer un chiffre aléatoire de 0 à 9
    return code
