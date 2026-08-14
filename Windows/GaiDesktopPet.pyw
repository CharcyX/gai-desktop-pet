import math
import os
import time
import tkinter as tk

CELL_W, CELL_H = 192, 208
COLS, ROWS = 8, 11
GAZE_MARGIN = 60
KEY = "#D12AFF"


class GaiPet:
    def __init__(self, root, atlas_path):
        self.root = root
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.configure(bg=KEY)
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=CELL_W, height=CELL_H, bg=KEY,
                                highlightthickness=0, bd=0)
        self.canvas.pack()
        self.atlas = tk.PhotoImage(file=atlas_path)
        self.image = self.canvas.create_image(0, 0, anchor="nw")
        self.state = "idle"
        self.frame = 0
        self.action_frames_played = 0
        self.idle_loops_completed = 0
        self.idle_sequence_index = 0
        self.action_loops_completed = 0
        self.started = time.monotonic()
        self.hover_active = False
        self.hover_count = 0
        self.dragging = False
        self.drag_started = 0
        self.drag_seconds = 0.0
        self.anger_after_action = False
        self.drag_start = None
        self.last_drag_point = None
        self.window_start = None
        self.canvas.bind("<Button-1>", self.begin_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<Button-3>", lambda event: root.destroy())
        root.bind("<Escape>", lambda event: root.destroy())
        self.place_bottom_right()
        self.enter_idle()
        self.tick()

    def place_bottom_right(self):
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{CELL_W}x{CELL_H}+{sw-CELL_W-24}+{sh-CELL_H-48}")

    def enter_idle(self):
        self.state, self.frame = "idle", 0
        self.started = time.monotonic()
        self.idle_loops_completed = 0
        self.idle_sequence_index = 0
        self.action_loops_completed = 0
        self.draw()

    def start(self, state):
        self.state, self.frame = state, 0
        self.action_frames_played = 0
        self.action_loops_completed = 0
        self.started = time.monotonic()
        self.draw()

    def is_idle_sequence_state(self):
        return self.state in ("singing", "review", "waiting", "failed")

    def start_next_idle_action(self):
        sequence = ("singing", "waiting", "failed")
        if self.idle_sequence_index >= len(sequence):
            self.enter_idle()
            return
        state = sequence[self.idle_sequence_index]
        self.idle_sequence_index += 1
        self.start(state)

    def frame_count(self):
        return {"idle": 6, "rap": 5, "singing": 6, "waiting": 6,
                "failed": 8, "review": 6, "gaze": 1,
                "running-right": 8, "running-left": 8, "angry": 6}[self.state]

    def atlas_index(self):
        if self.state == "idle": return self.frame
        if self.state == "running-right": return 8 + self.frame
        if self.state == "running-left": return 16 + self.frame
        if self.state == "rap": return 32 + self.frame
        if self.state == "failed": return 40 + self.frame
        if self.state in ("singing", "waiting"): return 48 + self.frame
        if self.state == "angry": return 56 + self.frame
        if self.state == "review": return 64 + self.frame
        if self.state == "gaze": return (72 + self.frame) if self.frame < 8 else (80 + self.frame - 8)
        return 0

    def draw(self):
        idx = self.atlas_index()
        col, row = idx % COLS, idx // COLS
        self.frame_image = tk.PhotoImage()
        self.frame_image.tk.call(self.frame_image, "copy", self.atlas, "-from",
                                 col * CELL_W, row * CELL_H,
                                 (col + 1) * CELL_W, (row + 1) * CELL_H)
        self.canvas.itemconfigure(self.image, image=self.frame_image)

    def mouse_info(self):
        px, py = self.root.winfo_pointerx(), self.root.winfo_pointery()
        x, y = self.root.winfo_rootx(), self.root.winfo_rooty()
        inside = x <= px < x + CELL_W and y <= py < y + CELL_H
        cx, cy = x + CELL_W / 2, y + CELL_H / 2
        return px, py, cx, cy, inside, math.hypot(px - cx, py - cy)

    def gaze_direction(self, px, py, cx, cy):
        deg = math.degrees(math.atan2(px - cx, cy - py)) % 360
        return int(round(deg / 22.5)) % 16

    def finish_action(self):
        if self.anger_after_action:
            self.anger_after_action = False
            self.start("angry")
        else:
            self.enter_idle()

    def tick(self):
        now = time.monotonic()
        px, py, cx, cy, inside, distance = self.mouse_info()
        if inside and not self.dragging:
            if not self.hover_active:
                self.hover_active = True
                self.hover_count += 1
                if self.hover_count >= 3:
                    self.hover_count = 0
                    self.anger_after_action = True
            if self.state != "rap":
                self.start("rap")
        elif not inside and 0 < distance <= GAZE_MARGIN and not self.dragging:
            direction = self.gaze_direction(px, py, cx, cy)
            if self.state != "gaze" or self.frame != direction:
                self.state, self.frame, self.started = "gaze", direction, now
                self.draw()
        elif not inside:
            self.hover_active = False
            if self.state == "rap":
                self.finish_action()
            if self.state == "gaze" and not self.dragging:
                self.enter_idle()

        if self.state == "idle":
            if now - self.started >= 0.18:
                self.frame += 1
                if self.frame >= self.frame_count():
                    self.frame = 0
                    self.idle_loops_completed += 1
                self.started = now
                if self.idle_loops_completed >= 6 and distance > GAZE_MARGIN:
                    self.start_next_idle_action()
                else:
                    self.draw()
        elif self.state == "rap" and now - self.started >= 0.14:
            if inside and not self.dragging:
                self.frame = (self.frame + 1) % self.frame_count()
                self.started = now
                self.draw()
        elif self.state != "gaze" and now - self.started >= 0.14:
            self.frame += 1
            self.action_frames_played += 1
            self.started = now
            if self.frame >= self.frame_count():
                self.action_loops_completed += 1
            self.frame %= self.frame_count()
            if self.is_idle_sequence_state() and self.action_loops_completed >= 3:
                if self.anger_after_action:
                    self.anger_after_action = False
                    self.start("angry")
                else:
                    self.start_next_idle_action()
            else:
                self.draw()
        self.root.after(66, self.tick)

    def begin_drag(self, event):
        self.dragging = True
        self.drag_started = time.monotonic()
        self.drag_start = (event.x_root, event.y_root)
        self.last_drag_point = self.drag_start
        self.window_start = (self.root.winfo_x(), self.root.winfo_y())

    def drag(self, event):
        dx = event.x_root - self.drag_start[0]
        dy = event.y_root - self.drag_start[1]
        step_dx = event.x_root - self.last_drag_point[0]
        self.root.geometry(f"+{self.window_start[0]+dx}+{self.window_start[1]+dy}")
        if abs(step_dx) >= 1:
            state = "running-right" if step_dx > 0 else "running-left"
            if self.state != state:
                self.start(state)
        self.last_drag_point = (event.x_root, event.y_root)

    def end_drag(self, event):
        if not self.dragging:
            return
        self.dragging = False
        self.drag_seconds += time.monotonic() - self.drag_started
        if self.state in ("running-right", "running-left"):
            if self.drag_seconds > 7:
                self.drag_seconds = 0
                self.anger_after_action = True
            self.finish_action()


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    atlas = os.path.join(root_dir, "spritesheet.png")
    if not os.path.exists(atlas):
        raise SystemExit("spritesheet.png is missing")
    root = tk.Tk()
    GaiPet(root, atlas)
    root.mainloop()


if __name__ == "__main__":
    main()
