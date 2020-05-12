import math
import pandas as pd
from material import Material

# Get Data
em_kette = pd.read_excel('em_kette_stanag2021.xlsx', index_col=0)
eq_kette = pd.read_excel('eq_kette_stanag2021.xlsx', index_col=0)
em_rad = pd.read_excel('em_rad_stanag2021.xlsx', index_col=0)
eq_rad = pd.read_excel('eq_rad_stanag2021.xlsx', index_col=0)

class Core():
    def __init__(self, model):

        # self.model = model

        self.material = Material()

        self.mlc = 40
        self.l_lt = 4.0
        self.n_lt = 5
        self.h_lt = 0.30
        self.b_lt = 0.20
        self.t_tb = 0.06
        self.b_ub = 5.5

        # Material
        self.nkl = 2
        self.kled = 'k_sk'
        self.m_type = 'vh'

        m = self.material.wood('c24')

        self.fmk = m['fmk']
        self.ft0k = m['ft0k']
        self.fvk = m['fvk']
        self.gamma_h = 5.0
        self.kmod = 1

        # Berechnungsparameter
        self.gamma_g = 1.35
        self.gamma_mlc = 1.50

        self.em_w = em_rad.loc[self.l_lt, 'mlc'+str(self.mlc)]
        self.eq_w = eq_rad.loc[self.l_lt, 'mlc'+str(self.mlc)]
        self.em_t = em_kette.loc[self.l_lt, 'mlc'+str(self.mlc)]
        self.eq_t = eq_kette.loc[self.l_lt, 'mlc'+str(self.mlc)]

        print(self.momentOfResistance())
        print(self.shearOfResistance())


        print(self.design())

    def Schwingungsbeiwert(self):
        
        kette = 1.10
        rad = 1.25

        if self.l_lt < 0:
            raise ValueError("Fehler: Länge l < 0")

        phi = 1.4 - self.l_lt * 8e-3
        if phi < 1: 
            phi = 1

        phi_w = min(rad, phi)
        phi_t = min(kette, phi)

        return phi_w, phi_t

    def getSelfWeight(self): 

        self.a_lt = self.h_lt * self.b_lt
        self.a_ub = self.t_tb * self.b_ub

        g = (self.a_lt + self.a_ub) * self.gamma_h      #kN/m

        return g

    def getMomentSelfweight(self):

        g = self.getSelfWeight()

        return g * self.l_lt**2 / 8

    def getShearSelfweight(self):

        g = self.getSelfWeight()

        return g * self.l_lt / 2

    def getMed(self):

        phi_w, phi_t = self.Schwingungsbeiwert()

        m_g = self.getMomentSelfweight()
        
        m_kt = self.em_t
        m_kw = self.em_w

        m_ed = max(phi_w * m_kw, phi_t * m_kt)

        m_ed = m_ed * self.l_lt

        return m_g * self.gamma_g + m_ed * self.gamma_mlc
        
    def getVed(self):

        phi_w, phi_t = self.Schwingungsbeiwert()

        q_g = self.getSelfWeight()

        q_kt = self.eq_t
        q_kw = self.eq_w
        
        q_ed = max(phi_w * q_kw, phi_t * q_kt)

        return q_g * self.gamma_g + q_ed * self.gamma_mlc

    def getCrosssectionArea(self, n=1):

        return n * self.h_lt * self.b_lt

    def getCrosssectionWy(self, n=1):
               
        return n * self.b_lt * self.h_lt**2 / 6

    def momentOfResistance(self):
        
        fmd = self.kmod * self.fmk

        wy = self.getCrosssectionWy(self.n_lt)

        return wy * fmd * 1e+3    # kNm 

    def shearOfResistance(self):

        kcr = self.material.kcr(self.fvk)

        kmod = self.material.kmod(self.nkl, self.kled)

        ft0d = kmod * kcr * self.ft0k

        a = self.getCrosssectionArea(self.n_lt)

        return a * ft0d / 1.5 * 1e+3    # kN 

    def design(self): 

        mEd = self.getMed()
        vEd = self.getVed()

        mRd = self.momentOfResistance()
        vRd = self.shearOfResistance()

        nu = math.sqrt((mEd/mRd)**2 + (vEd/vRd)**2)

        return nu

        


# if __name__ == "__main__":
#     model = None
#     Core(model)