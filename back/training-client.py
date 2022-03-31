import datetime
import requests
import json
import random
import copy
import numpy as np
import concurrent.futures
from operator import itemgetter

MAX_GENERATIONS = 50
POPULATION_SIZE = 100
GENOME_LENGTH = 40 # Must be divisable by 4 as we have 4 constants
CROSS_PROBABILITY = 0.7
MUTATION_PROBABILITY = 0.04

def get_constants(genome):
    #  Min and max value for each constant
    min_max = [
        (0.75, 5.75),
        (-2, 1),
        (-0.5, 2.5),
        (-2, 2)
    ]
    slices = [] # Fragments of Genome array - slicing them in equal parts to extract value from 0-1 array
    for i in range(4):
        slices.append(genome[int(i * (GENOME_LENGTH / 4)) : int((i + 1) * (GENOME_LENGTH / 4))])

    return (
        min_max[0][0] + (min_max[0][1] - min_max[0][0]) / (2 ** (GENOME_LENGTH / 4)) * int(f"0b{''.join([str(x) for x in slices[0]])}", 2),
        min_max[1][0] + (min_max[1][1] - min_max[1][0]) / (2 ** (GENOME_LENGTH / 4)) * int(f"0b{''.join([str(x) for x in slices[1]])}", 2),
        min_max[2][0] + (min_max[2][1] - min_max[2][0]) / (2 ** (GENOME_LENGTH / 4)) * int(f"0b{''.join([str(x) for x in slices[2]])}", 2),
        min_max[3][0] + (min_max[3][1] - min_max[3][0]) / (2 ** (GENOME_LENGTH / 4)) * int(f"0b{''.join([str(x) for x in slices[3]])}", 2),
    )

def generate_population(population_size, number_of_bits):
    return np.random.randint(2, size=(population_size, number_of_bits))

def roulette(population, evaluations):
    temp = (evaluations[:] if np.min(evaluations) > 0 else evaluations + np.abs(np.min(evaluations)) + 1).astype(int)
    probabilities = temp / np.sum(temp)
    new_population_ids = np.random.choice(population.shape[0], size=population.shape[0], p=probabilities)
    new_population = population[new_population_ids.astype(int)].copy()
    return new_population

def mutate(population, probablility):
    mask = np.random.random(size=population.shape) < probablility
    new_population = (np.logical_xor(population, mask)).astype(int)
    return new_population

def cross(population, probablility):
    new_population = copy.deepcopy(population)
    for i in range(0, len(population) - 1, 2):
      r = np.random.random()
      if r < probablility:
        nb = np.random.randint(1, len(population[0]))
        t1 = population[i][:nb]
        t2 = population[i][nb:]
        t3 = population[i + 1][:nb]
        t4 = population[i + 1][nb:]
        new_population[i] =  np.concatenate((t3, t2))
        new_population[i + 1] = np.concatenate((t1, t4))
    return new_population

