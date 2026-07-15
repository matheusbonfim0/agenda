from django.test import TestCase

# Create your tests here.
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Evento


class EventoAuthorizationTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('owner', password='safe-password')
        self.other = User.objects.create_user('other', password='safe-password')
        self.evento = Evento.objects.create(
            titulo='Privado',
            data_evento=datetime.now() + timedelta(days=1),
            descricao='Somente do proprietário',
            usuario=self.owner,
        )
        self.client.force_login(self.other)

    def test_cannot_view_another_users_event(self):
        response = self.client.get(f'/agenda/evento/?id={self.evento.id}')
        self.assertEqual(response.status_code, 404)

    def test_cannot_update_another_users_event(self):
        response = self.client.post('/agenda/evento/submit', {
            'id_evento': self.evento.id,
            'titulo': 'Alterado',
            'data_evento': '2030-01-01T10:00',
            'descricao': 'Alterado',
        })
        self.assertEqual(response.status_code, 404)
        self.evento.refresh_from_db()
        self.assertEqual(self.evento.titulo, 'Privado')

    def test_delete_requires_post_and_owner(self):
        url = f'/agenda/evento/delete/{self.evento.id}'
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url).status_code, 404)
        self.assertTrue(Evento.objects.filter(id=self.evento.id).exists())
