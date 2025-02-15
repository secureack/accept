from classes import output

class stdout(output.output):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,event):
        print(event)
