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
import manufacturingtoolkit.CadExMTK  as mtk

sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../"))
sys.path.append(os.path.abspath(os.path.dirname(Path(__file__).resolve()) + "/../../helpers/"))

import featuregroup
import shapeprocessor

def SmallDistanceIssueName(theIssue: mtk.DFMSheetMetal_SmallDistanceBetweenFeaturesIssue):
    if mtk.DFMSheetMetal_SmallDistanceBetweenHoleAndBendIssue.CompareType(theIssue):
        return "Small Distance Between Hole And Bend Issue(s)"
    elif mtk.DFMSheetMetal_SmallDistanceBetweenHoleAndCutoutIssue.CompareType(theIssue):
        return "Small Distance Between Hole And Cutout Issue(s)"
    elif mtk.DFMSheetMetal_SmallDistanceBetweenHoleAndEdgeIssue.CompareType(theIssue):
        return "Small Distance Between Hole And Edge Issue(s)"
    elif mtk.DFMSheetMetal_SmallDistanceBetweenHoleAndNotchIssue.CompareType(theIssue):
        return "Small Distance Between Hole And Notch Issue(s)"
    elif mtk.DFMSheetMetal_SmallDistanceBetweenHolesIssue.CompareType(theIssue):
        return "Small Distance Between Holes Issue(s)"
    elif mtk.DFMSheetMetal_SmallDistanceBetweenNotchAndBendIssue.CompareType(theIssue):
        return "Small Distance Between Notch And Bend Issue(s)"
    elif mtk.DFMSheetMetal_SmallDistanceBetweenNotchesIssue.CompareType(theIssue):
        return "Small Distance Between Notches Issue(s)"
    elif mtk.DFMSheetMetal_SmallDistanceBetweenTabsIssue.CompareType(theIssue):
        return "Small Distance Between Tabs Issue(s)"
    return "Small Distance Between Feature(s)"

