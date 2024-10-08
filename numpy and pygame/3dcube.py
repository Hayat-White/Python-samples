import pygame
import numpy as np

pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width,height))

pygame.display.set_caption("3d cube")

vertices= np.array([
    [-1,-1,-1],
    [1,-1,-1],
    [1,1,-1],
    [-1,1,-1], 
    [-1,-1,1],
    [1,-1,1],
    [1,1,1],
    [-1,1,1]
])

edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

def rotate_x(angle):
    cos = np.cos(angle)
    sin = np.sin(angle)
    return np.array([
        [1,0,0],
        [0,cos,-sin],
        [0,sin,cos]
        ])

def rotate_y(angle):
    cos = np.cos(angle)
    sin = np.sin(angle)
    return np.array([
        [cos,0,sin],
        [0,1,0],
        [-sin,0,cos]
        ])

def rotate_z(angle):
    cos = np.cos(angle)
    sin = np.sin(angle)
    return np.array([
        [cos,-sin,0],
        [sin,cos,0],
        [0,0,1]
        ])

def project(points):
    scale = 100
    projection_matrix = np.array([
        [1, 0, 0],
        [0, 1, 0]
    ])
    projected_points = []
    for point in points:
        projected_point = np.dot(projection_matrix, point)
        x = int(projected_point[0] * scale) + width // 2
        y = int(projected_point[1] * scale) + height // 2
        projected_points.append((x, y))
    return projected_points

def main():
    clock = pygame.time.Clock()
    angle_x = angle_y = angle_z = 0
    running = True

    while running:
        angle_x += 0.01
        angle_y += 0.01 
        angle_z += 0.01

        screen.fill((0, 0, 0))

        rotation_matrix = np.dot(rotate_x(angle_x), np.dot(rotate_y(angle_y), rotate_z(angle_z)))
        rotated_vertices = np.dot(vertices, rotation_matrix)
        projected_vertices = project(rotated_vertices)

        for edge in edges:
            pygame.draw.line(screen, (0, 0, 255), projected_vertices[edge[0]], projected_vertices[edge[1]], 1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()