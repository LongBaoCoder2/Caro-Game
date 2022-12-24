import json, os


class SaveManager:
    def __init__(self, filename, path_folder):
        print("hello")
        self.setting = json.load(open('data/setting.json'))
        self.SIZE_X = self.setting['grid']['size_x']
        self.SIZE_Y = self.setting['grid']['size_y']

        self.default_board = [[-1 for row in range(self.SIZE_Y)] for column in range(self.SIZE_X)]
        # self.default_value = dict.fromkeys(['PlayerName','Board', 'Turn'])
        self.default_value = {
            "PlayerName" : {
                "Player1" : "",
                "Player2" : ""
            },
            "Board" : self.default_board,
            # phải để 1, đừng để True False
            "Turn" : 1
        }
        self.filename = filename
        self.path_folder = path_folder
        self.path = os.path.join(path_folder, filename)
    
    def check_file(self):
        return os.path.isfile(self.path) and os.path.getsize(self.path) > 0

    def save(self, data):
        #print(data)
        with open(self.path, "w") as file:
            json.dump(data, file, indent = 4)
    
    def load(self):
        if self.check_file():
            with open(self.path, "r") as file:
                return json.load(file)
        return self.default_value

    def refresh(self):
        return self.default_value
