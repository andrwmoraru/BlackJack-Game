import unittest
from BlackJackGame import BlackjackGame

def test_full_round(self):
    """Testează o rundă completă de joc."""
    self.game.money = 1000  # Setează o sumă inițială de bani.
    self.game.bet = 100     # Setează pariul.
    self.game.deck = [
        ('10', '♠'), ('9', '♥'),  # Dealer: cărțile inițiale
        ('5', '♣'), ('6', '♦'),  # Player: cărțile inițiale
        ('8', '♠'), ('K', '♣'),  # Cărți pentru Hit
        ('3', '♦'), ('2', '♠')   # Dealer completează mâna
    ]
    self.game.start_new_game()

    # Verifică mâna inițială
    self.assertEqual(len(self.game.playerHand), 2, "Jucătorul ar trebui să aibă 2 cărți la început.")
    self.assertEqual(len(self.game.dealerHand), 2, "Dealerul ar trebui să aibă 2 cărți la început.")

    # Simulează jucătorul care face Hit
    self.game.handle_move('H')  # Trage o carte
    self.assertEqual(len(self.game.playerHand), 3, "Jucătorul ar trebui să aibă 3 cărți după un Hit.")
    self.assertEqual(self.game.playerHand[-1], ('8', '♠'), "Ultima carte trasă ar trebui să fie '8♠'.")

    # Jucătorul decide să se oprească
    self.game.handle_move('S')

    # Dealerul își joacă mâna
    dealer_value = self.game.get_hand_value(self.game.dealerHand)
    self.assertGreaterEqual(dealer_value, 17, "Dealerul ar trebui să se oprească la o valoare de cel puțin 17.")

    # Verifică rezultatul final
    player_value = self.game.get_hand_value(self.game.playerHand)
    self.assertTrue(player_value <= 21, "Jucătorul nu ar trebui să depășească 21.")
    
    if player_value > dealer_value and player_value <= 21:
        self.assertGreater(self.game.money, 1000, "Jucătorul ar trebui să câștige bani dacă valoarea este mai mare decât a dealerului.")
    elif player_value == dealer_value:
        self.assertEqual(self.game.money, 1000, "Jucătorul ar trebui să își recupereze pariul în caz de egalitate.")
    else:
        self.assertLess(self.game.money, 1000, "Jucătorul ar trebui să piardă bani dacă valoarea este mai mică decât a dealerului.")
