import math
import numpy as np

from data import *

# Rayon de S dirigé par u: (S, u)
# Sphère centre C, rayon r: (C, r)

### PART I : Géométrie
def vec(A, B):
	return B - A

def ps(v1, v2):
	return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def norme_sq(v):
	return ps(v,v)

def norme(v):
	return math.sqrt(norme_sq(v))

def unitaire(v):
	return (1 / norme(v)) * v

def pt(r, t): # Point à la distance t du rayon r
	assert t >= 0
	(S, u) = r
	return S + t * u

def dir(A, B): # Vecteur unitaire de la direction de A vers B
	return unitaire(vec(A, B))

def ra(A, B): # Rayon venant de A vers B
	return A, dir(A, B)

def sp(A, B): # Sphère centre A passant par B (donc rayon AB)
	return A, norme(vec(A,B))

def intersection(r, s):
	(A, u) = r
	(C, rayon) = s

	CA = vec(C, A)
	prod_uCA = ps(u, CA)

	discr = 4 * prod_uCA*prod_uCA - 4 * (norme_sq(CA) - rayon*rayon)

	if discr < 0:
		return None
	else:
		t = -0.5 * (2 * prod_uCA + math.sqrt(discr))
		return pt(r, t), t

### PART II : Optique
noir  = np.array([0., 0., 0.])
blanc = np.array([1., 1., 1.])

def au_dessus(s, P, src):
	(C, _) = s
	return ps(vec(P,src), vec(C,P)) > 0

def visible(obj, j, P, src):
	if not au_dessus(obj[j], P, src):
		return False
	
	ray = ra(src, P)
	point_dist_sq = norme_sq(vec(src, P))

	for i in range(len(obj)):
		inter = intersection(ray, obj[i])

		if inter is not None:
			(_, dist) = inter
			if dist*dist < point_dist_sq - 1e-2: # Si ce point est plus proche que P, alors P est caché
				return False             # Le 1e-2 est là car la comparaison de flottants est approximatives et il se peut que si dist == point_dist, celui soit considéré comme <
				
	return True

def couleur_difusee(r, Cs, N, kd):
	(_, u) = r
	cos_theta = ps(u, unitaire(N))
	return kd * Cs * cos_theta

def rayon_reflechi(s, P, src):
	(C, _) = s
	N = dir(C, P)
	u = vec(src, P)

	w = u - 2*ps(N,u)*N

	return w

### PART IV - Lancer de rayons

def grille(i, j):
	px_size = Delta / PX_COUNT
	return np.array([(i + 0.5) * px_size, (j + 0.5) * px_size, 0])

def rayon_ecran(omega, i, j):
	E = grille(i, j)
	return ra(omega, E)

# Version modifiée de rayon_ecran pour unire l'observateur et l'écran et avoir une caméra
# qui "filme" de sorte à ce que l'origine de la scène soit au centre de l'écran
def rayon_camera(omega, i, j):
	E = grille(i, j)
	E[0] -= Delta / 2
	E[1] -= Delta / 2

	return ra(omega, E)

def interception(r):
	closer_point, closer_dist = None, 0
	closer_obj = 0

	for i in range(len(Objet)):
		inter = intersection(r, Objet[i])

		if inter is not None:
			(point, dist) = inter
			if closer_point is None or dist < closer_dist:
				closer_point, closer_dist = point, dist
				closer_obj = i
	
	if closer_point is None:
		return None
	
	return (closer_point, closer_obj)

def couleur_difusion(P, j):
	Cd = noir.copy()
	(C, _) = Objet[j]
	Kd = KdObjet[j]
	for i in range(len(Source)):
		if visible(Objet, j, P, Source[i]):
			S, Cs = Source[i], ColSrc[i]
			r = ra(P, S)

			Cd += couleur_difusee(r, Cs, dir(C, P), Kd)

	return Cd

def lancer(omega, fond):
	im = np.full((PX_COUNT, PX_COUNT, 3), fill_value=fond)

	for j in range(PX_COUNT):
		for i in range(PX_COUNT):
			ray = rayon_camera(omega, i, j)
			inter = interception(ray)

			if inter is not None:
				(P, obj_id) = inter
				im[i,j] = couleur_difusion(P, obj_id)
	
	return im