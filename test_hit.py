def test_hit_action(self):
    """Testează acțiunea de Hit."""
    initial_hand_size = len(self.game.playerHand)
    self.game.playerHand = [('5', '♣'), ('6', '♠')]
    self.game.deck = [('K', '♦')]  # Adaugă o carte cunoscută în pachet.

    self.game.handle_move('H')
    self.assertEqual(len(self.game.playerHand), initial_hand_size + 1, "Mâna jucătorului ar trebui să conțină o carte în plus.")
    self.assertEqual(self.game.playerHand[-1], ('K', '♦'), "Ultima carte din mână ar trebui să fie 'K♦'.")
