# 📚 Documentation Technique - Détection de Pose Holistique

**Par Dady Akrou Cyrille - Data Scientist**

## 🎯 Vue d'ensemble

Ce document fournit une documentation technique détaillée du projet de détection de pose holistique utilisant MediaPipe et OpenCV. Le système permet la détection simultanée et en temps réel des landmarks du visage, des mains et du corps humain.

## 🏗️ Architecture du Projet

### Structure des Fichiers

```
📦 detection-pose-holistique-mediapipe/
├── 📄 detection_pose_holistic.py    # Script principal avec interface utilisateur
├── 📄 demo_avance.py                # Démonstration des fonctionnalités avancées
├── 📄 test_simple.py                # Tests de vérification du système
├── 📄 requirements.txt              # Dépendances Python
├── 📄 README.md                     # Documentation utilisateur
├── 📄 DOCUMENTATION_TECHNIQUE.md    # Documentation technique (ce fichier)
├── 📄 PRESENTATION_PROJET.md        # Présentation du projet
└── 📄 transcription.txt             # Transcription de la vidéo source
```

### Diagramme d'Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Webcam Input  │───▶│   MediaPipe      │───▶│   Landmarks     │
│   (OpenCV)      │    │   Holistic       │    │   Detection     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Visualization │◀───│   Processing     │───▶│   Data Export   │
│   (OpenCV)      │    │   & Analysis     │    │   (CSV)         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 Technologies Utilisées

### MediaPipe

**Version requise :** >= 0.10.0

**Composants utilisés :**
- `mp.solutions.holistic` : Modèle de détection holistique
- `mp.solutions.drawing_utils` : Utilitaires de dessin

**Configuration du modèle :**
```python
with mp_holistic.Holistic(
    min_detection_confidence=0.5,  # Seuil de confiance pour la détection
    min_tracking_confidence=0.5     # Seuil de confiance pour le suivi
) as holistic:
```

### OpenCV

**Version requise :** >= 4.8.0

**Fonctionnalités utilisées :**
- Capture vidéo : `cv2.VideoCapture()`
- Conversion d'espace colorimétrique : `cv2.cvtColor()`
- Affichage : `cv2.imshow()`
- Enregistrement vidéo : `cv2.VideoWriter()`

### NumPy

**Version requise :** >= 1.21.0

**Utilisation :**
- Manipulation des arrays d'images
- Calculs mathématiques pour les landmarks

## 🧠 Fonctionnement de MediaPipe Holistic

### Pipeline de Traitement

1. **Préprocessing :**
   - Conversion BGR → RGB
   - Normalisation de l'image

2. **Détection :**
   - Détection du visage
   - Détection de la pose corporelle
   - Détection des mains

3. **Postprocessing :**
   - Extraction des landmarks
   - Calcul des coordonnées normalisées

### Modèles Intégrés

- **Face Mesh :** 468 landmarks faciaux
- **Pose :** 33 landmarks corporels
- **Hands :** 21 landmarks par main

## 📊 Structure des Landmarks

### Landmarks du Visage (468 points)

```python
# Accès aux landmarks du visage
if results.face_landmarks:
    for landmark in results.face_landmarks.landmark:
        x = landmark.x  # Coordonnée X normalisée [0-1]
        y = landmark.y  # Coordonnée Y normalisée [0-1]
        z = landmark.z  # Profondeur relative
```

### Landmarks de la Pose (33 points)

**Points principaux :**
- 0-10 : Visage et tête
- 11-22 : Torse et bras
- 23-32 : Hanches et jambes

```python
# Exemple d'accès aux épaules
left_shoulder = results.pose_landmarks.landmark[11]
right_shoulder = results.pose_landmarks.landmark[12]
```

### Landmarks des Mains (21 points chacune)

**Structure :**
- 0 : Poignet
- 1-4 : Pouce
- 5-8 : Index
- 9-12 : Majeur
- 13-16 : Annulaire
- 17-20 : Auriculaire

## 🎨 Système de Rendu

### Styles de Dessin

```python
# Configuration des styles
face_style = mp_drawing.DrawingSpec(
    color=(0, 0, 255),    # Rouge (BGR)
    thickness=1,
    circle_radius=1
)

pose_style = mp_drawing.DrawingSpec(
    color=(0, 255, 255),  # Jaune (BGR)
    thickness=2,
    circle_radius=4
)
```

### Couleurs par Type

| Type | Couleur | Code BGR | Usage |
|------|---------|----------|-------|
| Visage | Rouge | (0, 0, 255) | Landmarks faciaux |
| Corps | Jaune | (0, 255, 255) | Pose corporelle |
| Main gauche | Vert | (0, 255, 0) | Main gauche |
| Main droite | Bleu | (255, 0, 0) | Main droite |

## 🧮 Algorithmes de Détection

### Détection de Gestes

#### Poing Fermé

