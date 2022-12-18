import json, os

setting = json.load(open('data/setting.json'))
SIZE_X = setting['grid']['size_x']
SIZE_Y = setting['grid']['size_y']

class SaveManager:

    def __init__(self, filename, path_folder):

        self.default_board = [[-1 for row in range(SIZE_Y)] for column in range(SIZE_X)]
        # self.default_value = dict.fromkeys(['PlayerName','Board', 'Turn'])
        self.default_value = {
            "PlayerName" : {
                "Player1" : "Anonymous",
                "Player2" : "Anonymous"
            },
            "Board" : self.default_board,
            # phải để 1, đừng để True False
            "Turn" : 0
        }
        self.filename = filename
        self.path_folder = path_folder
        self.path = os.path.join(path_folder, filename)
    
    def check_file(self):
        return os.path.isfile(self.path) and os.path.getsize(self.path) > 0

    def save(self, data):
        with open(self.path, "w") as file:
            json.dump(data, file, indent = 4)
    
    def load(self):
        if self.check_file():
            with open(self.path, "r") as file:
                return json.load(file)
        return self.default_value

    def refresh(self):
        return self.default_value
