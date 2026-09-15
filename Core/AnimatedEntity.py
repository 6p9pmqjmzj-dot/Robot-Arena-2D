"""Entity variant with lightweight shape-frame animation."""
from __future__ import annotations
from Core.Entity import Entity


class AnimatedEntity(Entity):
    """Cycles registered turtle shapes when frames are supplied."""
    def __init__(self, *args: object, frames: list[str] | None = None,
                 animation_speed: float = 0.1, loop: bool = True, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self.frames, self.current_frame = frames or [], 0
        self.animation_speed, self.animation_timer, self.loop = animation_speed, 0.0, loop

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.frames:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0.0
                self.current_frame = min(self.current_frame + 1, len(self.frames) - 1)
                if self.loop: self.current_frame %= len(self.frames)
                self.turtle.shape(self.frames[self.current_frame])
