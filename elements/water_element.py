from elements.base_element import BaseElement


class WaterElement(BaseElement):
    def __init__(self):
        super().__init__(
            name="water",
            name_ui="Вода",
            description="Пока хз)",
            image_path="assets/elements/water.png",
        )

    def apply(self, player):
        pass
