from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

@freezer.register_generator
def home():
    # URLs as strings
    yield '/home'

# @freezer.register_generator
# def registrarse():
#     # URLs as strings
#     yield '/registrarse/'

# @freezer.register_generator
# def foto():
#     # URLs as strings
#     yield '/foto/'

# @freezer.register_generator
# def cambio():
#     # URLs as strings
#     yield '/cambio/'

# @freezer.register_generator
# def validar():
#     # URLs as strings
#     yield '/validar/'

# @freezer.register_generator
# def publicar():
#     # URLs as strings
#     yield '/publicar/'

# @freezer.register_generator
# def publicacion():
#     # URLs as strings
#     yield '/publicacion/'

# @freezer.register_generator
# def publicacion2():
#     # URLs as strings
#     yield '/publicacion2/'

# @freezer.register_generator
# def imagenes():
#     # URLs as strings
#     yield '/imagenes/'

# @freezer.register_generator
# def casiila():
#     # URLs as strings
#     yield '/', {'ID': '1'}

# @freezer.register_generator
# def salir():
#     # URLs as strings
#     yield '/salir/'

if __name__ == '__main__':
	freezer.freeze()
