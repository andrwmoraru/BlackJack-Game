import unittest
from BlackJackGame import BlackjackGame

class TestBlackjackGame(unittest.TestCase):
    
    def setUp(self):
        """Configurează un joc pentru teste."""
        self.game = BlackjackGame(None)  # None deoarece nu testăm interfața grafică.

    def test_deck_generation(self):
        """Testează generarea pachetului de cărți."""
        deck = self.game.get_deck()
        self.assertEqual(len(deck), 52, "Pachetul ar trebui să conțină 52 de cărți.")
        self.assertTrue(all(len(card) == 2 for card in deck), "Fiecare carte ar trebui să fie un tuplu cu 2 elemente.")

    def test_hand_value(self):
        """Testează calculul valorii mâinii."""
        hand = [('A', '♠'), ('K', '♠')]
        value = self.game.get_hand_value(hand)
        self.assertEqual(value, 21, "Valoarea mâinii ar trebui să fie 21.")

        hand = [('5', '♦'), ('7', '♣'), ('9', '♥')]
        value = self.game.get_hand_value(hand)
        self.assertEqual(value, 21, "Valoarea mâinii ar trebui să fie 21.")

        hand = [('A', '♠'), ('9', '♠'), ('A', '♦')]
        value = self.game.get_hand_value(hand)
        self.assertEqual(value, 21, "Un As ar trebui să fie considerat 11 dacă nu se depășește 21.")

    def test_game_status(self):
        """Testează logica câștig/pierdere."""
        self.game.playerHand = [('10', '♣'), ('K', '♠')]
        self.game.dealerHand = [('9', '♦'), ('8', '♠')]
        self.assertEqual(self.game.get_hand_value(self.game.playerHand), 20)
        self.assertEqual(self.game.get_hand_value(self.game.dealerHand), 17)
    
        # Simulează sfârșitul jocului
        self.game.check_game_status()
        self.assertTrue(self.game.money > 0, "Jucătorul ar trebui să câștige dacă valoarea este mai mare decât a dealerului.")

if __name__ == '__main__':
    unittest.main()
