import pygame

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 1 - Filling Any Polygon")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Lista de polígonos
polygons = [
    [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330),
     (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)],
    
    [(321, 335), (288, 286), (339, 251), (374, 302)],
    
    [(377, 249), (411, 197), (436, 249)],
    
    [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36),
     (676, 37), (660, 52), (750, 145), (761, 179), (672, 192),
     (659, 214), (615, 214), (632, 230), (580, 230), (597, 215),
     (552, 214), (517, 144), (466, 180)],
    
    [(682, 175), (708, 120), (735, 148), (739, 170)]  # Este es un agujero dentro del anterior
]

# Función de dibujo de líneas (opcional para depuración)
def draw_polygon_edges(surface, points, color=BLACK):
    for i in range(len(points)):
        pygame.draw.line(surface, color, points[i], points[(i + 1) % len(points)], 1)

# Algoritmo básico de Scanline Fill
def scanline_fill(surface, polygon, color):
    # Ordenar vértices por Y
    edges = []
    n = len(polygon)
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        if p1[1] == p2[1]:
            continue  # ignorar líneas horizontales
        if p1[1] > p2[1]:
            p1, p2 = p2, p1
        edges.append({
            "y_min": p1[1],
            "y_max": p2[1],
            "x": p1[0],
            "inv_slope": (p2[0] - p1[0]) / (p2[1] - p1[1])
        })

    y_min = min(p[1] for p in polygon)
    y_max = max(p[1] for p in polygon)

    aet = []  # Active Edge Table

    for y in range(y_min, y_max):
        # Agregar nuevas aristas
        for edge in edges:
            if edge["y_min"] == y:
                aet.append(dict(edge))

        # Eliminar aristas que ya no cruzan este Y
        aet = [e for e in aet if e["y_max"] > y]

        # Ordenar por X actual
        aet.sort(key=lambda e: e["x"])

        # Rellenar entre pares de intersecciones
        for i in range(0, len(aet), 2):
            x_start = int(aet[i]["x"])
            x_end = int(aet[i + 1]["x"])
            pygame.draw.line(surface, color, (x_start, y), (x_end, y))

        # Avanzar X en las aristas activas
        for edge in aet:
            edge["x"] += edge["inv_slope"]

# Loop principal
running = True
while running:
    screen.fill(WHITE)

    # Polígonos a rellenar
    for i, poly in enumerate(polygons):
        if i == 4:
            # agujero, se rellena con blanco
            scanline_fill(screen, poly, WHITE)
        else:
            scanline_fill(screen, poly, RED)
        draw_polygon_edges(screen, poly, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
