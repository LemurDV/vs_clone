from elements.base_element import BaseElement


class WindElement(BaseElement):
    def __init__(self):
        super().__init__(
            name="wind",
            name_ui="Ветер",
            description="Увеличивает шанс крита",
            image_path="assets/elements/wind.png",
        )

    def apply(self, player):
        pass
