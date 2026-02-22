from elements.base_element import BaseElement


class FireElement(BaseElement):
    def __init__(self):
        super().__init__(
            name="Огонь",
            description="Поджигает врагов",
            image_path="assets/elements/fire.png",
        )

    def apply(self, player):
        pass
