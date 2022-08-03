import numpy as np
import moose
import pylab
import rdesigneur as rd


def makeFuncRate():
    model = moose.Neutral( '/library' )
    model = moose.Neutral( '/library/chem' )
    compt = moose.CubeMesh( '/library/chem/compt' )
    compt.volume = 1e-15
    A = moose.Pool( '/library/chem/compt/A' )
    B = moose.Pool( '/library/chem/compt/B' )
    C = moose.Pool( '/library/chem/compt/C' )
    reac = moose.Reac( '/library/chem/compt/reac' )
    func = moose.Function( '/library/chem/compt/reac/func' )
    func.x.num = 1
    func.expr = "(x0/1e8)^2"
    reac.Kf = 0
    moose.connect( C, 'nOut', func.x[0], 'input' )
    moose.connect( func, 'valueOut', reac, 'setNumKf' )
    moose.connect( reac, 'sub', A, 'reac' )
    moose.connect( reac, 'prd', B, 'reac' )

    A.concInit = 1
    B.concInit = 0
    C.concInit = 0
    reac.Kb = 1

makeFuncRate()
rdes = rd.rdesigneur(
        turnOffElec = True,
        #This subdivides the 50-micron cylinder into 2 micron voxels
        diffusionLength = 2e-6,
        cellProto = [['somaProto', 'soma', 5e-6, 50e-6]],
        chemProto = [['chem', 'chem']],
        chemDistrib = [['chem', 'soma', 'install', '1' ]],
        plotList = [['soma', '1', 'dend/A', 'conc', 'A conc', 'wave'],
            ['soma', '1', 'dend/B', 'conc', 'B conc', 'wave'],
            ['soma', '1', 'dend/C', 'conc', 'C conc', 'wave']],
)
rdes.buildModel()
C = moose.element( '/model/chem/dend/C' )
C.vec.concInit = [ 1+np.sin(x/5.0) for x in range( len(C.vec) ) ]
moose.reinit()
print("Printing Kfs")
print(moose.vec("/model/chem/dend/reac").Kf)
print("Printing NumKfs")
print(moose.element("/model/chem/dend/reac"))
moose.start(10)
print("Printing Kfs")
print(moose.element("/model/chem/dend/reac").Kf)
print("Printing NumKfs")
print(moose.element("/model/chem/dend/reac").vec)
rdes.display()

