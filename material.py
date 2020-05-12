"""
This modul only contains the Material class

Author: Lukas Rauch
"""

class Material(object):
    """
    Material data of a local cross section.

    Attributes 
    ---------
    id : int or str
        Unique matrial ID.
    density : float
        Material density to calculate the material weight.
    youngs_modulus : float
        Material young's modulus.
    fmk : float
        Avarage bending stiffness - characteristic.
    ft0k : float
        Tension stiffness parallel to material fiber.
    ft90k : float
        Tension stiffness vertical to material fiber.
    fc0k : float
        Compression stiffness parallel to material fiber.
    fc90k : float
        Compression stiffness vertical to material fiber.

    """

    def __init__(self):

        # self.model = model
        # , id, materialtype='wood',
        # density=0, youngs_modulus=0, fmk=0, fvk=0, 
        # ft0k=0, ft90k=0, fc0k=0, fc90k=0):
        # """
        # Create a new material.
        # """
        # self.id = id
        # self.materialtype = materialtype    # string
        # self.density = density
        # self.youngs_modulus = youngs_modulus
        # self.fmk = fmk
        # self.fvk = fvk
        # self.ft0k = ft0k
        # self.ft90k = ft90k
        # self.fc0k = fc0k
        # self.fc90k = fc90k
        pass

    def wood(self, materialclass):
        """
        Database of material data: wood
        """
        materialdata = {
            'c14' :{'fmk': 14, 'ft0k':  8, 'ft90k': 0.4, 'fc0k': 16, 'fc90k': 2.0, 'fvk': 3.0, 'e0mean': 7,    'e005': 4.7,  'e90mean': 0.23, 'gmean': 0.44, 'rok': 290, 'romean': 350},
            'c16' :{'fmk': 16, 'ft0k': 10, 'ft90k': 0.4, 'fc0k': 17, 'fc90k': 2.2, 'fvk': 3.2, 'e0mean': 8,    'e005': 5.4,  'e90mean': 0.27, 'gmean': 0.50, 'rok': 310, 'romean': 370},
            'c18' :{'fmk': 18, 'ft0k': 11, 'ft90k': 0.4, 'fc0k': 18, 'fc90k': 2.2, 'fvk': 3.4, 'e0mean': 9,    'e005': 6.0,  'e90mean': 0.30, 'gmean': 0.56, 'rok': 320, 'romean': 380},
            'c20' :{'fmk': 20, 'ft0k': 12, 'ft90k': 0.4, 'fc0k': 19, 'fc90k': 2.3, 'fvk': 3.6, 'e0mean': 9.5,  'e005': 6.4,  'e90mean': 0.32, 'gmean': 0.59, 'rok': 330, 'romean': 390},
            'c22' :{'fmk': 22, 'ft0k': 13, 'ft90k': 0.4, 'fc0k': 20, 'fc90k': 2.4, 'fvk': 3.8, 'e0mean': 10,   'e005': 6.7,  'e90mean': 0.33, 'gmean': 0.63, 'rok': 340, 'romean': 410},
            'c24' :{'fmk': 24, 'ft0k': 14, 'ft90k': 0.4, 'fc0k': 21, 'fc90k': 2.5, 'fvk': 4.0, 'e0mean': 11,   'e005': 7.4,  'e90mean': 0.37, 'gmean': 0.69, 'rok': 350, 'romean': 420},
            'c27' :{'fmk': 27, 'ft0k': 16, 'ft90k': 0.4, 'fc0k': 22, 'fc90k': 2.6, 'fvk': 4.0, 'e0mean': 11.5, 'e005': 7.7,  'e90mean': 0.38, 'gmean': 0.72, 'rok': 370, 'romean': 450},
            'c30' :{'fmk': 30, 'ft0k': 18, 'ft90k': 0.4, 'fc0k': 23, 'fc90k': 2.7, 'fvk': 4.0, 'e0mean': 12,   'e005': 8.0,  'e90mean': 0.40, 'gmean': 0.75, 'rok': 380, 'romean': 460},
            'c35' :{'fmk': 35, 'ft0k': 21, 'ft90k': 0.4, 'fc0k': 25, 'fc90k': 2.8, 'fvk': 4.0, 'e0mean': 13,   'e005': 8.7,  'e90mean': 0.43, 'gmean': 0.81, 'rok': 400, 'romean': 480},
            'c40' :{'fmk': 40, 'ft0k': 24, 'ft90k': 0.4, 'fc0k': 26, 'fc90k': 2.9, 'fvk': 4.0, 'e0mean': 14,   'e005': 9.4,  'e90mean': 0.47, 'gmean': 0.88, 'rok': 420, 'romean': 500},
            'c45' :{'fmk': 45, 'ft0k': 27, 'ft90k': 0.4, 'fc0k': 27, 'fc90k': 3.1, 'fvk': 4.0, 'e0mean': 15,   'e005': 10.0, 'e90mean': 0.50, 'gmean': 0.94, 'rok': 440, 'romean': 520},
            'c50' :{'fmk': 50, 'ft0k': 30, 'ft90k': 0.4, 'fc0k': 29, 'fc90k': 3.2, 'fvk': 4.0, 'e0mean': 16,   'e005': 10.7, 'e90mean': 0.53, 'gmean': 1.00, 'rok': 460, 'romean': 550}
        }

        return materialdata[materialclass]

    def kmod(self, nkl, kled):
        """
        returns k_mod factor depending on the "Nutzungsklasse" NKL and KLED.
        Function only valid for "Vollholz" VH and "Brettschichtholz" BSH.
        """
        kmod_data = {
            1 : {'staendig': 0.6, 'lang': 0.7,  'mittel': 0.8,  'kurz': 0.9, 'k_sk': 1.0, 'sehr_kurz': 1.1},
            2 : {'staendig': 0.6, 'lang': 0.7,  'mittel': 0.8,  'kurz': 0.9, 'k_sk': 1.0, 'sehr_kurz': 1.1},
            3 : {'staendig': 0.5, 'lang': 0.55, 'mittel': 0.65, 'kurz': 0.7, 'k_sk': 0.8, 'sehr_kurz': 0.9}
        }

        return kmod_data[nkl][kled]

    def kcr(self, fvk, woodentype='vh'):
        """
        Returns the factor kcr depending on the wooden class 
        (Vollholz = 'vh', Brettschichtholz='bsh' and the characteristic s
        hear resistance value of the material.)
        """
        if woodentype == 'vh':
            kcr = 2.0/fvk
        elif woodentype == 'bsh':
            kcr = 2.5/self.fvk
        else: 
            raise RuntimeError('The woodentype {} is not part of the library!' .format(woodentype))

        return kcr


