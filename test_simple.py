#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour vérifier que tout fonctionne
Par Dady Akrou Cyrille - Data Scientist
"""

import cv2
import mediapipe as mp
import numpy as np

def test_imports():
    """Test des imports"""
    print("Test des imports...")
    print(f"OpenCV version: {cv2.__version__}")
    print(f"MediaPipe version: {mp.__version__}")
    print(f"NumPy version: {np.__version__}")
    print("Tous les imports sont OK!")

def test_webcam_simple():
    """Test simple de la webcam"""
    print("\nTest de la webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la webcam")
        return False
    
    print("Webcam ouverte avec succès!")
    print("Appuyez sur 'q' pour quitter")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Erreur: Impossible de lire le frame")
            break
        
        frame_count += 1
        
        # Afficher le compteur de frames
        cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Test Webcam Simple', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"Test terminé. {frame_count} frames capturés.")
    return True

def test_mediapipe_simple():
    """Test simple de MediaPipe"""
    print("\nTest de MediaPipe...")
    
    try:
        # Initialisation de MediaPipe
        mp_holistic = mp.solutions.holistic
        mp_drawing = mp.solutions.drawing_utils
        
        print("MediaPipe initialisé avec succès!")
        
        # Test avec une image simple
        with mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as holistic:
            print("Modèle Holistic créé avec succès!")
            
            # Créer une image de test
            test_image = np.zeros((480, 640, 3), dtype=np.uint8)
            test_image_rgb = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
            
            # Traitement de l'image de test
            results = holistic.process(test_image_rgb)
            print("Traitement de l'image de test réussi!")
            
        return True
        
    except Exception as e:
        print(f"Erreur MediaPipe: {e}")
        return False

def main():
    print("="*50)
    print("    TEST SIMPLE DU PROJET")
    print("    Par Dady Akrou Cyrille")
    print("="*50)
    
    # Test des imports
    test_imports()
    
    # Test de MediaPipe
    if test_mediapipe_simple():
        print("\n✅ MediaPipe fonctionne correctement!")
    else:
        print("\n❌ Problème avec MediaPipe")
        return
    
    # Test de la webcam
    print("\nVoulez-vous tester la webcam? (o/n): ", end="")
    choix = input().lower()
    
    if choix in ['o', 'oui', 'y', 'yes']:
        if test_webcam_simple():
            print("\n✅ Webcam fonctionne correctement!")
        else:
            print("\n❌ Problème avec la webcam")
    
    print("\nTest terminé!")

if __name__ == "__main__":
    main()