import pygame
from src.core.graph import Graph
from src.model.ZoneType import ZoneType


class Visualizer:
    def __init__(self, graph: Graph):
        self.graph = graph
        pygame.init()
        self.width, self.height = 1000, 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Drone Simulation")
        self.font = pygame.font.SysFont("Arial", 16)
        self.node_positions: dict[str, tuple[int, int]] = {}

    def draw_map(self):
        self.screen.fill((30, 30, 40))

        for (u, v) in self.graph.connections_capacities.keys():
            if u in self.node_positions and v in self.node_positions:
                pos1 = self.node_positions[u]
                pos2 = self.node_positions[v]
                pygame.draw.line(self.screen, (100, 100, 100), pos1, pos2, 2)
        for hub, pos in self.node_positions.items():
            color = (70, 130, 180)
            if hub == self.graph.start_hub:
                color = (46, 204, 113)
            elif hub == self.graph.end_hub:
                color = (231, 76, 60)
            elif self.graph.get_hub_type(hub) == ZoneType.restricted:
                color = (241, 196, 15)
            pygame.draw.circle(self.screen, color, pos, 20)
            text = self.font.render(hub, True, (255, 255, 255))
            self.screen.blit(text, (pos[0] - 10, pos[1] - 30))

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_map()
            pygame.display.flip()
        pygame.quit()