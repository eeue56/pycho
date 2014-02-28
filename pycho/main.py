from pycho.core.app import application
 
if __name__ == '__main__':
    game, app, window = application('level_data.json', 50, 50, player_options={'speed' : 2})
    app.exec_()