```python
def detecter_geste_main_fermee(self, hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Extrémités des doigts
    finger_pips = [3, 6, 10, 14, 18]  # Articulations PIP
    
    fingers_down = 0
    
    # Vérification pour chaque doigt
    for i in range(1, 5):
        if hand_landmarks.landmark[finger_tips[i]].y > hand_landmarks.landmark[finger_pips[i]].y:
            fingers_down += 1
    
    # Logique spéciale pour le pouce
    if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_pips[0]].x:
        fingers_down += 1
    
    return fingers_down >= 4
```

#### Geste de Paix

```python
def detecter_geste_paix(self, hand_landmarks):
    # Index et majeur étendus, autres pliés
    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    ring_down = hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y
    pinky_down = hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y
    
    return index_up and middle_up and ring_down and pinky_down
```

### Calcul de Distance

```python
def calculer_distance(self, point1, point2):
    """Distance euclidienne entre deux landmarks"""
    return math.sqrt(
        (point1.x - point2.x)**2 + 
        (point1.y - point2.y)**2
    )
```

## ⚡ Optimisations de Performance

### Paramètres de Confiance

- **min_detection_confidence :** Seuil pour la détection initiale
- **min_tracking_confidence :** Seuil pour le suivi continu

**Recommandations :**
- Valeurs élevées (0.7-0.9) : Plus de précision, moins de détections
- Valeurs faibles (0.3-0.5) : Plus de détections, moins de précision

### Optimisation de la Webcam

```python
# Configuration optimale
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
```

### Gestion Mémoire

```python
# Libération des ressources
cap.release()
cv2.destroyAllWindows()
if self.video_writer:
    self.video_writer.release()
```

## 💾 Export et Sauvegarde

### Format CSV

```csv
frame,timestamp,type,landmark_id,x,y,z
1,2024-01-01T10:00:00,face,0,0.5,0.3,0.1
1,2024-01-01T10:00:00,pose,11,0.4,0.6,0.2
```

### Enregistrement Vidéo

```python
# Configuration de l'enregistrement
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(
    filename, 
    fourcc, 
    fps, 
    (width, height)
)
```

## 🔍 Cas d'Usage Avancés

### Analyse de Mouvement

```python
# Calcul de la vitesse de mouvement
def calculer_vitesse(landmarks_t1, landmarks_t2, delta_time):
    distance = calculer_distance(landmarks_t1, landmarks_t2)
    return distance / delta_time
```

### Détection d'Activité

```python
# Détection de mouvement significatif
def detecter_mouvement(landmarks_history, seuil=0.05):
    if len(landmarks_history) < 2:
        return False
    
    distance = calculer_distance(
        landmarks_history[-1], 
        landmarks_history[-2]
    )
    
    return distance > seuil
```

## 🚨 Gestion d'Erreurs

### Erreurs Communes

1. **Webcam non disponible**
   ```python
   if not cap.isOpened():
       raise RuntimeError("Impossible d'ouvrir la webcam")
   ```

2. **Frame invalide**
   ```python
   ret, frame = cap.read()
   if not ret:
       continue  # Passer au frame suivant
   ```

3. **Landmarks non détectés**
   ```python
   if results.pose_landmarks is None:
       # Gérer l'absence de détection
       pass
   ```

## 🛠️ Dépannage

### Problèmes de Performance

**Symptômes :** FPS faible, latence élevée

**Solutions :**
- Réduire la résolution de la webcam
- Augmenter les seuils de confiance
- Fermer les applications gourmandes

### Problèmes de Détection

**Symptômes :** Landmarks non détectés

**Solutions :**
- Améliorer l'éclairage
- Réduire les seuils de confiance
- Vérifier la position face à la caméra

### Erreurs d'Installation

**Problème :** Import MediaPipe échoue

**Solution :**
```bash
pip uninstall mediapipe
pip install mediapipe --no-cache-dir
```

## 📈 Métriques de Performance

### Benchmarks Typiques

| Configuration | FPS | Latence | CPU Usage |
|---------------|-----|---------|----------|
| 640x480, conf=0.5 | 25-30 | 33ms | 40-60% |
| 1280x720, conf=0.7 | 15-20 | 50ms | 60-80% |
| 320x240, conf=0.3 | 40-50 | 20ms | 20-40% |

### Optimisation Recommandée

```python
# Configuration équilibrée
HOLISTIC_CONFIG = {
    'min_detection_confidence': 0.5,
    'min_tracking_confidence': 0.5,
    'model_complexity': 1,  # 0=lite, 1=full, 2=heavy
    'smooth_landmarks': True
}
```

## 🔮 Extensions Possibles

### Intégration IA

- Classification de gestes avec TensorFlow
- Reconnaissance d'émotions
- Analyse comportementale

### Interfaces

- Interface web avec Flask/FastAPI
- Application mobile avec Kivy
- Interface desktop avec Tkinter/PyQt

### Données

- Base de données pour stockage historique
- API REST pour accès distant
- Streaming en temps réel

---

**Auteur :** Dady Akrou Cyrille - Data Scientist  
**Version :** 1.0  
**Dernière mise à jour :** Janvier 2024