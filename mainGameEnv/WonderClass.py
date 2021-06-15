from mainGameEnv.resourceClass import Resource
class Wonder:
    def __init__(self, name,side,resourceIni,resourceAmount, **kwargs):
        self.name = name
        self.side = side
        self.stage = 0
        self.step = {}
        self.beginResource = Resource(resourceIni,resourceAmount)
        steps = kwargs
        print(len(steps))
        for level in steps:
            self.step[level] = kwargs[level]
    def printWonder(self):
        print(self.__dict__)
        self.beginResource.printResource()

