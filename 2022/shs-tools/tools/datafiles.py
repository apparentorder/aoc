import json
import os
import pickle


class DataFile(dict):
    def __init__(self, filename: str, create: bool):
        super().__init__()
        self.filename = filename

        try:
            os.stat(self.filename)
        except OSError as e:
            if not create:
                raise e
            else:
                open(self.filename, "w").close()

        self.load()

    def load(self):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()


class JSONFile(DataFile):
    def __init__(self, filename: str, create: bool):
        super().__init__(filename, create)

    def load(self):
        with open(self.filename, "rt") as f:
            c = f.read()

        if len(c) > 0:
            self.update(json.loads(c))

    def save(self):
        with open(self.filename, "wt") as f:
            f.write(json.dumps(self.copy(), indent=4))


class PickleFile(DataFile):
    def __init__(self, filename: str, create: bool) -> None:
        super().__init__(filename, create)

    def load(self) -> None:
        with open(self.filename, "rb") as f:
            c = f.read()

        if len(c) > 0:
            self.update(pickle.loads(c))

    def save(self) -> None:
        with open(self.filename, "wb") as f:
            pickle.dump(self.copy(), f)
