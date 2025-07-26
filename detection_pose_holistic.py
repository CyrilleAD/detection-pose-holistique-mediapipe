# Projet de Détection de Pose Holistique avec MediaPipe
# Par Dady Akrou Cyrille - Data Scientist
# Basé sur la vidéo YouTube: https://www.youtube.com/watch?v=pG4sUNDOZFg

# Importation des dépendances
import mediapipe as mp
import cv2

# Configuration de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# Fonction principale pour la détection en temps réel
def detection_pose_holistic():
    """
    Fonction principale qui lance la détection de pose holistique en temps réel
    Détecte les landmarks du visage, des mains et du corps
    """
    
    # Initialisation de la capture vidéo
    cap = cv2.VideoCapture(0)
    
    # Configuration du modèle holistique
    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:
        
        while cap.isOpened():
            # Lecture du frame de la webcam
            ret, frame = cap.read()
            
            if not ret:
                print("Impossible de lire le frame de la webcam")
                break
            
            # Conversion de BGR vers RGB (requis par MediaPipe)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Traitement de l'image avec le modèle holistique
            results = holistic.process(image)
            
            # Conversion de RGB vers BGR pour l'affichage avec OpenCV
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Définition des styles de dessin pour chaque type de landmark
            
            # Style pour les landmarks du visage (rouge)
            face_landmark_style = mp_drawing.DrawingSpec(
                color=(0, 0, 255), thickness=1, circle_radius=1
            )
            face_connection_style = mp_drawing.DrawingSpec(
                color=(0, 0, 255), thickness=1, circle_radius=1
            )
            
            # Style pour la main droite (bleu)
            right_hand_landmark_style = mp_drawing.DrawingSpec(
                color=(255, 0, 0), thickness=2, circle_radius=4
            )
            right_hand_connection_style = mp_drawing.DrawingSpec(
                color=(240, 0, 0), thickness=2, circle_radius=2
            )
            
            # Style pour la main gauche (vert)
            left_hand_landmark_style = mp_drawing.DrawingSpec(
                color=(0, 255, 0), thickness=2, circle_radius=4
            )
            left_hand_connection_style = mp_drawing.DrawingSpec(
                color=(0, 240, 0), thickness=2, circle_radius=2
            )
            
            # Style pour la pose du corps (jaune)
            pose_landmark_style = mp_drawing.DrawingSpec(
                color=(0, 255, 255), thickness=2, circle_radius=4
            )
            pose_connection_style = mp_drawing.DrawingSpec(
                color=(0, 240, 240), thickness=2, circle_radius=2
            )
            
            # Dessin des landmarks du visage
            if results.face_landmarks:
                mp_drawing.draw_landmarks(
                    image, 
                    results.face_landmarks, 
                    mp_holistic.FACEMESH_CONTOURS,
                    face_landmark_style,
                    face_connection_style
                )
            
            # Dessin des landmarks de la main droite
            if results.right_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, 
                    results.right_hand_landmarks, 
                    mp_holistic.HAND_CONNECTIONS,
                    right_hand_landmark_style,
                    right_hand_connection_style
                )
            
            # Dessin des landmarks de la main gauche
            if results.left_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, 
                    results.left_hand_landmarks, 
                    mp_holistic.HAND_CONNECTIONS,
                    left_hand_landmark_style,
                    left_hand_connection_style
                )
            
            # Dessin des landmarks de la pose du corps
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image, 
                    results.pose_landmarks, 
                    mp_holistic.POSE_CONNECTIONS,
                    pose_landmark_style,
                    pose_connection_style
                )
            
            # Affichage du résultat
            cv2.imshow('Détection de Pose Holistique - MediaPipe', image)
            
            # Sortie avec la touche 'q'
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    
    # Libération des ressources
    cap.release()
    cv2.destroyAllWindows()

# Fonction pour tester uniquement la webcam
def test_webcam():
    """
    Fonction pour tester la webcam sans détection
    """
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            print("Impossible de lire le frame de la webcam")
            break
        
        cv2.imshow('Test Webcam', frame)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Fonction pour afficher les informations sur les landmarks détectés
def afficher_landmarks_info(results):
    """
    Affiche les informations sur les landmarks détectés
    """
    print("=== Informations sur les landmarks détectés ===")
    
    if results.face_landmarks:
        print(f"Landmarks du visage détectés: {len(results.face_landmarks.landmark)} points")
    else:
        print("Aucun landmark du visage détecté")
    
    if results.pose_landmarks:
        print(f"Landmarks de pose détectés: {len(results.pose_landmarks.landmark)} points")
    else:
        print("Aucun landmark de pose détecté")
    
    if results.left_hand_landmarks:
        print(f"Landmarks main gauche détectés: {len(results.left_hand_landmarks.landmark)} points")
    else:
        print("Aucun landmark main gauche détecté")
    
    if results.right_hand_landmarks:
        print(f"Landmarks main droite détectés: {len(results.right_hand_landmarks.landmark)} points")
    else:
        print("Aucun landmark main droite détecté")
    
    print("="*50)

# Fonction principale avec menu
def main():
    """
    Fonction principale avec menu de choix
    """
    try:
        print("="*60)
        print("    PROJET DE DÉTECTION DE POSE HOLISTIQUE")
        print("    Par Dady Akrou Cyrille - Data Scientist")
        print("    Utilisant MediaPipe et OpenCV")
        print("="*60)
        print()
        
        # Vérification rapide des imports
        print("Vérification des dépendances...")
        print(f"OpenCV version: {cv2.__version__}")
        print(f"MediaPipe version: {mp.__version__}")
        print("✅ Toutes les dépendances sont OK!")
        print()
        
        print("Choisissez une option:")
        print("1. Lancer la détection de pose holistique complète")
        print("2. Tester uniquement la webcam")
        print("3. Quitter")
        print()
        
        while True:
            choix = input("Votre choix (1-3): ")
            
            if choix == '1':
                print("\nLancement de la détection de pose holistique...")
                print("Appuyez sur 'q' pour quitter")
                print("Assurez-vous que votre webcam est connectée et fonctionnelle")
                input("Appuyez sur Entrée pour continuer...")
                try:
                    detection_pose_holistic()
                except Exception as e:
                    print(f"Erreur lors de la détection: {e}")
                    print("Essayez d'abord le test de la webcam (option 2)")
                break
            
            elif choix == '2':
                print("\nTest de la webcam...")
                print("Appuyez sur 'q' pour quitter")
                input("Appuyez sur Entrée pour continuer...")
                try:
                    test_webcam()
                except Exception as e:
                    print(f"Erreur lors du test de la webcam: {e}")
                break
            
            elif choix == '3':
                print("Au revoir!")
                break
            
            else:
                print("Choix invalide. Veuillez choisir 1, 2 ou 3.")
                
    except KeyboardInterrupt:
        print("\n\nProgramme interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        print("Veuillez vérifier votre installation de MediaPipe et OpenCV.")

if __name__ == "__main__":
    main()