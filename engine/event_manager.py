"""
Event system for LabyRun game.
Manages random events that affect both players during gameplay.
"""

import random

import pygame

from maze.maze import Floor


class GameEvent:
    """Base class for game events."""

    def __init__(self, name, duration=5000):
        self.name = name
        self.duration = duration
        self.active = False
        self.start_time = 0

    def activate(self, main):
        """Activate the event."""
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self._apply_effect(main)

    def _apply_effect(self, main):
        """Apply the event effect. Override in subclasses."""
        raise NotImplementedError("This method should be overridden by subclasses.")

    def update(self, main):
        """Update the event state and check if it should be deactivated."""
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.deactivate(main)
                return True
        return False

    def deactivate(self, main):
        """Deactivate the event and restore original state."""
        self.active = False
        self._restore_effect(main)

    def _restore_effect(self, main):
        """Restore original state after event ends. Override in subclasses."""
        raise NotImplementedError("This method should be overridden by subclasses.")


class ShortcutRevealEvent(GameEvent):
    """Event that reveals shortcuts by temporarily removing walls next to players."""

    def __init__(self):
        super().__init__("Shortcut Reveal", 5000)
        self.revealed_walls = []
        self.original_wall_positions = []

    def _apply_effect(self, main):
        """Remove walls next to both players."""
        self.revealed_walls = []
        self.original_wall_positions = []

        players = [main.player1, main.player2]

        for player in players:
            player_grid_x = (
                player.rect.centerx - main.maze.offset_x
            ) // main.settings.block_size
            player_grid_y = (
                player.rect.centery - main.maze.offset_y
            ) // main.settings.block_size

            adjacent_positions = [
                (player_grid_x, player_grid_y),
                (player_grid_x, player_grid_y - 1),
                (player_grid_x, player_grid_y + 1),
                (player_grid_x - 1, player_grid_y),
                (player_grid_x + 1, player_grid_y),
            ]

            for grid_x, grid_y in adjacent_positions:
                if (
                    0 < grid_x < len(main.maze.maze[0]) - 1
                    and 0 < grid_y < len(main.maze.maze) - 1
                    and main.maze.maze[grid_y][grid_x] == 1
                ):

                    pixel_x = main.maze.offset_x + grid_x * main.settings.block_size
                    pixel_y = main.maze.offset_y + grid_y * main.settings.block_size

                    for wall in main.maze.walls:
                        if wall.rect.x == pixel_x and wall.rect.y == pixel_y:
                            main.maze.walls.remove(wall)
                            self.revealed_walls.append(wall)

                            main.maze.maze[grid_y][grid_x] = 0

                            floor = Floor(
                                (200, 200, 200),
                                pixel_x,
                                pixel_y,
                                main.settings.block_size,
                            )
                            main.maze.floors.add(floor)

                            self.original_wall_positions.append(
                                (grid_x, grid_y, wall, floor)
                            )
                            break

    def _restore_effect(self, main):
        """Restore the removed walls."""
        for grid_x, grid_y, wall, floor in self.original_wall_positions:
            main.maze.floors.remove(floor)

            main.maze.walls.add(wall)

            main.maze.maze[grid_y][grid_x] = 1

        self.revealed_walls.clear()
        self.original_wall_positions.clear()


class TeleportationEvent(GameEvent):
    """Event that teleports both players to random mirrored locations."""

    def __init__(self):
        super().__init__("Teleportation", 0)

    def _apply_effect(self, main):
        """Teleport both players to mirrored random locations."""
        available_floors = []
        block_offset_p1 = (main.settings.block_size - main.player1.width) // 2
        block_offset_p2 = (main.settings.block_size - main.player2.width) // 2

        mid_x = main.settings.screen_width // 2
        safe_margin = main.settings.block_size * 3

        left_zone, right_zone = main.engine.win_zone

        for floor in main.maze.floors:
            floor_center_x = floor.rect.centerx

            is_in_win_zone = left_zone <= floor_center_x <= right_zone

            if not is_in_win_zone and floor.rect.centerx < mid_x - safe_margin:
                available_floors.append(floor)

        if available_floors:
            new_floor1 = random.choice(available_floors)

            p1_x = new_floor1.rect.x
            p1_y = new_floor1.rect.y
            p2_x = main.settings.screen_width - p1_x - main.settings.block_size
            p2_y = p1_y

            p1_x += block_offset_p1
            p1_y += block_offset_p1
            p2_x += block_offset_p2
            p2_y += block_offset_p2

            main.player1.x = p1_x
            main.player1.y = p1_y
            main.player1.rect.x = main.player1.x
            main.player1.rect.y = main.player1.y

            main.player2.x = p2_x
            main.player2.y = p2_y
            main.player2.rect.x = main.player2.x
            main.player2.rect.y = main.player2.y

    def update(self, main):
        """Teleportation is instant, so deactivate immediately."""
        if self.active:
            self.deactivate(main)
            return True
        return False

    def _restore_effect(self, main):
        """Nothing to restore, teleportation is instant."""


