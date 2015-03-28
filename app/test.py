from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from app.models import *
from django.core.urlresolvers import reverse
# Create your tests here.

class TestAdministracion(TestCase):

    def add_user(self, username='test', first_name= 'test', last_name='test', email='test@test.com',password= 'test'):
        return User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)


    def test_add_user(self):
        u = self.add_user(username='test')
        self.assertTrue(isinstance(u,User))
        self.assertEqual(u.__unicode__(), u.first_name)
        print('Test de crear usuario, exitoso')

   
    def crear_rol(self, nombre='administrador', descripcion ='Se encarga de la administracion general', categoria=1):
        return  Rol.objects.create(nombre=nombre, descripcion=descripcion, categoria= categoria)

    def test_crear_rol(self):
        rol= self.crear_rol(nombre ='administrador')
        self.assertTrue(isinstance(rol,Rol))
        self.assertEqual(rol.__unicode__(), rol.nombre)
        print('Test de crear rol, exitoso')    
