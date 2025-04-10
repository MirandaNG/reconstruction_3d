import cv2
import numpy as np
from scipy.spatial import Delaunay
from .exporter import exportar_modelo_obj, guardar_como_obj

def generar_relieve_desde_una_imagen(ruta_imagen):
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("[ERROR] No se pudo cargar la imagen.")
        return

    height_map = cv2.GaussianBlur(img, (5, 5), 0)
    h, w = height_map.shape

    vertices = []
    vertex_idx = {}
    faces = []

    def obtener_o_crear_vertice(x, y, z):
        clave = (x, y)
        if clave not in vertex_idx:
            vertex_idx[clave] = len(vertices)
            vertices.append((x, y, z))
        return vertex_idx[clave]

    for y in range(h - 1):
        for x in range(w - 1):
            z = height_map[y, x] / 10.0
            z1 = height_map[y + 1, x] / 10.0
            z2 = height_map[y, x + 1] / 10.0
            z3 = height_map[y + 1, x + 1] / 10.0

            v0 = obtener_o_crear_vertice(x, y, z)
            v1 = obtener_o_crear_vertice(x, y + 1, z1)
            v2 = obtener_o_crear_vertice(x + 1, y, z2)
            v3 = obtener_o_crear_vertice(x + 1, y + 1, z3)

            faces.append((v0, v1, v2))
            faces.append((v2, v1, v3))

    guardar_como_obj(ruta_imagen, vertices, faces)

def procesar_imagenes_con_triangulacion(imagenes):
    print("[INFO] Procesando imágenes para triangulación múltiple...")

    # Leer las imágenes
    imgs = [cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) for img_path in imagenes]
    if any(img is None for img in imgs):
        print("[ERROR] Al menos una imagen no se pudo cargar.")
        return

    sift = cv2.SIFT_create()
    puntos_3d_acumulados = []
    kp_acumulados = []  # Para almacenar los puntos clave de todas las imágenes
    des_acumulados = []  # Para almacenar los descriptores de todas las imágenes

    # Detectar y extraer características en cada imagen
    for img in imgs:
        kp, des = sift.detectAndCompute(img, None)
        kp_acumulados.append(kp)
        des_acumulados.append(des)

    bf = cv2.BFMatcher()
    puntos_3d_totales = []

    # Emparejar características entre imágenes consecutivas
    for i in range(len(imgs) - 1):
        img1 = imgs[i]
        img2 = imgs[i + 1]
        kp1, des1 = kp_acumulados[i], des_acumulados[i]
        kp2, des2 = kp_acumulados[i + 1], des_acumulados[i + 1]

        matches = bf.knnMatch(des1, des2, k=2)

        # Filtrar buenos matches
        buenos = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                buenos.append(m)

        pts1 = np.float32([kp1[m.queryIdx].pt for m in buenos])
        pts2 = np.float32([kp2[m.trainIdx].pt for m in buenos])

        if len(pts1) >= 8 and len(pts2) >= 8:
            # Estimar matriz esencial y pose de la cámara
            E, _ = cv2.findEssentialMat(pts1, pts2, method=cv2.RANSAC)
            _, R, t, _ = cv2.recoverPose(E, pts1, pts2)

            # Triangulación
            K = np.array([[1, 0, 0],
                          [0, 1, 0],
                          [0, 0, 1]])
            proj1 = np.hstack((np.eye(3), np.zeros((3, 1))))
            proj2 = np.hstack((R, t))

            pts4d = cv2.triangulatePoints(K @ proj1, K @ proj2, pts1.T, pts2.T)
            pts4d /= pts4d[3]  # Convertir a coordenadas homogéneas

            puntos_3d_totales.extend(pts4d[:3].T)

    if puntos_3d_totales:
        # Generar el modelo 3D final
        exportar_modelo_obj(puntos_3d_totales, imagenes[0])  # Usa el nombre de la primera imagen
    else:
        print("[ERROR] No se generaron puntos 3D.")

