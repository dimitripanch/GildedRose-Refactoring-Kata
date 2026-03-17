# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

# Refactor approach:
# - Strategy pattern: each item type has its own updater class.
# - Factory selects the correct updater based on item name.
# This reduces nested conditionals and makes new item rules easier to add.

class ItemUpdater:
    def increase_quality(self, item, amount=1):
        item.quality = min(50, item.quality + amount)

    def decrease_quality(self, item, amount=1):
        item.quality = max(0, item.quality - amount)

    def decrease_sell_in(self, item):
        item.sell_in -= 1

    def update(self, item):
        raise NotImplementedError


class NormalUpdater(ItemUpdater):
    def update(self, item):
        degrade = 1 if item.sell_in > 0 else 2
        self.decrease_quality(item, degrade)
        self.decrease_sell_in(item)


class ConjuredUpdater(ItemUpdater):
    def update(self, item):
        degrade = 2 if item.sell_in > 0 else 4
        self.decrease_quality(item, degrade)
        self.decrease_sell_in(item)


class AgedBrieUpdater(ItemUpdater):
    def update(self, item):
        increase = 1 if item.sell_in > 0 else 2
        self.increase_quality(item, increase)
        self.decrease_sell_in(item)


class BackstageUpdater(ItemUpdater):
    def update(self, item):
        if item.sell_in <= 0:
            item.quality = 0
        elif item.sell_in <= 5:
            self.increase_quality(item, 3)
        elif item.sell_in <= 10:
            self.increase_quality(item, 2)
        else:
            self.increase_quality(item, 1)

        self.decrease_sell_in(item)


class SulfurasUpdater(ItemUpdater):
    def update(self, item):
        # Legendary item never changes.
        return


class UpdaterFactory:
    AGED_BRIE = "Aged Brie"
    BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"

    def get_updater(self, item):
        if item.name == self.AGED_BRIE:
            return AgedBrieUpdater()
        if item.name == self.BACKSTAGE:
            return BackstageUpdater()
        if item.name == self.SULFURAS:
            return SulfurasUpdater()
        if item.name.startswith("Conjured"):
            return ConjuredUpdater()
        return NormalUpdater()


class GildedRose(object):
    def __init__(self, items):
        self.items = items
        self.factory = UpdaterFactory()

    def update_quality(self):
        for item in self.items:
            updater = self.factory.get_updater(item)
            updater.update(item)