def target_function(genome):
    (C1, C2, C3, C4) = get_constants(genome)
    def get_arrangement_table_for_placement(ai_player):
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

    def get_best_placement_for_patches(patches, arrangement_table):
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
                                    'score': score * C3 + score2 * C4,
                                })
            if len(possible_placements):
                max_score = max(possible_placements, key=itemgetter('score'))['score']
                items_with_max_score = [obj for obj in possible_placements if obj['score'] == max_score]

                patches_with_placements.append({
                    'placement': random.choice(items_with_max_score),
                    'patch': patch
                })
        return patches_with_placements


    # Create game
    post_response = requests.post("http://127.0.0.1:5000/training-game")
    id = json.loads(post_response.json()['trainingGameId'])['$oid']

    # Get game
    game = requests.get(f"http://127.0.0.1:5000/training-game?id={id}").json()['game']

    while game['player']['timeLeft'] > 0 or 'special' in game['patchesList'][0]['name']:
        # Calculate how many coins may bot have after coin draws
        available_coins = [game['player']['coins']]
        ai_income = sum(p['income_value'] for p in game['player']['patches'])
        for i in range(1, game['player']['timeLeft'] + 1):
            next_income = ai_income + 1 if game['player']['timeLeft'] + i in game['coinFields'] else 1
            available_coins.append(available_coins[-1] + next_income)

        # Check which patches can be afforded during this turn
        affordable_patches = [p for p in game['patchesList'] if p['price_coins'] <= available_coins[-1]]

        arrangement_table = get_arrangement_table_for_placement(game['player'])

        patches_with_placements = get_best_placement_for_patches(affordable_patches, arrangement_table)

        # Buy patch if any can be afforded and can fit
        if (len(patches_with_placements)):
            remaining_incomes = len([c for c in game['coinFields'] if c < game['player']['timeLeft']])
            needed_draws = lambda p: available_coins.index(next((c for c in available_coins if c >= p['price_coins'])))
            patch_size   = lambda p: sum([p for sub in p['arrangement_table'] for p in sub])
            time_needed  = lambda p: (p['price_time'] + needed_draws(p)) or 0.01 # Avoid division by zero when bonus patch is found 
            real_patch_value = lambda p: (patch_size(p) * 2 + remaining_incomes * p['income_value'] - p['price_coins'])/time_needed(p)
            patch_value  = lambda p: C1 * p['real_patch_value'] + C2 * p['patch_size'] + p['placement']['score']

            valued_patches = [{
                'placement': p['placement'],
                'real_patch_value': real_patch_value(p['patch']),
                'patch_size': patch_size(p['patch']),
                'needed_draws': needed_draws(p['patch']),
                'patch': p['patch']
            } for p in patches_with_placements]

            for p in valued_patches:
                p['patch_value'] = patch_value(p)

            best_patch = max(valued_patches, key=itemgetter('patch_value'))
            if best_patch['patch_value'] < 1:
                game = requests.put(f"http://127.0.0.1:5000/training-game?id={id}", json={ 'timeBalance': 1 }).json()['game']
                continue
            if best_patch['needed_draws']:
                game = requests.put(f"http://127.0.0.1:5000/training-game?id={id}", json={ 'timeBalance': best_patch['needed_draws'] }).json()['game']
                continue

            original_patch = next((p for p in game['patchesList'] if p['name'] == best_patch['patch']['name']))
            original_patch['flip'] = best_patch['placement']['flip']
            original_patch['position'] = {'x': best_patch['placement']['x'], 'y': best_patch['placement']['y']}
            original_patch['rotate'] = best_patch['placement']['rotate']

            game = requests.put(f"http://127.0.0.1:5000/training-game?id={id}", json={ 'patch': original_patch }).json()['game']
            continue

        if game['player']['timeLeft'] == 0:
            break
        result = requests.put(f"http://127.0.0.1:5000/training-game?id={id}", json={ 'timeBalance': game['player']['timeLeft'] })
        # if result.status_code == 400:
        #     print(result.text)
        game = result.json()['game']

    score = -162 + 2 * sum([i for sub in [i for sub in map(lambda x: x['arrangement_table'], game['player']['patches']) for i in sub] for i in sub]) + game['player']['coins']
    # Delete game
    delete_response = requests.delete(f"http://127.0.0.1:5000/training-game?id={id}")
    return score, genome, (C1, C2, C3, C4)


generation = 0
population = generate_population(POPULATION_SIZE, GENOME_LENGTH)

for x in range(MAX_GENERATIONS):
    print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} generation {generation}:")
    results = np.array([])

    # Evaluate all individuals in generation 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(target_function, individual) for individual in population] 
        results = np.array([f.result() for f in futures], dtype=object)

    evaluations = results[:,0]
    new_population = roulette(population, evaluations)
    new_population = cross(population, CROSS_PROBABILITY)
    new_population = mutate(population, MUTATION_PROBABILITY)
    print("Best value: ", max(evaluations), " params: ", next(r[2] for r in results if r[0] == max(evaluations)))
    population = new_population
    generation += 1
