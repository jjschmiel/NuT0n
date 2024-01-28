from config import GRAVITY, LOG_FUNCTION_CALLS
from scenes.activeGame.activeGameControls import active_game_controls
from scenes.activeGame.handleCollisions import handle_collisions

def update_active_game(player, platforms, environment):
    if LOG_FUNCTION_CALLS:
        print('running update_active_game')
    player.y += GRAVITY
    active_game_controls(player)
    player.update()
    environment.update()
    handle_collisions(player, platforms)
    player.update_animation()