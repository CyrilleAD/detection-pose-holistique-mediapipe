# 🤖 Détection de Pose Holistique avec MediaPipe

**Par Dady Akrou Cyrille - Data Scientist**

Ce projet implémente un système de détection de pose holistique en temps réel utilisant MediaPipe et OpenCV. Il permet de détecter simultanément :
- 🎭 **Landmarks du visage** (468 points)
- 🤲 **Landmarks des mains** (21 points par main)
- 🏃 **Landmarks du corps** (33 points)

## 📋 Fonctionnalités

- ✅ Détection en temps réel via webcam
- ✅ Visualisation colorée des différents types de landmarks
- ✅ Interface utilisateur simple avec menu de choix
- ✅ Code modulaire et bien documenté
- ✅ Gestion d'erreurs et test de webcam

## 🎯 Basé sur la vidéo YouTube

Ce projet est inspiré de la vidéo : [AI Face Body and Hand Pose Detection with Python and Mediapipe](https://www.youtube.com/watch?v=pG4sUNDOZFg)

## 🛠️ Installation

### Prérequis
- Python 3.7 ou plus récent
- Une webcam fonctionnelle
- Windows/macOS/Linux

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou installation manuelle :

```bash
pip install mediapipe opencv-python numpy matplotlib
```

## 🚀 Utilisation

### Lancement du programme

```bash
python detection_pose_holistic.py
```

### Menu principal

Le programme propose 3 options :
1. **Détection holistique complète** - Lance la détection de tous les landmarks
2. **Test webcam** - Teste uniquement la webcam sans détection
3. **Quitter** - Ferme le programme

### Contrôles
- **Touche 'q'** : Quitter la détection en cours
- **Échap** : Alternative pour quitter

## 🎨 Couleurs des Landmarks

- 🔴 **Rouge** : Landmarks du visage
- 🔵 **Bleu** : Main droite
- 🟢 **Vert** : Main gauche  
- 🟡 **Jaune** : Pose du corps

## 📁 Structure du Projet

```
📦 detection-pose-holistique-mediapipe/
├── 📄 detection_pose_holistic.py    # Script principal
├── 📄 demo_avance.py                # Démonstration avancée
├── 📄 test_simple.py                # Tests de vérification
├── 📄 requirements.txt              # Dépendances
├── 📄 README.md                     # Documentation
├── 📄 DOCUMENTATION_TECHNIQUE.md    # Documentation technique
├── 📄 PRESENTATION_PROJET.md        # Présentation du projet
└── 📄 transcription.txt             # Transcription de la vidéo source
```

## 🔧 Configuration Avancée

### Paramètres de détection

Vous pouvez ajuster les paramètres de confiance dans le code :

```python
with mp_holistic.Holistic(
    min_detection_confidence=0.5,  # Confiance minimale pour la détection
    min_tracking_confidence=0.5     # Confiance minimale pour le suivi
) as holistic:
```

### Personnalisation des couleurs

Modifiez les couleurs dans les `DrawingSpec` :

```python
# Format BGR (Blue, Green, Red)
face_landmark_style = mp_drawing.DrawingSpec(
    color=(0, 0, 255),    # Rouge
    thickness=1, 
    circle_radius=1
)
```

## 🚨 Résolution de Problèmes

### Webcam non détectée
- Vérifiez que votre webcam est connectée
- Essayez de changer l'index de la webcam dans le code :
  ```python
  cap = cv2.VideoCapture(1)  # Essayez 0, 1, 2, etc.
  ```

### Performance lente
- Réduisez la résolution de la webcam
- Augmentez les seuils de confiance
- Fermez les autres applications utilisant la webcam

### Erreurs d'installation
- Assurez-vous d'avoir Python 3.7+
- Utilisez un environnement virtuel :
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  pip install -r requirements.txt
  ```

## 🎓 Applications Possibles

Ce projet peut être étendu pour :
- 💪 **Comptage d'exercices** (squats, pompes, etc.)
- 🎮 **Contrôle de jeux** sans manette
- 😊 **Analyse d'émotions** et langage corporel
- 🖥️ **Interface tactile** sans contact
- 🏥 **Rééducation** et suivi médical
- 🎬 **Capture de mouvement** pour l'animation

## 📚 Ressources Supplémentaires

- [Documentation MediaPipe](https://mediapipe.dev/)
- [Documentation OpenCV](https://docs.opencv.org/)
- [Vidéo source YouTube](https://www.youtube.com/watch?v=pG4sUNDOZFg)

## 👨‍💻 Auteur

**Dady Akrou Cyrille**  
Data Scientist passionné par l'IA et la vision par ordinateur

---

⭐ **N'hésitez pas à mettre une étoile si ce projet vous a été utile !**