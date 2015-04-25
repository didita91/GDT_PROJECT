from django.test import TestCase
from django.contrib.auth.models import User
from app.models import *
import datetime
# tere

class TestAdminProyecto(TestCase):

    def add_proyecto(self, nombre='test',descripcion='test'):
        scrum = RolUsuario(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        P = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,descripcion=descripcion,fecha_inicio=fecha)
        return P

    def test_add_proyecto(self):
        u = self.add_proyecto(nombre='test')
        self.assertTrue(isinstance(u,Proyecto))
        self.assertEqual(u.__unicode__(), u.nombre)
        print('Test de crear Proyecto, exitoso')



