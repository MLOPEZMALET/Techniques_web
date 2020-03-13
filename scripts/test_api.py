import unittest
from flask_testing import TestCase
from flask import session, request
import warnings
import os
import json
from passlib.apps import custom_app_context as pwd_context
from api import app, db, User

    
class BaseTestCase(TestCase):
    """ Base du test case"""
    some_user = {
        "username": "test",
        "password": "password"
    }
    admin_user = {
        "username": "admin",
        "password": "admin"
    }
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTD_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app
    
    def setUp(self):
        """ Création d'une base de données avant le test"""
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        
        db.create_all()
        user = User(username="admin")
        user.hash_password("admin")
        db.session.add(user)
        db.session.commit()
        
    def tearDown(self):
        """ Suppression de la base de données après le test"""
        db.session.remove()
        db.drop_all()

class TestAPI(BaseTestCase):
    def test_index(self):
        """ Test de la page d'index """
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"hello. Je marche et c'est une bonne nouvelle!" in response.data)
        
    def test_new_user(self):
        """ Test pour un nouvel utilisateur """
        self.assertIsNone(User.query.filter_by(
                username=self.some_user["username"]
        ).first())

        res = self.client.post(
                "/api/users",
                data=json.dumps(self.some_user),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(User.query.filter_by(username=self.some_user["username"]).first().username, self.some_user["username"])

        res2 = self.client.post(
                "/api/users",
                data=json.dumps(self.some_user),
                content_type="application/json"
        )
        # vérifie que le code d'erreur est bien renvoyé dans le cas ou l'utilisateur existe déjà
        self.assertEqual(res2.status_code, 409)
    
    def test_login_post(self):
        """ Vérifie que le login fonctionne correctement """
        res = self.client.post(
                "/login",
                data=json.dumps(self.admin_user),
                content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"Successful authentication")
    
    def test_incorrect_login_post(self):
        """ Vérifie que le login fonctionne comme prévu dans le cas d'une authentification incorrecte """
        res = self.client.post(
                "/login",
                data=json.dumps(self.some_user),
                content_type="application/json"
        )
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data, b"authentication error")
    
    def test_check_password(self):
        """ Teste si le mot de passe est correct après l'avoir décrypté """
        user = User.query.filter_by(username="admin").first()
        self.assertTrue(pwd_context.verify("admin", user.password_hash))
        self.assertFalse(pwd_context.verify("foobar", user.password_hash))
    
    def test_get_user(self):
        """ Teste si la fonction get_user renvoie bien le nom d'utilisateur """
        res = self.client.get(
                "/api/users/1",
                content_type='application/json'
        )
        self.assertEqual(res.json['username'], "admin")
    
    def test_json_post_put_and_delete(self):
        """ Teste si on peut ajouter une contribution """
        data = {
                "user_name": "admin",
                "contrib_type": "sound",
                "contrib_data": "testest",
                "contrib_path": "www.ntealan",
                "contrib_name": "test",
                "ntealan": "true",
                "validate": "false",
                "last_update": "today"
        }
        res = self.client.post(
                "/api/resource/add_contrib",
                data=json.dumps(data),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json["contrib_name"], "test")
        
        public_id = res.json["public_id"]
        
        """ Teste si on peut modifier la valeur d'un champ d'une contribution donnée """
        data = {"field": "user_name", "data_number": public_id, "new_data": "Gate"}
        res = self.client.put(
                "/api/resource/update_contrib",
                data=json.dumps(data),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json["new_data"], "Gate")
        self.assertTrue(b"Data successfully updated!" in res.data)
        
        """ Teste si on peut supprimer une contribution """
        # suppression de la contribution avec le public id récupéré
        data = {"public_id": public_id}
        res = self.client.delete(
                "/api/resource/delete_contrib",
                data=json.dumps(data),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(b"Data successfully deleted!" in res.data)
        
    def test_json_read(self):
        """ Vérifie qu'on peut consulter les données """
        res = self.client.get(
                "/api/resource/get",
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(b"Mikolov" in res.data)
        self.assertTrue(b"Gate" in res.data)
        self.assertTrue(b"Fokwe" in res.data)
        self.assertTrue(b"Taken" in res.data)
        self.assertTrue(b"Bergier" in res.data)
        
    def test_json_read_num(self):
        """ Teste si on peut accéder à une contribution par son numéro """
        res = self.client.get(
                "/api/resource/get/0",
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(b"94ec363b-0537-4929-820e-b0559c57ab4d" in res.data)
        self.assertTrue(b'Bergier' in res.data)
        self.assertFalse(b'Mikolov' in res.data)
    
    def test_json_read_field(self):
        """ Teste si on peut accéder à un champ dans toutes les contributions """
        res = self.client.get(
                "/api/resource/get/user_name",
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(b"Mikolov" in res.data)
        self.assertTrue(b"Gate" in res.data)
        self.assertTrue(b"Fokwe" in res.data)
        self.assertTrue(b"Taken" in res.data)
        self.assertTrue(b"Bergier" in res.data)
        
        self.assertFalse(b"sound" in res.data)
    
    def test_json_read_num_field(self):
        """ Test si on peut accéder à un champ dans une contribution """
        res = self.client.get(
                "/api/resource/get/0/user_name",
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(b"Bergier" in res.data)
        self.assertFalse(b"Mikolov" in res.data)
    
if __name__ == '__main__':
    unittest.main()

