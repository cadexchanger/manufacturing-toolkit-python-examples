#!/usr/bin/env python3

# $Id$

# Copyright (C) 2008-2014, Roman Lygin. All rights reserved.
# Copyright (C) 2014-2023, CADEX. All rights reserved.

# This file is part of the CAD Exchanger software.

# You may use this file under the terms of the BSD license as follows:

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

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


import subprocess
import sys

from pathlib import Path
from os.path import abspath, dirname

from sheet_metal_analyzer import main

aPath = abspath(dirname(Path(__file__).resolve()))
aSource = aPath + "/../../models/Power_box_Chasis.STEP"

aPathToScript = aPath + r"/sheet_metal_analyzer.py"
import cadexchanger
aPathToLicensingTool = abspath(dirname(Path(cadexchanger.__file__).resolve()) + r"/bin/LicensingTool")
aSDKRet = subprocess.run([aPathToLicensingTool, aPathToScript, aPath + r"/../../cadex_license.lic", aPath + r"/sdk_runtime_key.lic"])
aMTKRet = subprocess.run([aPathToLicensingTool, aPathToScript, aPath + r"/../../mtk_license.lic", aPath + r"/mtk_runtime_key.lic"])

if aSDKRet.returncode == 0 and aMTKRet.returncode == 0:
    sys.exit(main(aSource))
else:
    sys.exit(aSDKRet.returncode or aMTKRet.returncode)
