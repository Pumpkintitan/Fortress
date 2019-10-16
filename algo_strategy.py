import gamelib
import random
import math
import warnings
from sys import maxsize

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips:

Additional functions are made available by importing the AdvancedGameState
class from gamelib/advanced.py as a replacement for the regular GameState class
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical
board states. Though, we recommended making a copy of the map to preserve
the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        """
        Read in config and perform any initial setup here
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]


    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.fortress(game_state)

        game_state.submit_turn()

    def fortress(self, game_state):
        """
        Repair Wall
        """
        self.repairWall(game_state)

        """
        Finally deploy our information units to attack.
        """
        self.deploy_attackers(game_state)

    # Here we make the C1 Logo!
    def repairWall(self, game_state):
        """
        Create lists of important locations in order of importance
        """
        first_row = [[0, 13], [1, 13],[2, 13],[3, 13],[4, 13],[5, 13],[6, 13],[7, 13],[8, 13],[9, 13],[10, 13],[11, 13],[12, 13],[13, 13],[15, 13],[16, 13],[17, 13],[18, 13],[19, 13],[20, 13],[21, 13],[22, 13],[23, 13],[24, 13],[25, 13],[26, 13],[27, 13]]
        destructor_loc1 = [[12,11], [16,11]]
        second_row = [[13, 12],[15, 12],[12, 12],[16, 12],[11, 12],[17, 12],[1, 12],[2, 12],[3, 12],[4, 12],[5, 12],[6, 12],[7, 12],[8, 12],[9, 12],[10, 12],[18, 12],[19, 12],[20, 12],[21, 12],[22, 12],[23, 12],[24, 12],[25, 12],[26, 12]]
        destructor_loc2 = [[8,11], [20,11]]
        encryptor_loc1 = [[13,11], [15,11]]
        destructor_loc3 = [[4,11], [24,11]]
        encryptor_row1 = [[13,10], [15,10]]
        destructor_row1 = [[12,10], [16,10]]
        encryptor_row2 = [[13,9], [15,9]]
        destructor_row2 = [[12,9], [16,9]]
        encryptor_row3 = [[13,8], [15,8]]
        destructor_row3 = [[12,8], [16,8]]

        for location in first_row:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)

        for location in destructor_loc1:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        for location in second_row:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)

        for location in destructor_loc2:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        for location in encryptor_loc1:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)

        for location in destructor_loc3:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        for location in encryptor_row1:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)

        for location in destructor_row1:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        for location in encryptor_row2:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)

        for location in destructor_row2:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        for location in encryptor_row3:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)

        for location in destructor_row3:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)




    def deploy_attackers(self, game_state):
        """
        First lets check if we have 10 bits, if we don't we lets wait for
        a turn where we do.
        """

        if (game_state.get_resource(game_state.BITS) >= 12):
            if game_state.can_spawn(EMP, [11, 2,], 3):
                game_state.attempt_spawn(EMP, [11, 2,], 3)

        #friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)

        scrambler_loc = [[10,3],[17,3],[11,2],[16,2],[12,1],[15,1],[13,0],[14,0]]
        if (game_state.get_resource(game_state.BITS) > 1):
            deploy_index = random.randint(0, len(scrambler_loc) - 1)
            deploy_location = scrambler_loc[deploy_index]
            game_state.attempt_spawn(SCRAMBLER, deploy_location)



if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
