#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration avancée de la détection de pose holistique
Par Dady Akrou Cyrille - Data Scientist

Ce script montre des fonctionnalités avancées :
- Sauvegarde des coordonnées des landmarks
- Calcul de distances entre points
- Détection de gestes simples
- Enregistrement vidéo avec détection
"""

import cv2
import mediapipe as mp
import numpy as np
import csv
import os
from datetime import datetime
import math

# Initialisation de MediaPipe
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

class DetectionAvancee:
    def __init__(self):
        self.landmarks_data = []
        self.recording = False
        self.video_writer = None
        
    def calculer_distance(self, point1, point2):
        """Calcule la distance euclidienne entre deux points"""
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def detecter_geste_main_fermee(self, hand_landmarks):
        """Détecte si la main est fermée (poing)"""
        if not hand_landmarks:
            return False
        
        # Points des doigts (tips) et des articulations (pip)
        finger_tips = [4, 8, 12, 16, 20]  # Pouce, Index, Majeur, Annulaire, Auriculaire
        finger_pips = [3, 6, 10, 14, 18]
        
        fingers_down = 0
        
        # Vérifier chaque doigt (sauf le pouce qui a une logique différente)
        for i in range(1, 5):
            if hand_landmarks.landmark[finger_tips[i]].y > hand_landmarks.landmark[finger_pips[i]].y:
                fingers_down += 1
        
        # Pour le pouce (logique différente car il bouge horizontalement)
        if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_pips[0]].x:
            fingers_down += 1
        
        return fingers_down >= 4  # Main fermée si au moins 4 doigts sont pliés
    
    def detecter_geste_paix(self, hand_landmarks):
        """Détecte le geste de paix (V avec index et majeur)"""
        if not hand_landmarks:
            return False
        
        # Index et majeur étendus, autres doigts pliés
        index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
        middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
        ring_down = hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y
        pinky_down = hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y
        
        return index_up and middle_up and ring_down and pinky_down
    
    def sauvegarder_landmarks(self, results, frame_number):
        """Sauvegarde les coordonnées des landmarks dans une liste"""
        frame_data = {
            'frame': frame_number,
            'timestamp': datetime.now().isoformat(),
            'face_landmarks': [],
            'pose_landmarks': [],
            'left_hand_landmarks': [],
            'right_hand_landmarks': []
        }
        
        # Landmarks du visage
        if results.face_landmarks:
            for landmark in results.face_landmarks.landmark:
                frame_data['face_landmarks'].append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })
        
        # Landmarks de la pose
        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                frame_data['pose_landmarks'].append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })
        
        # Landmarks des mains
        if results.left_hand_landmarks:
            for landmark in results.left_hand_landmarks.landmark:
                frame_data['left_hand_landmarks'].append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })
        
        if results.right_hand_landmarks:
            for landmark in results.right_hand_landmarks.landmark:
                frame_data['right_hand_landmarks'].append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })
        
        self.landmarks_data.append(frame_data)
    
    def exporter_donnees_csv(self, filename="landmarks_data.csv"):
        """Exporte les données des landmarks en CSV"""
        if not self.landmarks_data:
            print("Aucune donnée à exporter")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['frame', 'timestamp', 'type', 'landmark_id', 'x', 'y', 'z']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for frame_data in self.landmarks_data:
                frame_num = frame_data['frame']
                timestamp = frame_data['timestamp']
                
                # Écrire les landmarks du visage
                for i, landmark in enumerate(frame_data['face_landmarks']):
                    writer.writerow({
                        'frame': frame_num,
                        'timestamp': timestamp,
                        'type': 'face',
                        'landmark_id': i,
                        'x': landmark['x'],
                        'y': landmark['y'],
                        'z': landmark['z']
                    })
                
                # Écrire les landmarks de la pose
                for i, landmark in enumerate(frame_data['pose_landmarks']):
                    writer.writerow({
                        'frame': frame_num,
                        'timestamp': timestamp,
                        'type': 'pose',
                        'landmark_id': i,
                        'x': landmark['x'],
                        'y': landmark['y'],
                        'z': landmark['z']
                    })
                
                # Écrire les landmarks des mains
                for i, landmark in enumerate(frame_data['left_hand_landmarks']):
                    writer.writerow({
                        'frame': frame_num,
                        'timestamp': timestamp,
                        'type': 'left_hand',
                        'landmark_id': i,
                        'x': landmark['x'],
                        'y': landmark['y'],
                        'z': landmark['z']
                    })
                
                for i, landmark in enumerate(frame_data['right_hand_landmarks']):
                    writer.writerow({
                        'frame': frame_num,
                        'timestamp': timestamp,
                        'type': 'right_hand',
                        'landmark_id': i,
                        'x': landmark['x'],
                        'y': landmark['y'],
                        'z': landmark['z']
                    })
        
        print(f"Données exportées vers {filename}")
    
    def demarrer_enregistrement(self, width, height, fps=20):
        """Démarre l'enregistrement vidéo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"detection_pose_{timestamp}.mp4"
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
        self.recording = True
        print(f"Enregistrement démarré: {filename}")
    
    def arreter_enregistrement(self):
        """Arrête l'enregistrement vidéo"""
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        self.recording = False
        print("Enregistrement arrêté")
    
    def detection_avancee(self):
        """Fonction principale de détection avancée"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Erreur: Impossible d'ouvrir la webcam")
            return
        
        # Obtenir les dimensions de la vidéo
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        frame_count = 0
        
        with mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as holistic:
            
            print("Détection avancée démarrée!")
            print("Commandes:")
            print("- 'q': Quitter")
            print("- 'r': Démarrer/Arrêter l'enregistrement")
            print("- 's': Sauvegarder les données")
            print("- 'c': Effacer les données")
            
            while cap.isOpened():
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                frame_count += 1
                
                # Traitement MediaPipe
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = holistic.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Sauvegarder les landmarks
                self.sauvegarder_landmarks(results, frame_count)
                
                # Dessiner les landmarks
                if results.face_landmarks:
                    mp_drawing.draw_landmarks(
                        image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1),
                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1)
                    )
                
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),
                        mp_drawing.DrawingSpec(color=(0, 240, 240), thickness=2)
                    )
                
                # Détection de gestes pour les mains
                geste_texte = []
                
                if results.left_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                        mp_drawing.DrawingSpec(color=(0, 240, 0), thickness=2)
                    )
                    
                    if self.detecter_geste_main_fermee(results.left_hand_landmarks):
                        geste_texte.append("Main gauche: Poing")
                    elif self.detecter_geste_paix(results.left_hand_landmarks):
                        geste_texte.append("Main gauche: Paix")
                
                if results.right_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=4),
                        mp_drawing.DrawingSpec(color=(240, 0, 0), thickness=2)
                    )
                    
                    if self.detecter_geste_main_fermee(results.right_hand_landmarks):
                        geste_texte.append("Main droite: Poing")
                    elif self.detecter_geste_paix(results.right_hand_landmarks):
                        geste_texte.append("Main droite: Paix")
                
                # Afficher les informations
                y_offset = 30
                cv2.putText(image, f"Frame: {frame_count}", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                y_offset += 30
                
                cv2.putText(image, f"Donnees: {len(self.landmarks_data)} frames", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                y_offset += 30
                
                if self.recording:
                    cv2.putText(image, "ENREGISTREMENT", (10, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    y_offset += 30
                
                # Afficher les gestes détectés
                for geste in geste_texte:
                    cv2.putText(image, geste, (10, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    y_offset += 30
                
                # Enregistrer la frame si nécessaire
                if self.recording and self.video_writer:
                    self.video_writer.write(image)
                
                cv2.imshow('Detection Avancee - MediaPipe', image)
                
                # Gestion des touches
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    if self.recording:
                        self.arreter_enregistrement()
                    else:
                        self.demarrer_enregistrement(width, height)
                elif key == ord('s'):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"landmarks_{timestamp}.csv"
                    self.exporter_donnees_csv(filename)
                elif key == ord('c'):
                    self.landmarks_data.clear()
                    print("Données effacées")
        
        # Nettoyage
        if self.recording:
            self.arreter_enregistrement()
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Exporter les données finales
        if self.landmarks_data:
            self.exporter_donnees_csv("landmarks_final.csv")
            print(f"Session terminée. {len(self.landmarks_data)} frames analysés.")

def main():
    print("="*60)
    print("    DÉMONSTRATION AVANCÉE - DÉTECTION DE POSE")
    print("    Par Dady Akrou Cyrille - Data Scientist")
    print("="*60)
    print()
    print("Fonctionnalités avancées:")
    print("- Détection de gestes (poing, paix)")
    print("- Sauvegarde des coordonnées des landmarks")
    print("- Enregistrement vidéo avec détection")
    print("- Export des données en CSV")
    print()
    
    input("Appuyez sur Entrée pour commencer...")
    
    detector = DetectionAvancee()
    detector.detection_avancee()

if __name__ == "__main__":
    main()