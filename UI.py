"""Defines class for UI utilities in Hinger."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import pygame


class Button:
    """A reusable clickable Pygame button."""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        callback=None,
        colour=(22, 107, 82),
        hover_colour=(30, 140, 105),
        text_colour=(255, 255, 255)
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

        self.colour = colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour

        self.font = pygame.font.SysFont(
            "Segoe UI", 24, bold=True
        )

        self.enabled = True

    def draw(self, screen):
        """Draw the button."""

        hovered = self.rect.collidepoint(
            pygame.mouse.get_pos()
        )

        colour = (
            self.hover_colour
            if hovered and self.enabled
            else self.colour
        )

        pygame.draw.rect(
            screen,
            colour,
            self.rect,
            border_radius=10
        )

        label = self.font.render(
            self.text,
            True,
            self.text_colour
        )

        screen.blit(
            label,
            label.get_rect(center=self.rect.center)
        )

    def handle_event(self, event):
        """Execute callback when clicked."""

        if not self.enabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.callback is not None:
                        self.callback()

    def set_callback(self, callback):
        """Assign or replace the click callback."""
        self.callback = callback

    def set_position(self, x, y):
        """Move the button."""
        self.rect.topleft = (x, y)


class Selector:
    """A group of selectable buttons with one active option."""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        options,
        callback=None,
        gap=10
    ):
        self.options = list(options)
        self.callback = callback
        self.selected = None

        self.buttons = []
        self.gap = gap

        self.normal_colour = (55, 65, 81)
        self.selected_colour = (37, 99, 235)

        for index, option in enumerate(self.options):

            button = Button(
                x=x,
                y=y + index * (height + gap),
                width=width,
                height=height,
                text=option,
                callback=lambda i=index: self.select(i),
                colour=self.normal_colour
            )

            self.buttons.append(button)

    def select(self, index):
        """Select one option and deselect the others."""

        if not 0 <= index < len(self.options):
            raise IndexError("Invalid selector index")

        self.selected = index

        if self.callback is not None:
            self.callback(self.options[index])

    def get_selected(self):
        """Return the selected option or None."""
        if self.selected is None:
            return None

        return self.options[self.selected]

    def set_position(self, x, y):
        """Reposition the entire selector."""

        for index, button in enumerate(self.buttons):
            button.set_position(
                x,
                y + index * (button.rect.height + self.gap)
            )

    def draw(self, screen):
        """Draw every option with its selection state."""

        for index, button in enumerate(self.buttons):

            if index == self.selected:
                button.colour = self.selected_colour
                button.hover_colour = self.selected_colour
            else:
                button.colour = self.normal_colour
                button.hover_colour = (75, 85, 101)

            button.draw(screen)

    def handle_event(self, event):
        """Forward mouse events to all option buttons."""

        for button in self.buttons:
            button.handle_event(event)
