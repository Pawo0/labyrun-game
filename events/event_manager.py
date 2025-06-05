"""Manages random events that affect both players during gameplay."""

import random

import pygame

from .events import (FatigueEvent, InvisibleWallsEvent, ShortcutRevealEvent,
                     TeleportationEvent)


class EventManager:
    """Manages random events during gameplay."""

    def __init__(self, main):
        self.main = main
        self.events = [
            ShortcutRevealEvent,
            TeleportationEvent,
            FatigueEvent,
            InvisibleWallsEvent,
        ]
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
