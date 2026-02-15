from ui.base_menu import BaseMenu


class ElementMenu(BaseMenu):
    def __init__(self, game):
        super().__init__(game, "ВЫБЕРИТЕ ЭЛЕМЕНТ")

    def select_option(self, index):
        if 0 <= index < len(self.options):
            element = self.options[index]
            self.game.player.add_element(element)
            self.hide()
            self.game.on_upgrade_selected()
            return True
        return False
