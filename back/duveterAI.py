from doctest import script_from_examples
import copy
import numpy as np
import random
from operator import itemgetter

class DuveterAI():
    USERNAME="SophieBot"

    @staticmethod
    def __draw_coins(count, ai_player):
        coins_to_draw = ai_player['timeLeft'] if ai_player['timeLeft'] < count else count
        ai_player['timeLeft'] -= coins_to_draw
        ai_player['coins'] += coins_to_draw

    @staticmethod
    def __get_arrangement_table_for_placement(ai_player):
        arrangement_table = [[0 for j in range(9)] for i in range(9)]
        # Place all patches
        for patch in ai_player['patches']:
            patch_arrangement_table = copy.deepcopy(patch['arrangement_table'])
            x = patch['position']['x']
            y = patch['position']['y']
            if patch['rotate']:
                patch_arrangement_table = np.rot90(patch_arrangement_table, k=patch['rotate'], axes=(1,0))
            if patch['flip']:
                patch_arrangement_table = np.flip(patch_arrangement_table, axis=1)

            width = len(patch_arrangement_table[0])
            height = len(patch_arrangement_table)
            for i in range(width):
                for j in range(height):
                    arrangement_table[j + y][i + x] += patch_arrangement_table[j][i]
        # Generate -0.5, -1 and -2 fields for top-left AI placement proprity
        for i in range(9):
            for j in range(9):
                if arrangement_table[j][i] == 0:
                    if j - 1 < 0 or arrangement_table[j - 1][i] > 0:
                        arrangement_table[j][i] -= 1
                    if i - 1 < 0 or arrangement_table[j][i - 1] > 0:
                        arrangement_table[j][i] -= 1
                    if j < 8 and arrangement_table[j + 1][i] > 0:
                        arrangement_table[j][i] -= 0.5
                    if i < 8 and arrangement_table[j][i + 1] > 0:
                        arrangement_table[j][i] -= 0.5
        return arrangement_table

    @staticmethod
    def __get_best_placement_for_patches(patches, arrangement_table):
        patches_with_placements = []
        for patch in patches:
            possible_placements = []
            for rotate in range(4):
                for flip in range(2):
                    patch_arrangement_table = copy.deepcopy(patch['arrangement_table'])
                    patch_arrangement_table = np.rot90(patch_arrangement_table, k=rotate, axes=(1,0))
                    if flip:
                        patch_arrangement_table = np.flip(patch_arrangement_table, axis=1)
                    width = len(patch_arrangement_table[0])
                    height = len(patch_arrangement_table)
                    for x in range(9 - width + 1):
                        for y in range(9 - height + 1):
                            valid = True
                            score = 0
                            score2 = 0
                            for i in range(width):
                                for j in range(height):
                                    if patch_arrangement_table[j][i] == 1:
                                        if arrangement_table[j + y][i + x] > 0:
                                            valid = False
                                        if arrangement_table[j + y][i + x] < 0:
                                            score -= arrangement_table[j + y][i + x]
                                        if arrangement_table[j + y][i + x] <= -2:
                                            score2 += 1
                            if valid:
                                possible_placements.append({
                                    'x': x,
                                    'y': y,
                                    'rotate': rotate,
                                    'flip': flip,
                                    'score': score,
                                    'score2': score2
                                })
            if len(possible_placements):
                max_score = max(possible_placements, key=itemgetter('score'))['score']
                items_with_max_score = [obj for obj in possible_placements if obj['score'] == max_score]
                max_score2 = max(items_with_max_score, key=itemgetter('score2'))['score2']
                items_with_max_score2 = [obj for obj in items_with_max_score if obj['score2'] == max_score2]
                patches_with_placements.append({
                    'placement': random.choice(items_with_max_score2),
                    'patch': patch
                })
        return patches_with_placements

    @staticmethod
    def make_move(game):
        player = game['players'][0]
        ai_player = game['players'][1]
        
        available_time = ai_player['timeLeft'] - player['timeLeft']
        available_patches = game['patchesList'][:3]
            
        # Calculate how many coins may bot have after coin draws
        available_coins = [ai_player['coins']]
        ai_income = sum(p['income_value'] for p in ai_player['patches'])
        for i in range(1, available_time + 1):
            next_income = ai_income + 1 if ai_player['timeLeft'] + i in game['coinFields'] else 1
            available_coins.append(available_coins[-1] + next_income)
        
        # Check which patches can be afforded during this turn
        affordable_patches = [p for p in available_patches if p['price_coins'] <= available_coins[-1]]

        arrangement_table = DuveterAI.__get_arrangement_table_for_placement(ai_player)
        patches_with_placements = DuveterAI.__get_best_placement_for_patches(affordable_patches, arrangement_table)

        # Buy patch if any can be afforded and can fit
        if (len(patches_with_placements)):
            remaining_incomes = len([c for c in game['coinFields'] if c < ai_player['timeLeft']])
            needed_draws = lambda p: available_coins.index(next((c for c in available_coins if c >= p['price_coins'])))
            patch_size   = lambda p: sum([p for sub in p['arrangement_table'] for p in sub])
            time_needed  = lambda p: (p['price_time'] + needed_draws(p)) or 0.01 # Avoid division by zero when bonus patch is found 
            patch_value  = lambda p: (patch_size(p) * 2 + remaining_incomes * p['income_value'] - p['price_coins'])/time_needed(p)

            valued_patches = [{
                'placement': p['placement'],
                'patch_value': patch_value(p['patch']),
                'patch_size': patch_size(p['patch']),
                'needed_draws': needed_draws(p['patch']),
                'patch': p['patch']
            } for p in patches_with_placements]

            best_patch = max(valued_patches, key=itemgetter('patch_value'))
            if best_patch['patch_value'] < 1:
                DuveterAI.__draw_coins(1, ai_player)
                return
            if best_patch['needed_draws']:
                DuveterAI.__draw_coins(best_patch['needed_draws'], ai_player)
                return

            original_patch = next((p for p in game['patchesList'] if p['name'] == best_patch['patch']['name']))
            patch_index = game['patchesList'].index(original_patch)
            original_patch['flip'] = best_patch['placement']['flip']
            original_patch['position'] = {'x': best_patch['placement']['x'], 'y': best_patch['placement']['y']}
            original_patch['rotate'] = best_patch['placement']['rotate']

            # Remove used patch from game.patchesList and add to players[].patches
            game['patchesList'].pop(patch_index)
            ai_player['patches'].append(original_patch)

            # Move patches (before taken one) to the end
            while patch_index:
                game['patchesList'].append(
                    game['patchesList'].pop(0)
                )
                patch_index -= 1

            # Pay for patch
            ai_player['timeLeft'] -= original_patch['price_time']
            ai_player['coins'] -= original_patch['price_coins']
            return

        # If no other valid move could have been made - draw coins 
        DuveterAI.__draw_coins(ai_player["timeLeft"] - player["timeLeft"] + 1, ai_player)
