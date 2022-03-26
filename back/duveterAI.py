class DuveterAI():
    USERNAME="SophieBot"

    @staticmethod
    def make_move(game):
        player = game['players'][0]
        ai_player = game['players'][1]
        
        while ai_player["timeLeft"] >= player["timeLeft"]:
            ai_player['timeLeft'] -= 1
            ai_player['coins'] += 1