def PrintFeatureParameters(theIssue: mtk.MTKBase_Feature):
    if mtk.DFMSheetMetal_SmallRadiusBendIssue.CompareType(theIssue):
        aSRBIssue = mtk.DFMSheetMetal_SmallRadiusBendIssue.Cast(theIssue)
        featuregroup.FeatureGroupManager.PrintFeatureParameter("expected min radius", aSRBIssue.ExpectedMinRadius(), "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter("actual radius",       aSRBIssue.ActualRadius(),      "mm")
    elif mtk.DFMSheetMetal_SmallDiameterHoleIssue.CompareType(theIssue):
        aSDHIssue = mtk.DFMSheetMetal_SmallDiameterHoleIssue.Cast(theIssue)
        featuregroup.FeatureGroupManager.PrintFeatureParameter("expected min diameter", aSDHIssue.ExpectedMinDiameter(), "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter("actual diameter",       aSDHIssue.ActualDiameter(),      "mm")
    elif mtk.DFMSheetMetal_SmallDistanceBetweenFeaturesIssue.CompareType(theIssue):
        aSDBFIssue = mtk.DFMSheetMetal_SmallDistanceBetweenFeaturesIssue.Cast(theIssue)
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "expected min distance", aSDBFIssue.ExpectedMinDistanceBetweenFeatures(), "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "actual distance",       aSDBFIssue.ActualDistanceBetweenFeatures(),      "mm")
    elif mtk.DFMSheetMetal_FlatPatternInterferenceIssue.CompareType(theIssue):
        pass #no parameters
    elif mtk.DFMSheetMetal_IrregularSizeBendReliefIssue.CompareType(theIssue):
        aISBRIssue = mtk.DFMSheetMetal_IrregularSizeBendReliefIssue.Cast(theIssue)
        anExpectedRelief = aISBRIssue.ExpectedMinBendRelief()
        aFirstActualRelief = aISBRIssue.FirstActualRelief()
        aSecondActualRelief = aISBRIssue.SecondActualRelief()

        featuregroup.FeatureGroupManager.PrintFeatureParameter (
            "expected min relief size (LxW)",
            featuregroup.Pair (anExpectedRelief.Length(), anExpectedRelief.Width()),
            "mm")
        if (not aFirstActualRelief.IsNull()) and (not aSecondActualRelief.IsNull()):
            featuregroup.FeatureGroupManager.PrintFeatureParameter (
                "first actual relief size (LxW)",
                featuregroup.Pair(aFirstActualRelief.Length(), aFirstActualRelief.Width()),
                "mm")
            featuregroup.FeatureGroupManager.PrintFeatureParameter (
                "second actual relief size (LxW)",
                featuregroup.Pair(aSecondActualRelief.Length(), aSecondActualRelief.Width()),
                "mm")
        elif aFirstActualRelief.IsNull():
            featuregroup.FeatureGroupManager.PrintFeatureParameter (
                "actual relief size (LxW)",
                featuregroup.Pair(aSecondActualRelief.Length(), aSecondActualRelief.Width()),
                "mm")
        else:
            featuregroup.FeatureGroupManager.PrintFeatureParameter (
                "actual relief size (LxW)",
                featuregroup.Pair(aFirstActualRelief.Length(), aFirstActualRelief.Width()),
                "mm")
    elif mtk.DFMSheetMetal_LargeDepthBeadIssue.CompareType(theIssue):
        aLDBIssue = mtk.DFMSheetMetal_LargeDepthBeadIssue.Cast(theIssue)
        featuregroup.FeatureGroupManager.PrintFeatureParameter("expected max depth", aLDBIssue.ExpectedMaxDepth(), "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter("actual depth",       aLDBIssue.ActualDepth(),      "mm")
    elif mtk.DFMSheetMetal_InconsistentRadiusBendIssue.CompareType(theIssue):
        aIRBIssue = mtk.DFMSheetMetal_InconsistentRadiusBendIssue.Cast(theIssue)
        featuregroup.FeatureGroupManager.PrintFeatureParameter("expected max radius", aIRBIssue.ExpectedRadius(), "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter("actual radius",       aIRBIssue.ActualRadius(),   "mm")
    elif mtk.DFMSheetMetal_SmallLengthFlangeIssue.CompareType(theIssue):
        aSLFIssue = mtk.DFMSheetMetal_SmallLengthFlangeIssue.Cast(theIssue)
        featuregroup.FeatureGroupManager.PrintFeatureParameter("expected min length", aSLFIssue.ExpectedMinLength(), "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter("actual length",       aSLFIssue.ActualLength(),      "mm")
    elif mtk.DFMSheetMetal_IrregularSizeNotchIssue.CompareType(theIssue):
        aISNIssue = mtk.DFMSheetMetal_IrregularSizeNotchIssue.Cast(theIssue)
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "expected size (LxW)",
            featuregroup.Pair(aISNIssue.ExpectedLength(), aISNIssue.ExpectedWidth()),
            "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "actual size (LxW)",
            featuregroup.Pair(aISNIssue.ActualLength(), aISNIssue.ActualWidth()),
            "mm")
    elif mtk.DFMSheetMetal_IrregularSizeTabIssue.CompareType(theIssue):
        aISTIssue = mtk.DFMSheetMetal_IrregularSizeTabIssue.Cast(theIssue)
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "expected size (LxW)",
            featuregroup.Pair(aISTIssue.ExpectedLength(), aISTIssue.ExpectedWidth()),
            "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "actual size (LxW)",
            featuregroup.Pair(aISTIssue.ActualLength(), aISTIssue.ActualWidth()),
            "mm")
    elif mtk.DFMSheetMetal_NonStandardSheetThicknessIssue.CompareType(theIssue):
        aNSSTIssue = mtk.DFMSheetMetal_NonStandardSheetThicknessIssue.Cast(theIssue)
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "nearest standard sheet thickness", aNSSTIssue.NearestStandardSheetThickness(), "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "actual sheet thickness",           aNSSTIssue.ActualSheetThickness(),          "mm")
    elif mtk.DFMSheetMetal_NonStandardSheetSizeIssue.CompareType(theIssue):
        aNSSSIssue = mtk.DFMSheetMetal_NonStandardSheetSizeIssue.Cast(theIssue)
        aNearestStandardSize = aNSSSIssue.NearestStandardSheetSize()
        anActualSize = aNSSSIssue.ActualSheetSize()
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "nearest standard sheet size (LxW)",
            featuregroup.Pair(aNearestStandardSize.Length(), aNearestStandardSize.Width()),
            "mm")
        featuregroup.FeatureGroupManager.PrintFeatureParameter(
            "actual sheet size (LxW)",
            featuregroup.Pair(anActualSize.Length(), anActualSize.Width()),
            "mm")

def PrintIssues(theIssueList: mtk.MTKBase_FeatureList):
    aManager = featuregroup.FeatureGroupManager()

    #group by parameters to provide more compact information about features
    for anIssue in theIssueList:
        if mtk.DFMSheetMetal_SmallRadiusBendIssue.CompareType(anIssue):
            aManager.AddFeature("Small Radius Bend Issue(s)", "Bend(s)", True, anIssue)
        elif mtk.DFMSheetMetal_SmallDiameterHoleIssue.CompareType(anIssue):
            aManager.AddFeature("Small Diameter Hole Issue(s)", "Hole(s)", True, anIssue)
        elif mtk.DFMSheetMetal_FlatPatternInterferenceIssue.CompareType(anIssue):
            aManager.AddFeature("Flat Pattern Interference Issue(s)", "", False, anIssue)
        elif mtk.DFMSheetMetal_IrregularSizeBendReliefIssue.CompareType(anIssue):
            aManager.AddFeature("Irregular Size Bend Relief Issue(s)", "Bend(s)", True, anIssue)
        elif mtk.DFMSheetMetal_LargeDepthBeadIssue.CompareType(anIssue):
            aManager.AddFeature("Large Depth Bead Issue(s)", "Bead(s)", True, anIssue)
        elif mtk.DFMSheetMetal_InconsistentRadiusBendIssue.CompareType(anIssue):
            aManager.AddFeature("Inconsistent Radius Bend Issue(s)", "Bend(s)", True, anIssue)
        elif mtk.DFMSheetMetal_SmallLengthFlangeIssue.CompareType(anIssue):
            aManager.AddFeature("Small Length Flange Issue(s)", "Flange(s)", True, anIssue)
        elif mtk.DFMSheetMetal_IrregularSizeNotchIssue.CompareType(anIssue):
            aManager.AddFeature("Irregular Size Notch Issue(s)", "Notch(s)", True, anIssue)
        elif mtk.DFMSheetMetal_IrregularSizeTabIssue.CompareType(anIssue):
            aManager.AddFeature("Irregular Size Tab Issue(s)", "Tab(s)", True, anIssue)
        elif mtk.DFMSheetMetal_SmallDistanceBetweenFeaturesIssue.CompareType(anIssue):
            aSDBFIssue = mtk.DFMSheetMetal_SmallDistanceBetweenFeaturesIssue.Cast(anIssue)
            aManager.AddFeature(SmallDistanceIssueName (aSDBFIssue), "Distance(s)", True, anIssue)
        elif mtk.DFMSheetMetal_NonStandardSheetThicknessIssue.CompareType(anIssue):
            aManager.AddFeature("Non Standard Sheet Thickness Issue(s)", "Sheet Thickness(s)", True, anIssue)
        elif mtk.DFMSheetMetal_NonStandardSheetSizeIssue.CompareType(anIssue):
            aManager.AddFeature("Non Standard Sheet Size Issue(s)", "Sheet Size(s)", True, anIssue)

    aManager.Print ("issues", PrintFeatureParameters)

# Compute approximate thickness value, which can be used as the input thickness value for DFMSheetMetal_Analyzer.
def CalculateInitialThicknessValue(theShape: cadex.ModelData_Shape):
    aVolume = cadex.ModelAlgo_ValidationProperty_ComputeVolume(theShape)
    aSurfaceArea = cadex.ModelAlgo_ValidationProperty_ComputeSurfaceArea(theShape)
    aThickness = aVolume / (aSurfaceArea / 2.0)
    return aThickness

class PartProcessor(shapeprocessor.ShapeProcessor):
    def __init__(self):
        super().__init__()
        self.myAnalyzer = mtk.DFMSheetMetal_Analyzer()

    def ProcessSolid(self, theSolid: cadex.ModelData_Solid):
        aThickness = CalculateInitialThicknessValue(theSolid)
        anIssueList = self.myAnalyzer.Perform(theSolid, aThickness)
        PrintIssues(anIssueList)

    def ProcessShell(self, theShell: cadex.ModelData_Shell):
        anIssueList = self.myAnalyzer.Perform(theShell)
        PrintIssues(anIssueList)

def main(theSource: str):
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

    print("Model: ", aModel.Name(), "\n", sep="")

    # Processing
    aPartProcessor = PartProcessor()
    aVisitor = cadex.ModelData_SceneGraphElementUniqueVisitor(aPartProcessor)
    aModel.AcceptElementVisitor(aVisitor)

    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print( "Usage: <input_file>, where:")
        print( "    <input_file>  is a name of the file to be read")
        sys.exit()

    aSource = os.path.abspath(sys.argv[1])

    sys.exit(main(aSource))