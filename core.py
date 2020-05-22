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

        self.model = model

        self.material = Material()
        
        # Berechnungsparameter
        self.gamma_g = 1.35
        self.gamma_gm = 1.30
        self.gamma_mlc = 1.50

        self.gamma_holz = 5.0

        self.refreshModel()

    def refreshModel(self):
        self.mlc = self.model.mlc
        self.lt_l = self.model.lt_l
        self.lt_n = self.model.lt_n
        self.lt_h = self.model.lt_h
        self.lt_b = self.model.lt_b
        self.tb_t = self.model.tb_t
        self.ub_b = self.model.ub_b

        # Material
        self.name = self.model.m_class_lt
        self.nkl = self.model.m_lt_nkl
        self.kled = self.model.m_lt_kled
        self.m_type = self.model.m_lt_type

        m = self.material.wood(self.name)

        self.fmk = m['fmk']
        self.ft0k = m['ft0k']
        self.fvk = m['fvk']
        self.kmod = self.material.kmod(self.nkl, self.kled)

        self.em_w = em_rad.loc[self.lt_l, self.mlc]
        self.eq_w = eq_rad.loc[self.lt_l, self.mlc]
        self.em_t = em_kette.loc[self.lt_l, self.mlc]
        self.eq_t = eq_kette.loc[self.lt_l, self.mlc]


    def Schwingungsbeiwert(self):
        
        kette = 1.10
        rad = 1.25

        if self.lt_l < 0:
            raise ValueError("Fehler: Länge l < 0")

        phi = 1.4 - self.lt_l * 8e-3
        if phi < 1: 
            phi = 1

        phi_w = min(rad, phi)
        phi_t = min(kette, phi)

        return phi_w, phi_t

    def getSelfWeight(self): 

        self.a_lt = self.lt_h * self.lt_b
        self.a_ub = self.tb_t * self.ub_b

        g = (self.a_lt + self.a_ub) * self.gamma_holz      #kN/m

        return g

    def getMomentSelfweight(self):

        g = self.getSelfWeight()

        return g * self.lt_l**2 / 8

    def getShearSelfweight(self):

        g = self.getSelfWeight()

        return g * self.lt_l / 2

    def getMed(self):

        phi_w, phi_t = self.Schwingungsbeiwert()

        m_g = self.getMomentSelfweight()
        
        m_kt = self.em_t
        m_kw = self.em_w

        m_ed = max(phi_w * m_kw, phi_t * m_kt)

        m_ed = m_ed * self.lt_l

        return m_g * self.gamma_g + m_ed * self.gamma_mlc
        
    def getVed(self):

        phi_w, phi_t = self.Schwingungsbeiwert()

        q_g = self.getSelfWeight()

        q_kt = self.eq_t
        q_kw = self.eq_w
        
        q_ed = max(phi_w * q_kw, phi_t * q_kt)

        return q_g * self.gamma_g + q_ed * self.gamma_mlc

    def getCrosssectionArea(self, n=1):

        return n * self.lt_h * self.lt_b

    def getCrosssectionWy(self, n=1):
               
        return n * self.lt_b * self.lt_h**2 / 6

    def momentOfResistance(self):

        self.fmk = self.model.m_lt['fmk']

        fmd = self.kmod * self.fmk / self.gamma_gm

        wy = self.getCrosssectionWy(self.lt_n)

        return wy * fmd * 1e+3    # kNm 

    def shearOfResistance(self):

        kcr = self.material.kcr(self.fvk)

        kmod = self.material.kmod(self.nkl, self.kled)

        ft0d = kmod * kcr * self.ft0k / self.gamma_gm

        a = self.getCrosssectionArea(self.lt_n)

        return a * ft0d / 1.5 * 1e+3    # kN 

    def auflagerpressung(self, b):

        kmod = self.material.kmod(self.nkl, self.kled)

        self.fc90k = self.model.m_lt['fc90k']

        fc90d = kmod * self.fc90k / self.gamma_gm

        kc90 = 1.25     
        '''
        Annahme: 
            1. Schellendruck statt Auflagerdruck. Die Funktion wird für beides gleich verwendet. 
            2. Abstand zwischen zwei Lagern ist größer als die doppelte Auflagerbreite.
        '''
        a = b * (b + 2*0.03)     # in [m]

        rd = a * kc90 * fc90d * 1e3     # in kN 

        return rd

    def design(self, model): 
        
        self.refreshModel()

        mEd = self.getMed()
        vEd = self.getVed()

        mRd = self.momentOfResistance()
        vRd = self.shearOfResistance()
        aRd = self.auflagerpressung(self.lt_b)

        nu_m = mEd/mRd              # Biegenachweis Längsträger
        nu_v = vEd/vRd              # Querkraftnachweis Längsträger
        nu_a = vEd/aRd/self.lt_n  # Auflagerpressung Längsträger

        print(f"\nAusnutungsgrade: \nMoment: {nu_m:.2f} \nQuerkraft: {nu_v:.2f} \nAuflagerpressung: {nu_a:.2f}")

        return max(nu_m, nu_v, nu_a)


# if __name__ == "__main__":
#     model = None
#     Core(model)