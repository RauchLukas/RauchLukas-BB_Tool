import numpy as np

from material import Material

class Model():

    def __init__(self):
        super().__init__()

        self.mlc = 'MLC40'
        self.lm1 = False

        self.nodes = []
        self.supports = [[0,0], [30,0]]

        self.span = self.supports[-1][0]-self.supports[0][0]
        self.spacing = 3.50

        self.krag = 0.5
        self.dist = 'symmetrisch'

        self.makeNodes(self.nodes)
        
        self.col_pos = self.getPosColumn()
        self.col_height = self.getBridgeHeight()

        # Presettings
        self.lr_b = 4.0     #TODO fix by MLC 
        self.lt_l = 5.0
        self.lt_n = 8
        self.lt_h = 0.24
        self.lt_b = 0.18

        self.tb_t = 0.10
        self.fb_t = 0.04

        self.rb_h = 0.20
        self.rb_b = 0.20

        self.ub_krag = 1.0
        self.ub_b = self.lr_b + 2 * self.rb_b + 2 * self.ub_krag
        
        self.gt_h = 1.00
        self.gt_t = 0.08
        self.gt_d = self.gt_h * 0.7
        self.gt_b = self.gt_t
        self.alpha = 60
        self.gp_h = 0.10
        self.gp_t = 0.04

        #Presettings database
        self.m_database = Material()
        self.m_class_lt = 'c24'
        self.m_lt = self.m_database.wood(self.m_class_lt)
        self.m_lt_nkl = 2
        self.m_lt_kled = 'k_sk'
        self.m_lt_type = 'vh'


        self.m_class_tb = 'c24'
        self.m_tb = self.m_database.wood(self.m_class_tb)
        self.m_tb_nkl = 2
        self.m_tb_kled = 'k_sk'
        self.m_tb_type = 'vh'

        self.m_class_jt = 'c24'
        self.m_jt = self.m_database.wood(self.m_class_jt)
        self.m_jt_nkl = 2
        self.m_jt_kled = 'k_sk'
        self.m_jt_type = 'vh'

        self.nu_m_lt = None
        self.nu_v_lt = None
        self.nu_a_lt = None

    def updateMaterial(self, key, mclass):
        if key == 'lt':
            self.m_class_lt = mclass
            self.m_lt = self.m_database.wood(self.m_class_lt)
        if key == 'tb':
            self.m_class_lt = mclass
            self.m_tb = self.m_database.wood(self.m_class_tb)


    def _triger_refresh(self):

        self.getPosColumn()
        self.getBridgeHeight()

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

