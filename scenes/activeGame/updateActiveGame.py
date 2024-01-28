from config import GRAVITY, LOG_FUNCTION_CALLS
from scenes.activeGame.activeGameControls import active_game_controls
from scenes.activeGame.handleCollisions import handle_collisions

def update_active_game(player, platformManager, environment, seconds):
    if LOG_FUNCTION_CALLS:
        print('running update_active_game')
    player.y += GRAVITY
    active_game_controls(player)
    player.update()
    environment.update()
    handle_collisions(player, platformManager.platforms, seconds)
    platformManager.update()
    player.update_animation()