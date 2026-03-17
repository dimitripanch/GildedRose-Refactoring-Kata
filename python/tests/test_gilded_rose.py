# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):

    def update_once(self, name, sell_in, quality):
        item = Item(name, sell_in, quality)
        GildedRose([item]).update_quality()
        return item

    def test_conjured_degrades_by_2_before_sell_date(self):
        item = self.update_once("Conjured Mana Cake", 3, 6)
        self.assertEqual(4, item.quality)
        self.assertEqual(2, item.sell_in)

    def test_conjured_degrades_by_4_after_sell_date(self):
        item = self.update_once("Conjured Mana Cake", -1, 6)
        self.assertEqual(2, item.quality)
        self.assertEqual(-2, item.sell_in)

    def test_backstage_drops_to_zero_after_concert(self):
        item = self.update_once("Backstage passes to a TAFKAL80ETC concert", 0, 30)
        self.assertEqual(0, item.quality)
        self.assertEqual(-1, item.sell_in)

    def test_aged_brie_increases_and_caps_at_50(self):
        item = self.update_once("Aged Brie", 5, 49)
        self.assertEqual(50, item.quality)
        self.assertEqual(4, item.sell_in)
    
    def test_sulfuras_never_changes(self):
        item = self.update_once("Sulfuras, Hand of Ragnaros", 0, 80)
        self.assertEqual(80, item.quality)
        self.assertEqual(0, item.sell_in)

    def test_normal_item_degrades_by_2_after_sell_date(self):
        item = self.update_once("Elixir of the Mongoose", 0, 7)
        self.assertEqual(5, item.quality)
        self.assertEqual(-1, item.sell_in)
    
    def test_backstage_increases_by_2_when_sell_in_is_10(self):
        item = self.update_once("Backstage passes to a TAFKAL80ETC concert", 10, 20)
        self.assertEqual(22, item.quality)
        self.assertEqual(9, item.sell_in)

    def test_aged_brie_increases_by_2_after_sell_date(self):
        item = self.update_once("Aged Brie", 0, 10)
        self.assertEqual(12, item.quality)
        self.assertEqual(-1, item.sell_in)
        
if __name__ == '__main__':
    unittest.main()
