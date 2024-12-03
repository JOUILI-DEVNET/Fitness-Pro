import customtkinter as ctk
from PIL import Image, ImageTk
import json
from datetime import datetime
import math
import os
import time
from tkinter import messagebox

class ModernFitnessApp:
    def __init__(self):
        # Configuration du thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Fenêtre principale
        self.window = ctk.CTk()
        self.window.title("FITNESS PRO ELITE 2024")
        self.window.geometry("1400x800")
        
        # Couleurs modernes
        self.colors = {
            'primary': '#00ff88',    # Vert néon
            'secondary': '#ff3366',   # Rose néon
            'accent': '#00ccff',      # Bleu néon
            'background': '#111111',  # Noir profond
            'card': '#1a1a1a',       # Gris foncé
            'text': '#ffffff'         # Blanc
        }
        
        # Variables
        self.current_view = None
        self.timer_running = False
        self.time_remaining = 60
        self.progress = 0
        self.timer_completions = 0
        
        # Création de l'interface
        self.create_gui()
        self.start_animation()
        
        # Afficher la vue par défaut
        self.show_view("workout")

    def create_gui(self):
        # Container principal
        self.main_frame = ctk.CTkFrame(self.window, fg_color=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Barre latérale
        self.create_sidebar()
        
        # Zone principale
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['card'])
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        # Création des vues
        self.create_workout_view()
        self.create_stats_view()
        self.create_settings_view()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.main_frame, fg_color=self.colors['card'])
        sidebar.pack(side="left", fill="y", padx=10)
        
        # Logo animé et signature dans un même conteneur
        logo_container = ctk.CTkFrame(sidebar, fg_color='transparent')
        logo_container.pack(pady=(30,0))  # Espacement en haut seulement
        
        # Logo animé
        self.logo_label = ctk.CTkLabel(
            logo_container,
            text="FITNESS PRO",
            font=("Roboto", 28, "bold"),
            text_color=self.colors['primary']
        )
        self.logo_label.pack()
        
        # Signature directement sous le logo
        signature = ctk.CTkLabel(
            logo_container,
            text="Made by Achraf",
            font=("Roboto", 12),
            text_color=self.colors['accent']
        )
        signature.pack(pady=(5,20))  # Espacement en haut et en bas
        
        # Profil utilisateur
        try:
            with open('data/settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)
                
            profile_frame = ctk.CTkFrame(sidebar, fg_color='transparent')
            profile_frame.pack(fill="x", pady=20)
            
            # Avatar (cercle coloré avec initiales)
            avatar_frame = ctk.CTkFrame(
                profile_frame,
                width=60,
                height=60,
                fg_color=self.colors['primary'],
                corner_radius=30
            )
            avatar_frame.pack(pady=10)
            avatar_frame.pack_propagate(False)
            
            initials = settings['user']['name'][0].upper() if settings['user']['name'] else "U"
            ctk.CTkLabel(
                avatar_frame,
                text=initials,
                font=("Roboto", 24, "bold"),
                text_color=self.colors['card']
            ).place(relx=0.5, rely=0.5, anchor="center")
            
            # Infos utilisateur
            ctk.CTkLabel(
                profile_frame,
                text=settings['user']['name'],
                font=("Roboto", 18, "bold"),
                text_color=self.colors['text']
            ).pack(pady=5)
            
            stats_text = f"{settings['user']['age']} ans • {settings['user']['weight']}kg"
            ctk.CTkLabel(
                profile_frame,
                text=stats_text,
                font=("Roboto", 14),
                text_color=self.colors['accent']
            ).pack()
            
        except Exception as e:
            print(f"Erreur lors du chargement du profil: {e}")
        
        # Séparateur
        separator = ctk.CTkFrame(sidebar, height=2, fg_color=self.colors['accent'])
        separator.pack(fill="x", padx=20, pady=20)
        
        # Boutons de navigation
        buttons = [
            ("Entraînement", "workout"),  # Supprimé l'icône
            ("Statistiques", "stats"),
            ("Paramètres", "settings")
        ]
        
        for text, view in buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=lambda v=view: self.show_view(v),
                font=("Roboto", 18),
                fg_color="transparent",
                text_color=self.colors['text'],
                hover_color=self.colors['primary'],
                width=200,
                height=50
            )
            btn.pack(pady=10)

    def create_workout_view(self):
        # Supprimer l'ancienne vue si elle existe
        if hasattr(self, 'workout_frame'):
            self.workout_frame.destroy()
        
        # Créer une nouvelle vue
        self.workout_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        
        # Titre
        title = ctk.CTkLabel(
            self.workout_frame,
            text="CHOISISSEZ VOTRE ENTRAÎNEMENT",
            font=("Roboto", 32, "bold"),
            text_color=self.colors['primary']
        )
        title.pack(pady=20)
        
        try:
            # Charger les programmes d'entraînement
            with open('data/workout_programs.json', 'r', encoding='utf-8') as f:
                self.workout_programs = json.load(f)
            
            # Conteneur défilable pour les programmes
            programs_container = ctk.CTkScrollableFrame(
                self.workout_frame,
                fg_color='transparent',
                height=600  # Hauteur fixe pour activer le défilement
            )
            programs_container.pack(fill="x", padx=20, pady=10)
            
            # Créer une carte pour chaque programme
            for program_id, program in self.workout_programs.items():
                self.create_program_card(programs_container, program_id, program)
        
        except Exception as e:
            print(f"Erreur lors du chargement des programmes : {e}")
            # Afficher un message d'erreur dans l'interface
            ctk.CTkLabel(
                self.workout_frame,
                text="Erreur lors du chargement des programmes",
                font=("Roboto", 18),
                text_color=self.colors['secondary']
            ).pack(pady=20)

    def create_program_card(self, container, program_id, program):
        card = ctk.CTkFrame(container, fg_color=self.colors['card'])
        card.pack(fill="x", padx=20, pady=5)
        
        # En-tête
        header = ctk.CTkFrame(card, fg_color='transparent')
        header.pack(fill="x", padx=15, pady=10)
        
        # Titre et description
        info_frame = ctk.CTkFrame(header, fg_color='transparent')
        info_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=program['name'],
            font=("Roboto", 20, "bold"),
            text_color=self.colors['text']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=program['description'],
            font=("Roboto", 14),
            text_color=self.colors['text']
        ).pack(anchor="w")
        
        # Boutons de durée
        duration_frame = ctk.CTkFrame(card, fg_color='transparent')
        duration_frame.pack(fill="x", padx=15, pady=10)
        
        for duration in program['durations']:
            ctk.CTkButton(
                duration_frame,
                text=f"⏱️ {duration['name']}",
                command=lambda p_id=program_id, d=duration: self.start_workout(p_id, d),
                font=("Roboto", 16),
                fg_color=self.colors['secondary'],
                hover_color=self.colors['accent'],
                width=120
            ).pack(side="left", padx=5)

    def create_stats_view(self):
        # Nettoyer la vue précédente
        if hasattr(self, 'stats_frame'):
            for widget in self.stats_frame.winfo_children():
                widget.destroy()
        
        self.stats_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        
        # Titre
        ctk.CTkLabel(
            self.stats_frame,
            text="STATISTIQUES",
            font=("Roboto", 32, "bold"),
            text_color=self.colors['primary']
        ).pack(pady=20)
        
        # Conteneur pour les stats
        stats_container = ctk.CTkFrame(self.stats_frame, fg_color=self.colors['card'])
        stats_container.pack(fill="x", padx=20, pady=10)
        
        try:
            # Charger les données de progression
            with open('data/progress.json', 'r') as f:
                progress_data = json.load(f)
            
            # Afficher les statistiques principales
            stats = [
                ("💪 Entraînements totaux", progress_data['stats']['total_workouts']),
                ("🍖 Calories brûlées", progress_data['stats']['total_calories']),
                ("🎯 Série actuelle", progress_data['stats']['streak']),
                ("⭐ Meilleure série", progress_data['stats']['best_streak']),
                ("⏱️ Séances minuteur complétées", self.timer_completions)
            ]
            
            for label, value in stats:
                stat_frame = ctk.CTkFrame(stats_container, fg_color='transparent')
                stat_frame.pack(fill="x", padx=15, pady=10)
                
                ctk.CTkLabel(
                    stat_frame,
                    text=label,
                    font=("Roboto", 18),
                    text_color=self.colors['text']
                ).pack(side="left")
                
                ctk.CTkLabel(
                    stat_frame,
                    text=str(value),
                    font=("Roboto", 18, "bold"),
                    text_color=self.colors['primary']
                ).pack(side="right")
            
        except Exception as e:
            # Afficher un message d'erreur si le fichier ne peut pas être lu
            ctk.CTkLabel(
                stats_container,
                text="Erreur lors du chargement des statistiques",
                font=("Roboto", 18),
                text_color=self.colors['secondary']
            ).pack(pady=20)

    def create_settings_view(self):
        self.settings_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        
        # Titre principal
        ctk.CTkLabel(
            self.settings_frame,
            text="PARAMÈTRES",
            font=("Roboto", 32, "bold"),
            text_color=self.colors['primary']
        ).pack(pady=20)

        # Création des onglets
        tabs = ctk.CTkTabview(self.settings_frame)
        tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Ajouter les onglets
        tabs.add("Général")
        tabs.add("Programmes")
        
        # Onglet Général
        self.create_general_settings(tabs.tab("Général"))
        
        # Onglet Programmes
        self.create_programs_settings(tabs.tab("Programmes"))

    def create_general_settings(self, parent):
        # Charger les paramètres actuels
        try:
            with open('data/settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Paramètres utilisateur
            user_frame = ctk.CTkFrame(parent, fg_color=self.colors['card'])
            user_frame.pack(fill="x", padx=20, pady=10)
            
            # En-tête avec avatar
            header_frame = ctk.CTkFrame(user_frame, fg_color='transparent')
            header_frame.pack(fill="x", pady=10)
            
            # Avatar
            avatar_frame = ctk.CTkFrame(
                header_frame,
                width=60,
                height=60,
                fg_color=self.colors['primary'],
                corner_radius=30
            )
            avatar_frame.pack(side="left", padx=20)
            avatar_frame.pack_propagate(False)
            
            initials = settings['user']['name'][0].upper() if settings['user']['name'] else "U"
            ctk.CTkLabel(
                avatar_frame,
                text=initials,
                font=("Roboto", 24, "bold"),
                text_color=self.colors['card']
            ).place(relx=0.5, rely=0.5, anchor="center")
            
            ctk.CTkLabel(
                header_frame,
                text="Paramètres utilisateur",
                font=("Roboto", 18, "bold"),
                text_color=self.colors['primary']
            ).pack(side="left", padx=10)
            
            # Variables pour stocker les valeurs
            self.user_vars = {}
            
            # Champs de paramètres utilisateur
            fields = [
                ("Nom", "name", settings['user']['name']),
                ("Âge", "age", settings['user']['age']),
                ("Poids (kg)", "weight", settings['user']['weight']),
                ("Taille (cm)", "height", settings['user']['height'])
            ]
            
            for label, key, value in fields:
                field_frame = ctk.CTkFrame(user_frame, fg_color='transparent')
                field_frame.pack(fill="x", padx=15, pady=5)
                
                ctk.CTkLabel(
                    field_frame,
                    text=label,
                    font=("Roboto", 14)
                ).pack(side="left")
                
                var = ctk.StringVar(value=str(value))
                self.user_vars[key] = var
                
                entry = ctk.CTkEntry(
                    field_frame,
                    textvariable=var,
                    width=200
                )
                entry.pack(side="right")
            
            # Bouton de sauvegarde
            ctk.CTkButton(
                user_frame,
                text="Enregistrer",
                command=self.save_user_settings,
                font=("Roboto", 14),
                fg_color=self.colors['primary'],
                hover_color=self.colors['accent']
            ).pack(pady=20)
                
        except Exception as e:
            ctk.CTkLabel(
                parent,
                text="Erreur lors du chargement des paramètres",
                font=("Roboto", 16),
                text_color=self.colors['secondary']
            ).pack(pady=20)

    def save_user_settings(self):
        try:
            with open('data/settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Mettre à jour les paramètres utilisateur
            for key, var in self.user_vars.items():
                value = var.get()
                # Convertir en nombre si nécessaire
                if key in ['age', 'weight', 'height']:
                    value = int(value)
                settings['user'][key] = value
            
            with open('data/settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            
            # Rafraîchir la barre latérale
            self.refresh_sidebar()
            
            # Afficher un message de confirmation
            messagebox.showinfo("Succès", "Paramètres enregistrés avec succès!")
            
        except Exception as e:
            self.show_error_dialog("Erreur lors de la sauvegarde des paramètres")

    def refresh_sidebar(self):
        # Supprimer l'ancienne barre latérale
        if hasattr(self, 'main_frame'):
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget != self.content_frame:
                    widget.destroy()
        
        # Recréer la barre latérale
        self.create_sidebar()

    def toggle_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.start_button.configure(text="REPRENDRE")
        else:
            self.timer_running = True
            self.start_button.configure(text="PAUSE")
            self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        
        if self.time_remaining > 0:
            mins, secs = divmod(self.time_remaining, 60)
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
            self.time_remaining -= 1
            self.window.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.start_button.configure(text="DÉMARRER")
            self.timer_completions += 1
            self.update_progress_file()
            self.show_completion_message()

    def update_progress_file(self, program):
        try:
            with open('data/progress.json', 'r') as f:
                progress_data = json.load(f)
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Mettre à jour les statistiques
            progress_data['stats']['total_workouts'] += 1
            progress_data['stats']['total_calories'] += self.current_duration['calories']
            
            # Mettre à jour la série
            last_date = progress_data['stats']['last_workout_date']
            if last_date:
                last_date = datetime.strptime(last_date, "%Y-%m-%d")
                if (datetime.now() - last_date).days == 1:
                    progress_data['stats']['streak'] += 1
                    progress_data['stats']['best_streak'] = max(
                        progress_data['stats']['streak'],
                        progress_data['stats']['best_streak']
                    )
                elif (datetime.now() - last_date).days > 1:
                    progress_data['stats']['streak'] = 1
            else:
                progress_data['stats']['streak'] = 1
            
            progress_data['stats']['last_workout_date'] = today
            
            # Ajouter à l'historique
            new_workout = {
                "date": today,
                "workout": program['name'],
                "duration": self.current_duration['name'],
                "completed": True,
                "calories": self.current_duration['calories'],
                "time": self.current_duration['time'],
                "exercises_completed": len(program['exercises'])
            }
            progress_data['history'].append(new_workout)
            
            # Mettre à jour le compteur de ce type d'entraînement
            program_type = program['name'].split()[0]
            if program_type in progress_data['workout_counts']:
                progress_data['workout_counts'][program_type] += 1
            
            with open('data/progress.json', 'w') as f:
                json.dump(progress_data, f, indent=4)
                
        except Exception as e:
            print(f"Erreur lors de la mise à jour des statistiques: {e}")

    def reset_timer(self):
        self.timer_running = False
        self.time_remaining = 60
        self.timer_label.configure(text="01:00")
        self.start_button.configure(text="DÉMARRER")

    def show_completion_message(self):
        popup = ctk.CTkToplevel()
        popup.title("Exercice terminé!")
        popup.geometry("300x200")
        
        # Centrer la fenêtre popup
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 150
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 100
        popup.geometry(f"+{x}+{y}")
        
        # Configurer la popup pour être toujours au premier plan
        popup.attributes('-topmost', True)
        
        # Ajouter un fond coloré
        popup.configure(fg_color=self.colors['card'])
        
        ctk.CTkLabel(
            popup,
            text="🎉 Excellent travail! 🎉",
            font=("Roboto", 20, "bold"),
            text_color=self.colors['primary']
        ).pack(pady=20)
        
        ctk.CTkButton(
            popup,
            text="OK",
            command=popup.destroy,
            fg_color=self.colors['secondary'],
            hover_color=self.colors['accent']
        ).pack(pady=10)

    def show_view(self, view_name):
        # Cacher toutes les vues
        for view in ['workout', 'stats', 'manage_programs', 'settings']:
            if hasattr(self, f'{view}_frame'):
                getattr(self, f'{view}_frame').pack_forget()
        
        # Afficher la vue demandée
        if view_name == 'workout':
            self.create_workout_view()  # Recréer la vue workout
        elif view_name == 'stats':
            self.create_stats_view()    # Recréer la vue stats
        elif view_name == 'manage_programs':
            self.create_manage_programs_view()
        
        if hasattr(self, f'{view_name}_frame'):
            getattr(self, f'{view_name}_frame').pack(fill="both", expand=True)

    def start_animation(self):
        def animate():
            self.progress = (self.progress + 2) % 360
            r = int(abs(math.sin(math.radians(self.progress))) * 255)
            g = int(abs(math.sin(math.radians(self.progress + 120))) * 255)
            b = int(abs(math.sin(math.radians(self.progress + 240))) * 255)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.logo_label.configure(text_color=color)
            self.window.after(50, animate)
        
        animate()

    def run(self):
        self.window.mainloop()

    def start_workout(self, program_id, duration):
        self.current_program = self.workout_programs[program_id]
        self.current_duration = duration
        self.time_remaining = duration['time']
        self.total_time = duration['time']
        
        # Nettoyer la vue précédente
        for widget in self.workout_frame.winfo_children():
            widget.destroy()
        
        # Recréer le frame principal avec une taille fixe
        self.workout_frame.configure(width=1200, height=700)
        self.workout_frame.pack_propagate(False)  # Empêcher le redimensionnement automatique
        
        # Afficher la vue d'exercice actif
        self.active_workout_frame = ctk.CTkFrame(self.workout_frame, fg_color=self.colors['card'])
        self.active_workout_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centrer le frame
        
        # Créer le canvas pour l'animation
        self.canvas = ctk.CTkCanvas(
            self.active_workout_frame,
            width=300,
            height=300,
            bg=self.colors['card'],
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Créer les cercles d'animation
        self.circles = []
        for i in range(3):  # Créer 3 cercles concentriques
            circle = self.canvas.create_oval(
                50, 50, 250, 250,
                outline=self.colors['primary'],
                width=2,
                dash=(1, 1)  # Créer un effet pointillé
            )
            self.circles.append(circle)
        
        # Timer au centre du cercle
        self.timer_label = ctk.CTkLabel(
            self.active_workout_frame,
            text=f"{duration['time']:02d}",
            font=("Roboto", 72, "bold"),
            text_color=self.colors['primary']
        )
        self.timer_label.pack(pady=10)
        
        # Nom de l'entraînement
        ctk.CTkLabel(
            self.active_workout_frame,
            text=self.current_program['name'],
            font=("Roboto", 24, "bold"),
            text_color=self.colors['primary']
        ).pack(pady=10)
        
        # Barre de progression
        self.progress_var = ctk.DoubleVar(value=0)
        self.progress_bar = ctk.CTkProgressBar(
            self.active_workout_frame,
            variable=self.progress_var,
            width=400,
            height=20,
            fg_color=self.colors['background'],
            progress_color=self.colors['primary']
        )
        self.progress_bar.pack(pady=20)
        
        # Animation initiale
        self.pulse_size = 1.0
        self.pulse_growing = True
        self.animate_circles()
        
        # Démarrer le timer
        self.timer_running = True
        self.animate_circles()  # Démarrer l'animation avant le timer
        self.update_workout_timer()
        
        # Forcer une mise à jour immédiate de l'interface
        self.window.update_idletasks()
        self.window.update()

    def animate_circles(self):
        if not self.timer_running:
            return
        
        center_x, center_y = 150, 150
        base_radius = 100
        
        # Animation pour chaque cercle
        for i, circle in enumerate(self.circles):
            # Calculer l'angle et le rayon pour chaque cercle
            phase = time.time() * (2 - i * 0.5)  # Vitesses différentes pour chaque cercle
            scale = 0.1 * math.sin(phase * 2) + 1.0  # chelle d'oscillation
            
            # Rayon spécifique pour chaque cercle
            radius = base_radius * (1 + i * 0.2) * scale
            
            # Ajouter un mouvement circulaire
            orbit_radius = 10  # Rayon de l'orbite
            orbit_speed = 2 * (i + 1)  # Vitesse de rotation différente pour chaque cercle
            orbit_x = math.cos(time.time() * orbit_speed) * orbit_radius
            orbit_y = math.sin(time.time() * orbit_speed) * orbit_radius
            
            # Mettre à jour la position du cercle avec le mouvement orbital
            self.canvas.coords(circle,
                center_x - radius + orbit_x,
                center_y - radius + orbit_y,
                center_x + radius + orbit_x,
                center_y + radius + orbit_y
            )
            
            # Couleur dynamique pour chaque cercle
            hue = (time.time() * 50 + i * 30) % 360
            color = self.hsv_to_rgb(hue, 1, 1)
            self.canvas.itemconfig(circle, outline=color)
            
            # Faire tourner le motif pointillé
            dash_offset = int(time.time() * 50) % 20
            self.canvas.itemconfig(circle, dash=(1, 1), dashoffset=dash_offset)
        
        # Effet de pulsation pour le texte du timer
        pulse = abs(math.sin(time.time() * 2)) * 0.2 + 0.8
        self.timer_label.configure(text_color=self.hsv_to_rgb(time.time() * 50 % 360, 0.7, 1))
        
        if self.timer_running:
            self.window.after(20, self.animate_circles)  # Animation plus fluide (50 FPS)

    def hsv_to_rgb(self, h, s, v):
        """Convertit HSV en code couleur RGB hexadécimal"""
        h = h / 360
        if s == 0.0:
            return '#%02x%02x%02x' % (v, v, v)
        
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
        
        return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

    def update_workout_timer(self):
        if not self.timer_running:
            return
        
        if self.time_remaining > 0:
            # Afficher les secondes
            self.timer_label.configure(text=f"{self.time_remaining:02d}")
            
            # Mise à jour de la barre de progression
            elapsed_time = self.total_time - self.time_remaining
            progress = elapsed_time / self.total_time
            self.progress_var.set(progress)
            
            # Effet de "battement" plus prononcé à chaque seconde
            def pulse_effect():
                self.pulse_size = 1.2  # Expansion rapide
                self.window.after(100, lambda: setattr(self, 'pulse_size', 1.0))  # Retour à la normale
            
            pulse_effect()
            self.time_remaining -= 1
            self.window.after(1000, self.update_workout_timer)
        else:
            self.complete_workout()

    def complete_workout(self):
        self.timer_running = False
        self.update_progress_file(self.current_program)
        self.show_completion_message()
        
        # Attendre un court instant avant de réinitialiser la vue
        self.window.after(1000, self.reset_workout_view)

    def reset_workout_view(self):
        # Arrêter l'animation
        self.timer_running = False
        
        # Nettoyer complètement la vue
        for widget in self.workout_frame.winfo_children():
            widget.destroy()
        
        # Réinitialiser la configuration du frame
        self.workout_frame.pack_propagate(True)
        self.workout_frame.configure(width=None, height=None)  # Réinitialiser les dimensions fixes
        
        # Retourner à la vue principale des entraînements
        self.show_view('workout')

    def create_manage_programs_view(self):
        self.manage_programs_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        
        # Titre
        ctk.CTkLabel(
            self.manage_programs_frame,
            text="GESTION DES PROGRAMMES",
            font=("Roboto", 32, "bold"),
            text_color=self.colors['primary']
        ).pack(pady=20)
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(self.manage_programs_frame, fg_color='transparent')
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            actions_frame,
            text="➕ Nouveau Programme",
            command=self.create_new_program,
            font=("Roboto", 16),
            fg_color=self.colors['secondary'],
            hover_color=self.colors['accent']
        ).pack(side="left", padx=5)
        
        # Liste des programmes existants
        programs_frame = ctk.CTkFrame(self.manage_programs_frame, fg_color=self.colors['card'])
        programs_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger et afficher les programmes existants
        try:
            with open('data/workout_programs.json', 'r', encoding='utf-8') as f:
                programs = json.load(f)
                
            for program_id, program in programs.items():
                program_frame = ctk.CTkFrame(programs_frame, fg_color='transparent')
                program_frame.pack(fill="x", padx=15, pady=5)
                
                ctk.CTkLabel(
                    program_frame,
                    text=program['name'],
                    font=("Roboto", 16),
                    text_color=self.colors['text']
                ).pack(side="left", padx=10)
                
                ctk.CTkButton(
                    program_frame,
                    text="✏️ Modifier",
                    command=lambda p=program_id: self.edit_program(p),
                    font=("Roboto", 14),
                    fg_color=self.colors['primary'],
                    hover_color=self.colors['accent'],
                    width=100
                ).pack(side="right", padx=5)
                
                ctk.CTkButton(
                    program_frame,
                    text="🗑️ Supprimer",
                    command=lambda p=program_id: self.delete_program(p),
                    font=("Roboto", 14),
                    fg_color=self.colors['secondary'],
                    hover_color=self.colors['accent'],
                    width=100
                ).pack(side="right", padx=5)
                
        except Exception as e:
            ctk.CTkLabel(
                programs_frame,
                text="Erreur lors du chargement des programmes",
                font=("Roboto", 16),
                text_color=self.colors['secondary']
            ).pack(pady=20)

    def create_new_program(self):
        self.show_program_form()

    def edit_program(self, program_id):
        self.show_program_form(program_id)

    def delete_program(self, program_id):
        try:
            if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce programme ?"):
                with open('data/workout_programs.json', 'r', encoding='utf-8') as f:
                    programs = json.load(f)
                
                # Supprimer le programme
                if program_id in programs:
                    del programs[program_id]
                    
                    # Sauvegarder les modifications
                    with open('data/workout_programs.json', 'w', encoding='utf-8') as f:
                        json.dump(programs, f, indent=4)
                    
                    # Rafraîchir l'interface
                    if hasattr(self, 'settings_frame'):
                        tabs = [child for child in self.settings_frame.winfo_children() 
                               if isinstance(child, ctk.CTkTabview)]
                        if tabs:
                            programs_tab = tabs[0].tab("Programmes")
                            # Nettoyer l'onglet
                            for widget in programs_tab.winfo_children():
                                widget.destroy()
                            # Recréer la liste des programmes
                            self.create_programs_settings(programs_tab)
                    
                    messagebox.showinfo("Succès", "Programme supprimé avec succès!")
                else:
                    messagebox.showerror("Erreur", "Programme introuvable")
        
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")
            messagebox.showerror("Erreur", "Erreur lors de la suppression du programme")

    def show_program_form(self, program_id=None):
        form_window = ctk.CTkToplevel(self.window)
        form_window.title("Nouveau Programme" if program_id is None else "Modifier Programme")
        form_window.geometry("500x600")
        
        # Forcer la fenêtre à être au premier plan
        form_window.lift()  # Mettre la fenêtre au premier plan
        form_window.focus_force()  # Forcer le focus
        form_window.grab_set()  # Empêcher l'interaction avec la fenêtre principale
        form_window.attributes('-topmost', True)  # Garder la fenêtre au-dessus
        
        # Centrer la fenêtre
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 250
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 300
        form_window.geometry(f"+{x}+{y}")
        
        # Variables pour stocker les valeurs
        program_name = ctk.StringVar()
        program_desc = ctk.StringVar()
        
        # Charger les données si on modifie un programme existant
        if program_id:
            with open('data/workout_programs.json', 'r', encoding='utf-8') as f:
                programs = json.load(f)
                program = programs[program_id]
                program_name.set(program['name'])
                program_desc.set(program['description'])
        
        # Formulaire
        form_frame = ctk.CTkFrame(form_window, fg_color=self.colors['card'])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Champs du formulaire
        ctk.CTkLabel(
            form_frame,
            text="Nom du programme",
            font=("Roboto", 16)
        ).pack(pady=(20,5))
        
        ctk.CTkEntry(
            form_frame,
            textvariable=program_name,
            width=300
        ).pack(pady=(0,20))
        
        ctk.CTkLabel(
            form_frame,
            text="Description",
            font=("Roboto", 16)
        ).pack(pady=5)
        
        ctk.CTkEntry(
            form_frame,
            textvariable=program_desc,
            width=300
        ).pack(pady=(0,20))
        
        # Boutons de durée
        durations_frame = ctk.CTkFrame(form_frame, fg_color='transparent')
        durations_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            durations_frame,
            text="Durées disponibles",
            font=("Roboto", 16)
        ).pack()
        
        durations = [
            {"time": 15, "name": "15 sec", "calories": 20},
            {"time": 30, "name": "30 sec", "calories": 40},
            {"time": 60, "name": "60 sec", "calories": 80}
        ]
        
        for duration in durations:
            duration_frame = ctk.CTkFrame(durations_frame, fg_color='transparent')
            duration_frame.pack(fill="x", pady=5)
            
            ctk.CTkCheckBox(
                duration_frame,
                text=f"{duration['name']} ({duration['calories']} calories)",
                font=("Roboto", 14)
            ).pack(side="left", padx=20)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(form_frame, fg_color='transparent')
        buttons_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            buttons_frame,
            text="Annuler",
            command=form_window.destroy,
            fg_color=self.colors['secondary'],
            hover_color=self.colors['accent'],
            width=100
        ).pack(side="left", padx=20)
        
        ctk.CTkButton(
            buttons_frame,
            text="Enregistrer",
            command=lambda: self.save_program(program_id, program_name.get(), program_desc.get(), form_window),
            fg_color=self.colors['primary'],
            hover_color=self.colors['accent'],
            width=100
        ).pack(side="right", padx=20)

    def save_program(self, program_id, name, description, form_window):
        try:
            with open('data/workout_programs.json', 'r', encoding='utf-8') as f:
                programs = json.load(f)
            
            new_program = {
                "name": name,
                "description": description,
                "durations": [
                    {"time": 15, "name": "15 sec", "calories": 20},
                    {"time": 30, "name": "30 sec", "calories": 40},
                    {"time": 60, "name": "60 sec", "calories": 80}
                ],
                "exercises": []
            }
            
            if program_id is None:
                # Nouveau programme
                program_id = f"program_{len(programs) + 1}"
            
            programs[program_id] = new_program
            
            with open('data/workout_programs.json', 'w', encoding='utf-8') as f:
                json.dump(programs, f, indent=4)
            
            form_window.destroy()
            
            # Rafraîchir l'onglet Programmes
            if hasattr(self, 'settings_frame'):
                tabs = [child for child in self.settings_frame.winfo_children() 
                       if isinstance(child, ctk.CTkTabview)][0]
                programs_tab = tabs.tab("Programmes")
                for widget in programs_tab.winfo_children():
                    widget.destroy()
                self.create_programs_settings(programs_tab)
                
        except Exception as e:
            self.show_error_dialog("Erreur lors de la sauvegarde du programme")

    def create_programs_settings(self, parent):
        # Bouton d'ajout
        ctk.CTkButton(
            parent,
            text="➕ Nouveau Programme",
            command=self.create_new_program,
            font=("Roboto", 16),
            fg_color=self.colors['secondary'],
            hover_color=self.colors['accent']
        ).pack(pady=10)
        
        # Liste des programmes
        programs_frame = ctk.CTkScrollableFrame(parent, fg_color=self.colors['card'])
        programs_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        try:
            with open('data/workout_programs.json', 'r', encoding='utf-8') as f:
                programs = json.load(f)
                
            for program_id, program in programs.items():
                program_frame = ctk.CTkFrame(programs_frame, fg_color='transparent')
                program_frame.pack(fill="x", padx=15, pady=5)
                
                # Conteneur pour le nom et la description
                info_frame = ctk.CTkFrame(program_frame, fg_color='transparent')
                info_frame.pack(side="left", fill="x", expand=True, padx=10)
                
                ctk.CTkLabel(
                    info_frame,
                    text=program['name'],
                    font=("Roboto", 16, "bold"),
                    text_color=self.colors['text']
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=program['description'],
                    font=("Roboto", 12),
                    text_color=self.colors['accent']
                ).pack(anchor="w")
                
                # Boutons d'action
                buttons_frame = ctk.CTkFrame(program_frame, fg_color='transparent')
                buttons_frame.pack(side="right")
                
                ctk.CTkButton(
                    buttons_frame,
                    text="✏️",
                    command=lambda p=program_id: self.edit_program(p),
                    font=("Roboto", 14),
                    fg_color=self.colors['primary'],
                    hover_color=self.colors['accent'],
                    width=40
                ).pack(side="left", padx=2)
                
                ctk.CTkButton(
                    buttons_frame,
                    text="🗑️",
                    command=lambda p=program_id: self.delete_program(p),
                    font=("Roboto", 14),
                    fg_color=self.colors['secondary'],
                    hover_color=self.colors['accent'],
                    width=40
                ).pack(side="left", padx=2)
                
        except Exception as e:
            ctk.CTkLabel(
                programs_frame,
                text="Erreur lors du chargement des programmes",
                font=("Roboto", 16),
                text_color=self.colors['secondary']
            ).pack(pady=20)

if __name__ == "__main__":
    app = ModernFitnessApp()
    app.run()