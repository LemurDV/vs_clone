from ui.base_menu import BaseMenu


class UpgradeMenu(BaseMenu):
    def __init__(self, game):
        super().__init__(game, "ВЫБЕРИТЕ УЛУЧШЕНИЕ")

    def select_option(self, index):
        if 0 <= index < len(self.options):
            upgrade = self.options[index]
            self.game.player.add_upgrade(upgrade)
            self.hide()
            self.game.on_upgrade_selected()
            return True
        return False
