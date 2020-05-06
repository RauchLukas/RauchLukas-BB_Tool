import numpy as np

class Model():

    def __init__(self):
        super().__init__()

        self.model = dict()
        self.nodes = []
        self.supports = [[0,0], [30,0]]

        self.span = 30
        self.spacing = 3.50

        self.krag = 0.5
        self.dist = 'symmetrisch'

        self.makeNodes(self.nodes)
        
        self.col_pos = self.getPosColumn()
        self.col_height = self.getBridgeHeight()


    def _triger_refresh(self):

        self.getPosColumn()
        self.getBridgeHeight()

        pass
    
    def getModel(self):

        self.model['nodes'] = self.nodes
        self.model['support'] = self.support
        self.model['span'] = float(self.span)
        self.model['spacing'] = float(self.spacing)
        self.model['krag'] = self.krag
       
        return self.model
        

    def makeNodes(self, nodelist):
        '''Collecting the actual node list and the support coordinates making one sorted nodelist.'''

        out = [self.supports[0]]
        end = self.supports[-1]

        # Check if Nodelist is empty 
        #   -> In case: make it [0,0]
        if nodelist == []:
            nodelist = out
        if nodelist == [[]]:
            nodelist = out
        # If nodelist is NOT empty, but dose not has [0,0] in first place
        #   -> Append it to [0,0]
        if nodelist[0][0] != 0: 
            out.extend(nodelist)
        else: 
        #   -> In Case nodelist has [0,0] just copy it
            out = nodelist
        if out[-1][0] != end[0]: 
            out.append(end)

        out = sorted(out, key=lambda x: x[0] )

        self.nodes = out
        return out

    def getNodesSeperated(self):
        
        x = []
        y = []
        for xi, yi in iter(self.nodes):
            x.append(xi)
            y.append(yi)

        return x, y

    def getPosColumn(self):

        span = self.span
        spacing = float(self.spacing)

        n_full = int(span / spacing)
        self.n_fields = n_full + 1


        
        if self.dist == 'linear':

            res = (span - (n_full * spacing))

            spur = 0
            vec = [0]

            for i in range(n_full):
                spur += spacing
                vec.append(spur)
            
            if res != 0:
                vec.append(spur + res)
        else:
            
            res = 0.5 * (span - (n_full * spacing))
            spur = res
            vec = [0]

            if res != 0:
                vec.append(res)
            
            for i in range(n_full):
                spur += spacing
                vec.append(spur)
            
            if res != 0:
                vec.append(spur + res)

        self.col_pos = vec
        return vec

    def getBridgeHeight(self):

        xe = self.getPosColumn()

        xp, fp = self.getNodesSeperated()

        self.col_height = np.interp(xe, xp, fp)

        return self.col_height

