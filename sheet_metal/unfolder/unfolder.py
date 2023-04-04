# $Id$
#
# Copyright (C) 2008-2014, Roman Lygin. All rights reserved.
# Copyright (C) 2014-2023, CADEX. All rights reserved.
#
# This file is part of the CAD Exchanger software.
#
# You may use this file under the terms of the BSD license as follows:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import sys

from pathlib import Path

import cadexchanger.CadExCore as cadex
import manufacturingtoolkit.CadExMTK as mtk

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../"))

class PartCollector(cadex.ModelData_Model_VoidElementVisitor):
    def __init__(self, thePartVec: list):
        super().__init__()
        self.myPartVec = thePartVec

    def VisitPart(self, thePart: cadex.ModelData_Part):
        self.myPartVec.append(thePart)

# Compute approximate thickness value, which can be used as the input thickness value for SheetMetal_Unfolder.
def CalculateInitialThicknessValue(theShape: cadex.ModelData_Shape):
    aVolume = cadex.ModelAlgo_ValidationProperty_ComputeVolume(theShape)
    aSurfaceArea = cadex.ModelAlgo_ValidationProperty_ComputeSurfaceArea(theShape)
    aThickness = aVolume / (aSurfaceArea / 2.0)
    return aThickness

def Unfold(thePart: cadex.ModelData_Part):
    aBRep = thePart.BRepRepresentation()
    if aBRep:
        anUnfolder = mtk.SheetMetal_Unfolder()
        # Iterate over bodies
        aBodyList = aBRep.Get()
        for aBody in aBodyList:
            aShapeIt = cadex.ModelData_Shape_Iterator(aBody)
            while aShapeIt.HasNext():
                aShape = aShapeIt.Next()
                if aShape.Type() == cadex.ModelData_ST_Solid:
                    aSolid = cadex.ModelData_Solid_Cast(aShape)
                    aThickness = CalculateInitialThicknessValue(aSolid)
                    return anUnfolder.Perform(aSolid, aThickness)
                elif aShape.Type() == cadex.ModelData_ST_Shell:
                    aShell = cadex.ModelData_Shell_Cast(aShape)
                    return anUnfolder.Perform(aShell)
    return cadex.ModelData_Shell()

def WriteToDrawing(theUnfoldedShell: cadex.ModelData_Shell, theFilePath: str):
    aDrawing = mtk.SheetMetal_Unfolder().CreateDrawing(theUnfoldedShell)
    if aDrawing.IsNull():
        return False
    aDrawingModel = cadex.ModelData_Model()
    aDrawingModel.SetDrawing(aDrawing)
    aWriter = cadex.ModelData_ModelWriter()
    aRes = aWriter.Write(aDrawingModel, cadex.Base_UTF16String(theFilePath))
    return aRes

def main(theSource: str, theDrawingPath: str):
    aSDKRuntimeKey = os.path.abspath(os.path.dirname(Path(__file__).resolve()) + r"/sdk_runtime_key.lic")
    aMTKRuntimeKey = os.path.abspath(os.path.dirname(Path(__file__).resolve()) + r"/mtk_runtime_key.lic")
    if not cadex.LicenseManager.CADExLicense_ActivateRuntimeKeyFromAbsolutePath(aSDKRuntimeKey) or not cadex.LicenseManager.CADExLicense_ActivateRuntimeKeyFromAbsolutePath(aMTKRuntimeKey):
        print("Failed to activate CAD Exchanger license.")
        return 1

    aModel = cadex.ModelData_Model()
    aReader = cadex.ModelData_ModelReader()

    # Reading the file
    if not aReader.Read(cadex.Base_UTF16String(theSource), aModel):
        print("Failed to open and convert the file " + theSource)
        return 1

    aPartVec = list()
    aPartCollector = PartCollector(aPartVec)
    aVisitor = cadex.ModelData_SceneGraphElementUniqueVisitor(aPartCollector)
    aModel.AcceptElementVisitor(aVisitor)

    aPartIndex = 0
    if aPartIndex >= aPartVec.__sizeof__():
        print("Part #", aPartIndex, " was not found.", sep="")
        return 1

    aPart = aPartVec[aPartIndex]
    anUnfoldedShell = Unfold(aPart)

    # Save unfolded shape as 2D DXF drawing
    if WriteToDrawing(anUnfoldedShell, theDrawingPath):
        aPartName = ""
        if aPart.Name().IsEmpty():
            aPartName = "noname"
        else:
            aPartName = aPart.Name()
        print("A drawing of the unfolded view of the part #", aPartIndex, " [\"", aPartName, "\"] has been saved to ", theDrawingPath, sep="")
    else:
        print("Failed to save drawing of the unfolded view to ", theDrawingPath, sep="")
        return 1
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: <input_file> <output_file>, where:")
        print("    <input_file>  is a name of the file to be read")
        print("    <output_file> is a name of the DXF file with drawing to be written")
        sys.exit()

    aSource = os.path.abspath(sys.argv[1])
    aRes = os.path.abspath(sys.argv[2])

    sys.exit(main(aSource, aRes))