class FatigueEvent(GameEvent):
    """Event that reduces both players' speed for a duration."""

    def __init__(self):
        super().__init__("Fatigue", 5000)
        self.original_speeds = {}

    def _apply_effect(self, main):
        """Reduce both players' speed."""
        self.original_speeds[1] = main.player1.speed
        self.original_speeds[2] = main.player2.speed

        main.player1.speed = int(main.player1.speed * 0.5)
        main.player2.speed = int(main.player2.speed * 0.5)

    def _restore_effect(self, main):
        """Restore original speeds."""
        if 1 in self.original_speeds:
            main.player1.speed = self.original_speeds[1]
        if 2 in self.original_speeds:
            main.player2.speed = self.original_speeds[2]
        self.original_speeds.clear()


class EventManager:
    """Manages random events during gameplay."""

    def __init__(self, main):
        self.main = main
        self.events = [ShortcutRevealEvent, TeleportationEvent, FatigueEvent]
        self.active_events = []
        self.last_event_time = 0
        self.next_event_time = 0
        self._schedule_next_event()

    def _schedule_next_event(self):
        """Schedule the next random event based on settings."""
        if not self._events_enabled():
            return

        min_interval = getattr(self.main.settings, "event_min_interval", 10000)
        max_interval = getattr(self.main.settings, "event_max_interval", 20000)

        # Add some progression - events become more frequent over time
        game_time = pygame.time.get_ticks()
        progression_factor = min(1.0, game_time / 60000)

        min_interval = int(min_interval * (1 - progression_factor * 0.3))
        max_interval = int(max_interval * (1 - progression_factor * 0.3))

        interval = random.randint(min_interval, max_interval)
        self.next_event_time = pygame.time.get_ticks() + interval

    def _events_enabled(self):
        """Check if events are enabled in settings."""
        return getattr(self.main.settings, "events_enabled", True)

    def _get_enabled_events(self):
        """Get list of events that are enabled in settings."""
        enabled_events = []

        for event_class in self.events:
            event_name = event_class.__name__.replace("Event", "").lower()
            setting_name = f"{event_name}_enabled"

            if getattr(self.main.settings, setting_name, True):
                enabled_events.append(event_class)

        return enabled_events

    def update(self):
        """Update event system - check for new events and update active ones."""
        if not self._events_enabled():
            return

        current_time = pygame.time.get_ticks()

        if (
            current_time >= self.next_event_time
            and self.main.game_state.get_current_state() == "running"
        ):
            self._trigger_random_event()
            self._schedule_next_event()

        for event in self.active_events[:]:
            if event.update(self.main):
                self.active_events.remove(event)

    def _trigger_random_event(self):
        """Trigger a random event from enabled events."""
        enabled_events = self._get_enabled_events()

        if not enabled_events:
            return

        if self.active_events:
            return

        event_class = random.choice(enabled_events)
        event = event_class()
        event.activate(self.main)
        self.active_events.append(event)

        print(f"Event triggered: {event.name}")

    def get_active_events(self):
        """Get list of currently active events."""
        return [event.name for event in self.active_events]

    def draw_active_events(self, screen):
        """Draw active events on screen as visual indicators."""
        if not self.active_events:
            return

        font = pygame.font.SysFont("arial", 24)
        y_offset = 10

        for event in self.active_events:
            # Choose color based on event type
            if "Shortcut" in event.name:
                color = (0, 255, 255)  # Cyan
            elif "Teleportation" in event.name:
                color = (148, 0, 211)  # Purple
            elif "Fatigue" in event.name:
                color = (255, 165, 0)  # Orange
            else:
                color = (255, 255, 255)  # White

            text = f"ACTIVE: {event.name}"
            if event.duration > 0:  # Show remaining time for timed events
                remaining = max(
                    0, event.duration - (pygame.time.get_ticks() - event.start_time)
                )
                text += f" ({remaining // 1000}s)"

            text_surface = font.render(text, True, color)
            screen.blit(text_surface, (10, y_offset))
            y_offset += 30
