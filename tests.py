import unittest
import app


class TestHelpers(unittest.TestCase):

    def test_prevday(self):
        self.assertEqual(app.prevDay('mo'), 'su')
        self.assertEqual(app.prevDay('su'), 'sa')
        self.assertEqual(app.prevDay('sa'), 'fr')
        self.assertEqual(app.prevDay('fr'), 'th')
        self.assertEqual(app.prevDay('th'), 'we')
        self.assertEqual(app.prevDay('we'), 'tu')
        self.assertEqual(app.prevDay('tu'), 'mo')

    def test_nextday(self):
        self.assertEqual(app.nextDay('mo'), 'tu')
        self.assertEqual(app.nextDay('tu'), 'we')
        self.assertEqual(app.nextDay('we'), 'th')
        self.assertEqual(app.nextDay('th'), 'fr')
        self.assertEqual(app.nextDay('fr'), 'sa')
        self.assertEqual(app.nextDay('sa'), 'su')
        self.assertEqual(app.nextDay('su'), 'mo')


if __name__ == '__main__':
    unittest.main()

