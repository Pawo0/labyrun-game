"""This module contains classes for different settings pages in the game."""

import pygame

from menu.menu_elements import Button, TextInput


class SettingsOptions:
    """Base class for settings pages in the game."""

    def __init__(self, main, title, options_names, options_values):
        """Initialize the settings page with options."""
        self.main = main
        self.screen = main.screen
        self.title = title
        self.options_names = options_names
        self.options_values = options_values
        self.current_values = [0] * len(options_names)  # Indexes of selected values

        # Text settings
        self.font = pygame.font.SysFont("arialblack", 40)
        self.text_color = (255, 255, 255)
        self.active_color = (255, 0, 0)
        self.background_color = (0, 0, 0)

        # Title position
        self.title_width, self.title_height = self.font.size(title)
        self.title_x = self.screen.get_width() // 2 - self.title_width // 2
        self.title_y = self.screen.get_height() // 6

        # Determine the size and position of elements
        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width()

        # Calculate the total required height
        total_options = len(options_names)

        # Adjust spacing between options based on the number of options
        if total_options <= 5:
            self.option_spacing = 80
        else:
            max_content_height = screen_height * 0.65
            self.option_spacing = min(80, max_content_height / (total_options + 1))

        # Start of the options section
        self.option_start_y = self.title_y + self.title_height + 50

        # Column positions
        column_margin = 150
        self.option_x = screen_width // 2 - column_margin
        self.value_x = screen_width // 2 + column_margin

        # Currently selected option
        self.selected = 0

        # Back button
        self.back_text = "Back"
        self.back_width, self.back_height = self.font.size(self.back_text)
        self.back_x = screen_width // 2

        # Set the position of the Back button below the last option
        self.back_y = self.option_start_y + (total_options * self.option_spacing) + 40

        # Make sure the Back button is not too low
        max_back_y = screen_height - 80
        if self.back_y > max_back_y:
            self.back_y = max_back_y

        self.back_button = Button(
            self.main, self.back_text, self.back_x, self.back_y, False
        )
        self.disabled_options = []  # List of indexes of disabled options
        self.disabled_color = (100, 100, 100)  # Gray color for disabled options
        self.dependencies = {}  # Dictionary of dependencies between options

    def set_option_dependency(self, dependent_option, parent_option, condition_func):
        """Set an option as dependent on another option."""
        if not hasattr(self, "dependencies"):
            self.dependencies = {}

        if parent_option not in self.dependencies:
            self.dependencies[parent_option] = []

        self.dependencies[parent_option].append((dependent_option, condition_func))

    def update_dependencies(self):
        """Update the state of dependent options based on parent settings."""
        self.disabled_options = []

        for parent, dependents in self.dependencies.items():
            for dependent_option, condition_func in dependents:
                if not condition_func(self.current_values, parent):
                    self.disabled_options.append(dependent_option)

    def handle_events(self, event):
        """Handle events for the settings page."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Skip inactive options
                self.selected = (self.selected - 1) % (len(self.options_names) + 1)
                while self.selected in self.disabled_options:
                    self.selected = (self.selected - 1) % (len(self.options_names) + 1)
            elif event.key == pygame.K_DOWN:
                # Skip inactive options
                self.selected = (self.selected + 1) % (len(self.options_names) + 1)
                while self.selected in self.disabled_options:
                    self.selected = (self.selected + 1) % (len(self.options_names) + 1)
            elif event.key == pygame.K_LEFT and self.selected < len(self.options_names):
                # Change option value left only for active options
                if self.selected not in self.disabled_options:
                    self.current_values[self.selected] = (
                        self.current_values[self.selected] - 1
                    ) % len(self.options_values[self.selected])
                    self._apply_setting(self.selected)
                    # Update dependencies after changing the option
                    self.update_dependencies()
            elif event.key == pygame.K_RIGHT and self.selected < len(
                self.options_names
            ):
                # Change option value right only for active options
                if self.selected not in self.disabled_options:
                    self.current_values[self.selected] = (
                        self.current_values[self.selected] + 1
                    ) % len(self.options_values[self.selected])
                    self._apply_setting(self.selected)
                    # Update dependencies after changing the option
                    self.update_dependencies()
            elif event.key == pygame.K_RETURN:
                # If "Back" is selected
                if self.selected == len(self.options_names):
                    self.main.game_state.open_settings()

        # Mouse event handling
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the Back button was clicked
            if self.back_button.is_clicked(event.pos):
                self.main.game_state.open_settings()
                return

            # Check if an option was clicked
            for i in range(len(self.options_names)):
                # Skip inactive options
                if i in self.disabled_options:
                    continue

                option_y = self.option_start_y + i * self.option_spacing

                # Option row area
                option_rect = pygame.Rect(
                    self.option_x - 100,
                    option_y - 20,
                    self.value_x - self.option_x + 200,
                    40,
                )

                if option_rect.collidepoint(event.pos):
                    self.selected = i
                    return

                # Left arrow area
                left_arrow = pygame.Rect(self.value_x - 70, option_y + 10, 40, 40)

                # Right arrow area
                right_arrow = pygame.Rect(self.value_x + 30, option_y + 10, 40, 40)

                if left_arrow.collidepoint(event.pos):
                    self.selected = i
                    self.current_values[i] = (self.current_values[i] - 1) % len(
                        self.options_values[i]
                    )
                    self._apply_setting(i)
                    self.update_dependencies()
                    return

                if right_arrow.collidepoint(event.pos):
                    self.selected = i
                    self.current_values[i] = (self.current_values[i] + 1) % len(
                        self.options_values[i]
                    )
                    self._apply_setting(i)
                    self.update_dependencies()
                    return

        elif event.type == pygame.MOUSEMOTION:
            # Highlight options under the cursor
            if self.back_button.is_hovered(event.pos):
                self.selected = len(self.options_names)
                return

            for i in range(len(self.options_names)):
                # Skip inactive options
                if i in self.disabled_options:
                    continue

                option_y = self.option_start_y + i * self.option_spacing
                option_rect = pygame.Rect(
                    self.option_x - 100,
                    option_y - 20,
                    self.value_x - self.option_x + 200,
                    40,
                )

                if option_rect.collidepoint(event.pos):
                    self.selected = i
                    return

    def draw(self):
        """Draw the settings page on the screen."""
        # Draw title
        title_render = self.font.render(self.title, True, self.text_color)
        self.screen.blit(title_render, (self.title_x, self.title_y))

        # Draw options and their values
        for i, option_name in enumerate(self.options_names):
            option_y = self.option_start_y + i * self.option_spacing

            # Determine the text color depending on the option state
            if i in self.disabled_options:
                option_color = self.disabled_color  # Gray color for disabled options
            else:
                option_color = (
                    self.active_color if i == self.selected else self.text_color
                )

            # Option name
            option_render = self.font.render(option_name, True, option_color)
            self.screen.blit(
                option_render, (self.option_x - option_render.get_width(), option_y)
            )

            # Option value
            current_value = self.options_values[i][self.current_values[i]]
            value_render = self.font.render(str(current_value), True, option_color)
            value_width = value_render.get_width()
            self.screen.blit(value_render, (self.value_x - value_width // 2, option_y))

            # Draw arrows only for active options
            if i == self.selected and i not in self.disabled_options:
                arrow_size = min(15, self.option_spacing // 3)

                # Left arrow
                pygame.draw.polygon(
                    self.screen,
                    option_color,
                    [
                        (self.value_x - 60, option_y + arrow_size * 2),
                        (self.value_x - 40, option_y + arrow_size),
                        (self.value_x - 40, option_y + arrow_size * 3),
                    ],
                )

                # Right arrow
                pygame.draw.polygon(
                    self.screen,
                    option_color,
                    [
                        (self.value_x + 60, option_y + arrow_size * 2),
                        (self.value_x + 40, option_y + arrow_size),
                        (self.value_x + 40, option_y + arrow_size * 3),
                    ],
                )

        # Draw the "Back" button
        if self.selected == len(self.options_names):
            self.back_button.active = True
        else:
            self.back_button.active = False
        self.back_button.draw()


class GameMenu(SettingsOptions):
    """Settings page for maze size."""

    def __init__(self, main):
        # Define options for maze size
        options_names = ["Width", "Height", "Fog of War"]
        options_values = [
            [7, 11, 15, 23, 31, 55],  # possible widths
            [7, 11, 15, 23, 31, 55],  # possible heights
            ["On", "Off"],  # Fog of war options
        ]

        # Find current values in options_values
        current_width = main.settings.maze_width
        current_height = main.settings.maze_height

        super().__init__(main, "Game Settings", options_names, options_values)

        # Set current indexes for values
        for i, value in enumerate(options_values[0]):
            if value == current_width:
                self.current_values[0] = i
                break
        for i, value in enumerate(options_values[1]):
            if value == current_height:
                self.current_values[1] = i
                break
        self.current_values[2] = 0 if main.settings.fog_of_war_enabled else 1

    def _apply_setting(self, index):
        """Apply the selected maze size setting."""
        width = self.options_values[0][self.current_values[0]]
        height = self.options_values[1][self.current_values[1]]
        self.main.settings.set_maze_size(width, height)
        self.main.settings.fog_of_war_enabled = self.current_values[2] == 0


class PowerupMenu(SettingsOptions):
    """Settings page for power-up options."""

    def __init__(self, main):
        options_names = [
            "Power-ups",
            "Speed Boost",
            "Slow Down",
            "Enlarge",
            "Teleport",
            "Freeze",
            "Reverse Controls",
        ]
        options_values = [
            ["On", "Off"],  # Power-ups (general)
            ["On", "Off"],  # Speed Boost
            ["On", "Off"],  # Slow Down
            ["On", "Off"],  # Enlarge
            ["On", "Off"],  # Teleport
            ["On", "Off"],  # Freeze
            ["On", "Off"],  # Reverse
        ]

        super().__init__(main, "Powerup Settings", options_names, options_values)

        # Set current values
        self.current_values[0] = 0 if main.settings.power_ups_enabled else 1
        self.current_values[1] = 0 if main.settings.speed_boost_enabled else 1
        self.current_values[2] = 0 if main.settings.slow_down_enabled else 1
        self.current_values[3] = 0 if main.settings.enlarge_enabled else 1
        self.current_values[4] = 0 if main.settings.teleport_enabled else 1
        self.current_values[5] = 0 if main.settings.freeze_enabled else 1
        self.current_values[6] = 0 if main.settings.reverse_controls_enabled else 1

        # Set dependencies - power-up options are active only when the main option is enabled (value=0)
        def powerups_enabled(values, parent_idx):
            return values[parent_idx] == 0  # "On"

        for powerup_idx in range(
            1, 7
        ):  # Indexes for Speed Boost, Slow Down, Enlarge, Teleport, Freeze, Reverse
            self.set_option_dependency(powerup_idx, 0, powerups_enabled)

        # Update dependencies at the start
        self.update_dependencies()

    def _apply_setting(self, index):
        """Apply the selected power-up setting to the game."""
        if index == 0:  # Power-ups (general)
            self.main.settings.power_ups_enabled = self.current_values[0] == 0
        elif index == 1:  # Speed Boost
            self.main.settings.speed_boost_enabled = self.current_values[1] == 0
        elif index == 2:  # Slow Down
            self.main.settings.slow_down_enabled = self.current_values[2] == 0
        elif index == 3:  # Enlarge
            self.main.settings.enlarge_enabled = self.current_values[3] == 0
        elif index == 4:  # Teleport
            self.main.settings.teleport_enabled = self.current_values[4] == 0
        elif index == 5:  # Freeze
            self.main.settings.freeze_enabled = self.current_values[5] == 0
        elif index == 6:  # Reverse Controls
            self.main.settings.reverse_controls_enabled = self.current_values[6] == 0


class EventMenu(SettingsOptions):
    """Settings page for configuring random events."""

    def __init__(self, main):
        options_names = [
            "Events Enabled",
            "Shortcut Reveal",
            "Teleportation",
            "Fatigue",
            "Invisible Walls",
            "Event Frequency",
        ]

        options_values = [
            ["On", "Off"],
            ["On", "Off"],
            ["On", "Off"],
            ["On", "Off"],
            ["On", "Off"],
            ["L", "N", "H"],
        ]

        super().__init__(main, "Event Settings", options_names, options_values)

        # Set current values
        self.current_values[0] = 0 if main.settings.events_enabled else 1
        self.current_values[1] = 0 if main.settings.shortcutreveal_enabled else 1
        self.current_values[2] = 0 if main.settings.teleportation_enabled else 1
        self.current_values[3] = 0 if main.settings.fatigue_enabled else 1
        self.current_values[4] = 0 if main.settings.invisiblewalls_enabled else 1

        # Set event frequency value
        if main.settings.event_max_interval >= 20000:
            self.current_values[5] = 0  # Low
        elif main.settings.event_max_interval >= 10000:
            self.current_values[5] = 1  # Normal
        else:
            self.current_values[5] = 2  # High

        # Set dependencies - event options are active only when the main option is enabled (value=0)
        def events_enabled(values, parent_idx):
            return values[parent_idx] == 0  # "On"

        for event_idx in range(1, 6):  # Indexes for event options
            self.set_option_dependency(event_idx, 0, events_enabled)

    def _apply_setting(self, index):
        """Apply the selected event settings."""
        if index == 0:  # Events master switch
            self.main.settings.events_enabled = self.current_values[0] == 0
        elif index == 1:  # Shortcut reveal
            self.main.settings.shortcutreveal_enabled = self.current_values[1] == 0
        elif index == 2:  # Teleportation
            self.main.settings.teleportation_enabled = self.current_values[2] == 0
        elif index == 3:  # Fatigue
            self.main.settings.fatigue_enabled = self.current_values[3] == 0
        elif index == 4:  # Invisible walls
            self.main.settings.invisiblewalls_enabled = self.current_values[4] == 0
        elif index == 5:  # Event frequency
            frequency = self.current_values[5]
            if frequency == 0:  # Low frequency
                self.main.settings.event_min_interval = 20000
                self.main.settings.event_max_interval = 40000
            elif frequency == 1:  # Normal frequency
                self.main.settings.event_min_interval = 10000
                self.main.settings.event_max_interval = 20000
            else:  # High frequency
                self.main.settings.event_min_interval = 5000
                self.main.settings.event_max_interval = 10000


class SetNames:
    """This class handles the player name input menu."""

    def __init__(self, main):
        """Initialize the name input menu."""
        self.main = main
        self.screen = main.screen
        self.font = pygame.font.SysFont("arialblack", 40)

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        center_x = screen_width // 2

        self.title_pos = (
            center_x - self.font.size("Set Player Names")[0] // 2,
            screen_height // 6,
        )

        vertical_center = screen_height // 2
        vertical_spacing = 120

        p1_y = vertical_center - vertical_spacing
        p2_y = vertical_center + 20

        label_x = center_x - 300
        input_x = center_x + 130

        self.p1_input = TextInput(main, "", input_x, p1_y, True)
        self.p2_input = TextInput(main, "", input_x, p2_y, False)
        self.play_button = Button(
            main, "Play!", center_x, p2_y + vertical_spacing, True
        )

        self.labels = [
            ("Set Player Names", self.title_pos),
            (
                "Player 1:",
                (
                    label_x - self.font.size("Player 1:")[0] // 2,
                    p1_y - self.font.size("Player 1:")[1] // 2,
                ),
            ),
            (
                "Player 2:",
                (
                    label_x - self.font.size("Player 2:")[0] // 2,
                    p2_y - self.font.size("Player 2:")[1] // 2,
                ),
            ),
        ]

        self.active_input = 1

    def handle_events(self, event):
        """Handle events for the name input screen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.is_clicked(event.pos):
                self._play()
            if self.p1_input.handle_event(event):
                self.active_input = 1
                self.p2_input.active = False
            elif self.p2_input.handle_event(event):
                self.active_input = 2
                self.p1_input.active = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.active_input = 1
                self.p1_input.active = True
                self.p2_input.active = False
            elif event.key == pygame.K_DOWN:
                self.active_input = 2
                self.p1_input.active = False
                self.p2_input.active = True
            elif event.key == pygame.K_TAB:
                self.active_input = 2 if self.active_input == 1 else 1
                self.p1_input.active = not self.p1_input.active
                self.p2_input.active = not self.p2_input.active
            elif event.key == pygame.K_RETURN:
                self._play()
            else:
                if self.active_input == 1:
                    self.p1_input.handle_event(event)
                elif self.active_input == 2:
                    self.p2_input.handle_event(event)

    def _play(self):
        """Start the game with the entered player names."""
        p1_name = self.p1_input.get_text() or "Player 1"
        p2_name = self.p2_input.get_text() or "Player 2"
        self.main.player1.set_name(p1_name)
        self.main.player2.set_name(p2_name)
        self.main.game_state.run_game()

    def draw(self):
        """Draw the name input menu screen."""

        for text, pos in self.labels:
            self.screen.blit(self.font.render(text, True, (255, 255, 255)), pos)

        self.p1_input.draw()
        self.p2_input.draw()
        self.play_button.draw()
