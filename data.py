import numpy as np

Source = [
	np.array([-3, -3, 0]),
]
ColSrc = [
	np.array([1.2, 1.2, 1.1]),
]

Objet = [
	(np.array([0, 0, -100]), 30), 
	(np.array([-5, 0, -30]), 1),
	(np.array([4, 0, -20]), 1), 
]
KdObjet = [
	np.array([229., 196., 143.]) * (1 / 255), 
	np.array([171., 140., 120.]) * (1 / 255),
	np.array([35., 42., 70.])    * (1 / 255), 
]

# Variable utiles pour régler omega (== viewer)
fov_angle = np.pi / 6 # Angle de vision de l'observateur
view_distance = 2     # Distance à laquelle il se trouve de l'écran

Delta = np.tan(fov_angle) * view_distance
PX_COUNT = 1000 # == N dans l'énoncé mais conflit de nom avec la normale de couleur_diffusee
viewer = np.array([0, 0, view_distance]) # == omega; pour la même raison

background_color = np.array([0.1, 0.1, 0.1])