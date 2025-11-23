import pygame
import sys
import math

WIDTH = 1100
HEIGHT = 650
FPS = 60

FIXED_ARRAY = [35, 12, 88, 7, 54, 29, 100, 61, 43, 77, 15, 90, 3, 50]
N = len(FIXED_ARRAY)
BAR_WIDTH = WIDTH // N

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shell Sort Visualizer — Multi-Gap Edition")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 24)
font_small = pygame.font.SysFont("consolas", 18)

BASELINE = HEIGHT - 150   # ← столбцы подняты выше


# ───────────────────────────────────────────────────────────────
#                     GAPS SEQUENCES
# ───────────────────────────────────────────────────────────────

def shell_gaps(n):
    gaps = []
    h = n // 2
    while h > 0:
        gaps.append(h)
        h //= 2
    return gaps


def hibbard_gaps(n):
    gaps = []
    k = 1
    while (h := 2 ** k - 1) < n:
        gaps.append(h)
        k += 1
    gaps.reverse()
    return gaps


def knuth_gaps(n):
    gaps = []
    h = 1
    while h < n:
        gaps.append(h)
        h = h * 3 + 1
    gaps.reverse()
    return gaps


def sedgewick_gaps(n):
    gaps = []
    k = 0
    while True:
        if k % 2 == 0:
            h = 9 * (2 ** k - 2 ** (k//2)) + 1
        else:
            h = 8 * (2 ** k - 2 ** ((k+1)//2)) + 1
        if h >= n or h <= 0:
            break
        gaps.append(h)
        k += 1
    gaps.sort(reverse=True)
    return gaps


def pratt_gaps(n):
    gaps = set()
    i = 0
    while 2 ** i < n:
        j = 0
        while 2 ** i * 3 ** j < n:
            gaps.add(2 ** i * 3 ** j)
            j += 1
        i += 1
    gaps = sorted([g for g in gaps if g > 0], reverse=True)
    return gaps


GAP_MODES = {
    "Shell": shell_gaps,
    "Hibbard": hibbard_gaps,
    "Pratt": pratt_gaps,
    "Knuth": knuth_gaps,
    "Sedgewick": sedgewick_gaps,
}

MODE_KEYS = ["Shell", "Hibbard", "Pratt", "Knuth", "Sedgewick"]


# ───────────────────────────────────────────────────────────────
#                    VISUALIZER CLASS
# ───────────────────────────────────────────────────────────────

class ShellVisualizer:
    def __init__(self, mode_name="Hibbard"):
        self.mode_name = mode_name
        self.arr = FIXED_ARRAY.copy()
        self.gaps = GAP_MODES[self.mode_name](len(self.arr))

        self.gi = 0
        self.gap = self.gaps[self.gi]

        self.i = self.gap
        self.j = None
        self.x = None

        self.phase = "gap_start"
        self.running = False

    def set_mode(self, name):
        self.mode_name = name
        self.reset()

    def reset(self):
        self.arr = FIXED_ARRAY.copy()
        self.gaps = GAP_MODES[self.mode_name](len(self.arr))

        self.gi = 0
        self.gap = self.gaps[self.gi]

        self.i = self.gap
        self.j = None
        self.x = None
        self.phase = "gap_start"
        self.running = False

    # ───────────────────────────────────────────────
    # ONE STEP OF STATE MACHINE
    # ───────────────────────────────────────────────
    def step(self):
        if self.phase == "done":
            return

        if self.phase == "gap_start":
            self.i = self.gap
            self.phase = "i_loop"
            return

        if self.phase == "i_loop":
            if self.i >= len(self.arr):
                self.gi += 1
                if self.gi >= len(self.gaps):
                    self.phase = "done"
                    return
                self.gap = self.gaps[self.gi]
                self.phase = "gap_start"
                return

            self.x = self.arr[self.i]
            self.j = self.i
            self.phase = "j_shift"
            return

        if self.phase == "j_shift":
            if self.j >= self.gap and self.arr[self.j - self.gap] > self.x:
                self.arr[self.j] = self.arr[self.j - self.gap]
                self.j -= self.gap
                return
            else:
                self.phase = "write_value"
                return

        if self.phase == "write_value":
            self.arr[self.j] = self.x
            self.phase = "i_next"
            return

        if self.phase == "i_next":
            self.i += 1
            self.phase = "i_loop"
            return


    # ───────────────────────────────────────────────
    # DRAWING
    # ───────────────────────────────────────────────

    def draw_gradient(self):
        for y in range(HEIGHT):
            color = (
                225 - y // 30,
                235 - y // 45,
                245 - y // 60,
            )
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    def shadow_rect(self, x, y, w, h):
        shadow = pygame.Surface((w, h), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 45))
        screen.blit(shadow, (x + 4, y + 4))

    def draw(self):
        self.draw_gradient()

        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, 80))
        pygame.draw.line(screen, (160, 160, 160), (0, 80), (WIDTH, 80))

        title = font.render(
            f"{self.mode_name} gaps   GAP: {self.gap if self.phase!='done' else '-'}",
            True, (40, 40, 40)
        )
        screen.blit(title, (20, 10))

        subtitle = font_small.render(
            f"phase = {self.phase}     i = {self.i if self.phase!='done' else '-'}   j = {self.j if self.j is not None else '-'}",
            True, (60, 60, 60)
        )
        screen.blit(subtitle, (20, 45))

        # bars
        for idx, val in enumerate(self.arr):
            x = idx * BAR_WIDTH
            y = BASELINE - val   # ← подняли столбцы

            color = (160, 160, 160)

            if self.phase in ("j_shift", "write_value"):
                if idx == self.i:
                    color = (255, 100, 100)
                if idx == self.j:
                    color = (120, 150, 255)
                if self.j is not None and idx == self.j - self.gap:
                    color = (255, 190, 60)

            self.shadow_rect(x, y, BAR_WIDTH - 2, val)
            pygame.draw.rect(screen, color, (x, y, BAR_WIDTH - 2, val), border_radius=5)

            label = font_small.render(str(val), True, (30, 30, 30))
            screen.blit(label, (x + BAR_WIDTH // 2 - label.get_width() // 2, y - 20))

        # controls
        controls = font_small.render(
            "1..5 → change sequence   |   SPACE play/pause   |   → step   |   R reset   |   Q quit",
            True, (40, 40, 40)
        )
        screen.blit(controls, (20, HEIGHT - 35))

        pygame.display.flip()


# ───────────────────────────────────────────────────────────────
# MAIN LOOP
# ───────────────────────────────────────────────────────────────

def main():
    visual = ShellVisualizer("Hibbard")

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()

                # переключение режимов
                if event.key == pygame.K_1:
                    visual.set_mode("Shell")
                if event.key == pygame.K_2:
                    visual.set_mode("Hibbard")
                if event.key == pygame.K_3:
                    visual.set_mode("Pratt")
                if event.key == pygame.K_4:
                    visual.set_mode("Knuth")
                if event.key == pygame.K_5:
                    visual.set_mode("Sedgewick")

                if event.key == pygame.K_SPACE:
                    visual.running = not visual.running

                if event.key == pygame.K_RIGHT:
                    visual.step()

                if event.key == pygame.K_r:
                    visual.reset()

        if visual.running and visual.phase != "done":
            visual.step()

        visual.draw()


if __name__ == "__main__":
    main()
