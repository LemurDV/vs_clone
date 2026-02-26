from elements.base_element import BaseElement


class ToxicElement(BaseElement):
    def __init__(self):
        super().__init__(
            name="toxic",
            name_ui="Яд",
            description="Отравляет врагов",
            image_path="assets/elements/toxic.png",
        )

    def apply(self, player):
        pass
