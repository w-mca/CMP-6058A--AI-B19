"""Defines the move history GUI in Hinger."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import pygame


class MoveHistoryGUI:

    BACKGROUND = (17, 24, 39)
    PANEL = (31, 41, 55)
    ACTIVE = (22, 107, 82)
    EMPTY = (55, 65, 81)
    TEXT = (249, 250, 251)

    def __init__(self, gui):
        self.gui = gui

        self.scroll = 0
        self.close_rect = pygame.Rect(0, 0, 0, 0)

        self.max_scroll = 0

    def draw(self):
        game = self.gui.game
        screen = self.gui.screen

        width, height = screen.get_size()
        size = min(width, height)

        screen.fill(self.BACKGROUND)

        title_font = pygame.font.SysFont(
            "Arial", max(18, int(size * 0.055)), bold=True
        )

        info_font = pygame.font.SysFont(
            "Arial", max(14, int(size * 0.028))
        )

        # Move history title
        title = title_font.render(
            "Move History", True, self.TEXT
        )

        screen.blit(
            title,
            title.get_rect(center=(width // 2, int(height * 0.10)))
        )

        # Close Move History button
        button_width = int(size * 0.30)
        button_height = int(size * 0.06)

        self.close_rect = pygame.Rect(
            0, 0, button_width, button_height
        )

        self.close_rect.center = (
            width // 2,
            int(height * 0.95)
        )

        pygame.draw.rect(
            screen,
            self.ACTIVE,
            self.close_rect,
            border_radius=10
        )

        close_text = info_font.render(
            "Close Move History", True, self.TEXT
        )

        screen.blit(
            close_text,
            close_text.get_rect(center=self.close_rect.center)
        )

        # Move list layout
        row_width = int(width * 0.75)
        row_height = int(size * 0.075)
        row_spacing = int(size * 0.025)

        number_width = int(size * 0.075)
        number_gap = int(size * 0.015)

        start_x = (width - row_width) // 2
        start_y = int(height * 0.20)
        bottom_y = int(height * 0.88)

        row_step = row_height + row_spacing

        # Calculate how far the list can scroll
        visible_height = bottom_y - start_y

        content_height = (
            len(game.move_history) * row_step - row_spacing
            if game.move_history else 0
        )

        self.max_scroll = max(
            0, content_height - visible_height
        )

        self.scroll = max(
            0, min(self.scroll, self.max_scroll)
        )

        # Keep the move list inside its display area
        old_clip = screen.get_clip()

        screen.set_clip(
            pygame.Rect(
                0,
                start_y,
                width,
                visible_height
            )
        )

        # Display each move
        for i, move in enumerate(game.move_history):

            y = start_y + i * row_step - self.scroll

            # Skip moves outside the visible area
            if y + row_height < start_y or y > bottom_y:
                continue

            # Number rectangle
            number_rect = pygame.Rect(
                start_x,
                y,
                number_width,
                row_height
            )

            pygame.draw.rect(
                screen,
                self.ACTIVE,
                number_rect,
                border_radius=10
            )

            number_text = info_font.render(
                str(i + 1), True, self.TEXT
            )

            screen.blit(
                number_text,
                number_text.get_rect(center=number_rect.center)
            )

            # Move rectangle
            move_rect = pygame.Rect(
                start_x + number_width + number_gap,
                y,
                row_width - number_width - number_gap,
                row_height
            )

            # Alternate the colour of each move
            colour = (
                self.PANEL if i % 2 == 0 else self.EMPTY
            )

            pygame.draw.rect(
                screen,
                colour,
                move_rect,
                border_radius=10
            )

            move_text = info_font.render(
                str(move), True, self.TEXT
            )

            screen.blit(
                move_text,
                move_text.get_rect(center=move_rect.center)
            )

        # Restore normal drawing area
        screen.set_clip(old_clip)

        # Display a message when no moves have been made
        if not game.move_history:

            empty_text = info_font.render(
                "No moves have been made yet.",
                True,
                self.TEXT
            )

            screen.blit(
                empty_text,
                empty_text.get_rect(
                    center=(width // 2, height // 2)
                )
            )

    def handle_event(self, event):

        # Scroll through the move history
        if event.type == pygame.MOUSEWHEEL:

            self.scroll -= event.y * 35

            self.scroll = max(
                0, min(self.scroll, self.max_scroll)
            )

        # Handle Close Move History button
        elif event.type == pygame.MOUSEBUTTONDOWN:
        
            if event.button == 1:
        
                if self.close_rect.collidepoint(event.pos):
        
                    self.gui.game.resume_timer()
                    self.gui.game_gui.show_move_history = False
                    self.scroll = 0
                    return
