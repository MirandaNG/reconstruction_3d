import cv2
import numpy as np
import os

def generar_relieve_desde_una_imagen(ruta_imagen):
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("[ERROR] No se pudo cargar la imagen.")
        return

    height_map = cv2.GaussianBlur(img, (5, 5), 0)
    h, w = height_map.shape

    vertices = []
    faces = []

    for y in range(h - 1):
        for x in range(w - 1):
            z = height_map[y, x] / 10.0
            z1 = height_map[y + 1, x] / 10.0
            z2 = height_map[y, x + 1] / 10.0
            z3 = height_map[y + 1, x + 1] / 10.0

            idx = len(vertices)
            vertices.extend([
                (x, y, z),
                (x, y + 1, z1),
                (x + 1, y, z2),
                (x + 1, y + 1, z3)
            ])

            faces.append((idx + 0, idx + 1, idx + 2))
            faces.append((idx + 2, idx + 1, idx + 3))

    guardar_como_obj("outputs/relieve.obj", vertices, faces)
    print("[OK] Modelo 3D de relieve guardado como relieve.obj")


def procesar_imagenes_con_triangulacion(imagenes):
    img1 = cv2.imread(imagenes[0])
    img2 = cv2.imread(imagenes[1])
    if img1 is None or img2 is None:
        print("[ERROR] No se pudieron cargar las imágenes.")
        return

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    if len(good) < 8:
        print("[ERROR] No se encontraron suficientes coincidencias.")
        return

    pts1 = np.float32([kp1[m.queryIdx].pt for m in good])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good])

    E, _ = cv2.findEssentialMat(pts1, pts2, method=cv2.RANSAC, prob=0.999, threshold=1.0)
    _, R, t, _ = cv2.recoverPose(E, pts1, pts2)

    proj1 = np.hstack((np.eye(3), np.zeros((3, 1))))
    proj2 = np.hstack((R, t))

    pts4d = cv2.triangulatePoints(proj1, proj2, pts1.T, pts2.T)
    pts4d /= pts4d[3]

    vertices = [tuple(p[:3]) for p in pts4d.T]
    faces = []  # sin topología definida

    guardar_como_obj("outputs/triangulacion.obj", vertices, faces)
    print("[OK] Nube de puntos triangulada guardada como triangulacion.obj")


def guardar_como_obj(ruta, vertices, caras):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w') as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for c in caras:
            f.write(f"f {c[0]+1} {c[1]+1} {c[2]+1}\n")
