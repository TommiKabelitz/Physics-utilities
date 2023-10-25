import unittest

from utilities import configIDs as cfg


class Test_ConfigIDs(unittest.TestCase):
    def test_init_str(self):
        ID_str = "-a-001880"
        id = cfg.ConfigID(13770, ID_str=ID_str)
        self.assertEqual(id.icon, 1)
        self.assertEqual(id.runID, "a")
        self.assertEqual(str(id), id.ID_str)
        self.assertEqual(id.ID_str, ID_str)

    def test_init_icon(self):
        icon = 1
        runID = "a"
        id = cfg.ConfigID(13770, icon=icon, runID=runID)
        self.assertEqual(id.icon, icon)
        self.assertEqual(id.runID, runID)
        self.assertEqual(str(id), id.ID_str)
        self.assertEqual(id.ID_str, "-a-001880")

    def test_mixed_init(self):
        icon = 1
        runID = "a"
        ID_str = "-a-001880"
        id = cfg.ConfigID(13770, ID_str=ID_str, icon=icon, runID=runID)
        self.assertEqual(id.icon, icon)
        self.assertEqual(id.runID, runID)
        self.assertEqual(str(id), id.ID_str)
        self.assertEqual(id.ID_str, ID_str)

    def test_mixed_init_fail(self):
        icon = 2
        runID = "a"
        ID_str = "-a-001880"
        self.assertRaises(
            ValueError, cfg.ConfigID, 13770, ID_str=ID_str, icon=icon, runID=runID
        )
    


if __name__ == "__main__":
    unittest.main()
