import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os
import tkinter as tk
from fitness_app import ModernFitnessApp
import customtkinter as ctk

class TestModernFitnessApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour toute la classe de test"""
        cls.root = tk.Tk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        cls.root.destroy()

    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.app = ModernFitnessApp()
        # Initialiser les composants nécessaires pour les tests
        if hasattr(self.app, 'create_workout_view'):
            self.app.create_workout_view()

    def tearDown(self):
        """Nettoyage après chaque test"""
        if hasattr(self, 'app'):
            self.app.window.destroy()

    def test_init(self):
        """Test de l'initialisation de l'application"""
        self.assertIsInstance(self.app.window, ctk.CTk)
        self.assertEqual(self.app.window.title(), "FITNESS PRO")
        self.assertEqual(self.app.time_remaining, 60)
        self.assertEqual(self.app.timer_completions, 0)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, 
           read_data='{"user": {"name": "TEST", "age": 25, "weight": 70, "height": 180}}')
    def test_load_user_settings(self, mock_open):
        """Test du chargement des paramètres utilisateur"""
        self.app.create_sidebar()
        mock_open.assert_called_with('data/settings.json', 'r', encoding='utf-8')

    def test_show_view(self):
        """Test du changement de vue"""
        self.app.show_view('stats')
        self.assertTrue(hasattr(self.app, 'stats_frame'))
        
        self.app.show_view('workout')
        self.assertTrue(hasattr(self.app, 'workout_frame'))

    @patch('json.dump')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_user_settings(self, mock_open, mock_json_dump):
        """Test de la sauvegarde des paramètres utilisateur"""
        # Configurer le mock pour retourner un JSON valide
        mock_open.return_value.read.return_value = json.dumps({
            "user": {
                "name": "TEST",
                "age": 25,
                "weight": 70,
                "height": 180
            }
        })
        
        self.app.user_vars = {
            'name': Mock(get=lambda: 'TEST'),
            'age': Mock(get=lambda: '30'),
            'weight': Mock(get=lambda: '75'),
            'height': Mock(get=lambda: '185')
        }
        
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.save_user_settings()
            mock_showinfo.assert_called_once()

    def test_timer_functions(self):
        """Test des fonctions du minuteur"""
        # Créer les composants nécessaires
        self.app.start_button = ctk.CTkButton(self.app.window)
        self.app.timer_label = ctk.CTkLabel(self.app.window, text="01:00")
        
        # Test du démarrage du timer
        self.app.toggle_timer()
        self.assertTrue(self.app.timer_running)
        
        # Test de la pause du timer
        self.app.toggle_timer()
        self.assertFalse(self.app.timer_running)
        
        # Test de la réinitialisation du timer
        self.app.reset_timer()
        self.assertEqual(self.app.time_remaining, 60)
        self.assertFalse(self.app.timer_running)

    @patch('json.load')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_update_progress_file(self, mock_open, mock_json_load):
        """Test de la mise à jour du fichier de progression"""
        mock_json_load.return_value = {
            'stats': {
                'total_workouts': 0,
                'total_calories': 0,
                'streak': 0,
                'best_streak': 0,
                'last_workout_date': None
            },
            'history': [],
            'workout_counts': {'HIIT': 0}
        }
        
        test_program = {
            'name': 'HIIT Test',
            'exercises': []
        }
        
        self.app.current_duration = {
            'name': '30 sec',
            'calories': 40,
            'time': 30
        }
        
        self.app.update_progress_file(test_program)
        mock_open.assert_called()

    def test_hsv_to_rgb(self):
        """Test de la conversion HSV vers RGB"""
        # Test avec des valeurs connues
        rgb = self.app.hsv_to_rgb(0, 1, 1)  # Rouge pur
        self.assertEqual(rgb, '#ff0000')
        
        rgb = self.app.hsv_to_rgb(120, 1, 1)  # Vert pur
        self.assertEqual(rgb, '#00ff00')
        
        rgb = self.app.hsv_to_rgb(240, 1, 1)  # Bleu pur
        self.assertEqual(rgb, '#0000ff')

class TestWorkoutPrograms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour toute la classe de test"""
        cls.root = tk.Tk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        cls.root.destroy()

    def setUp(self):
        self.app = ModernFitnessApp()
        
    def tearDown(self):
        self.app.window.destroy()

    @patch('json.load')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_create_new_program(self, mock_open, mock_json_load):
        """Test de la création d'un nouveau programme"""
        mock_json_load.return_value = {}
        
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.save_program(None, "Test Program", "Test Description", Mock())
            mock_open.assert_called()

    @patch('json.load')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_delete_program(self, mock_open, mock_json_load):
        """Test de la suppression d'un programme"""
        mock_json_load.return_value = {
            'program_1': {'name': 'Test Program'}
        }
        
        with patch('tkinter.messagebox.askyesno', return_value=True):
            with patch('tkinter.messagebox.showinfo') as mock_showinfo:
                self.app.delete_program('program_1')
                mock_showinfo.assert_called_once()

if __name__ == '__main__':
    unittest.main() 