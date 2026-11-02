import pygame
from src.core.graph import Graph
from src.model.ZoneType import ZoneType
from src.core.Dron import Dron


class Visualizer:
    def __init__(
        self, graph: Graph, drones: list[Dron], max_turns: int
    ) -> None:
        self.graph = graph
        self.drones = drones
        self.max_turns = max_turns
        self.current_turn = 0
        pygame.init()
        self.width, self.height = 1000, 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Drone Simulation")
        self.font = pygame.font.SysFont("Arial", 16)
        self.node_positions: dict[str, tuple[int, int]] = {}
        self._generate_layout()

    def _generate_layout(self):
        if not self.graph.hubs:
            return
        all_coords = [
            self.graph.get_coordinates(name) for name in self.graph.hubs
            ]
        min_x = min(coord[0] for coord in all_coords)
        max_x = max(coord[0] for coord in all_coords)
        min_y = min(coord[1] for coord in all_coords)
        max_y = max(coord[1] for coord in all_coords)
        map_width = max_x - min_x
        map_height = max_y - min_y
        if map_width == 0:
            map_width = 1
        if map_height == 0:
            map_height = 1
        margin = 50
        usable_width = self.width - (2 * margin)
        usable_height = self.height - (2 * margin)
        scale_x = usable_width / map_width
        scale_y = usable_height / map_height
        for name in self.graph.hubs:
            real_x, real_y = self.graph.get_coordinates(name)
            screen_x = int((real_x - min_x) * scale_x) + margin
            screen_y = int((real_y - min_y) * scale_y) + margin
            self.node_positions[name] = (screen_x, screen_y)

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

    def draw_drons(self) -> None:
        color = (255, 255, 255)
        turn_text = self.font.render(
            f"Turn: {self.current_turn} / {self.max_turns} ( Use LEFT / RIGHT arrows)",
            True,
            color,
        )
        self.screen.blit(turn_text, (20, 20))
        for dron in self.drones:
            loc = dron.location(self.current_turn)
            if not loc:
                continue
            target = loc.split("-", 1)[1]
            if "-" not in target:
                x, y = self.node_positions[target]
            else:
                u, v = target.split("-")
                x1, y1 = self.node_positions[u]
                x2, y2 = self.node_positions[v]
                x, y = (x1 + x2) // 2, (y2 + y1) // 2
            pygame.draw.circle(self.screen,(color), (x, y), 10)
            dron_label = self.font.render(f"D{dron.id_dron}", True, color)
            self.screen.blit(dron_label, (x - 10, y + 12))

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.current_turn < self.max_turns:
                        self.current_turn += 1
                    elif event.key == pygame.K_LEFT and self.current_turn > 0:
                        self.current_turn -= 1
            self.draw_map()
            self.draw_drons()
            pygame.display.flip()
        pygame.quit()
