/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 2011-2016 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Application
    pimpleFoam

Description
    Large time-step transient solver for incompressible, turbulent flow, using
    the PIMPLE (merged PISO-SIMPLE) algorithm.

    Sub-models include:
    - turbulence modelling, i.e. laminar, RAS or LES
    - run-time selectable MRF and finite volume options, e.g. explicit porosity

\*---------------------------------------------------------------------------*/

#include "powerLawVelocityFvPatchVectorField.H"
#include "fvCFD.H"
#include "singlePhaseTransportModel.H"
#include "turbulentTransportModel.H"
#include "simpleControl.H"
#include "pimpleControl.H"
#include "fvOptions.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
    #include "postProcess.H"
    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"
    simpleControl simple(mesh);
    #include "createControl.H"
    #include "createTimeControls.H"
    #include "createFields.H"
    #include "createFvOptions.H"
    #include "initContinuityErrs.H"

    	turbulence->validate();


    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

    Info<< "\nStarting time loop\n" << endl;

    while (runTime.run())
    {
	Info << endl;
        #include "readTimeControls.H"
        #include "CourantNo.H"
        #include "setDeltaT.H"

        runTime++;

        Info<< "Time = " << runTime.timeName() << nl << endl;

        // --- Pressure-velocity PIMPLE corrector loop
        Info << "FLOW CALCULATION..." << endl;
	while (pimple.loop())
        {
            #include "UEqn.H"

            // --- Pressure corrector loop
            while (pimple.correct())
            {
                #include "pEqn.H"
            }

            if (pimple.turbCorr())
            {
                laminarTransport.correct();
                turbulence->correct();
            }

        }

	// --- Transport calculation with turbulent diffusion
	Info << endl << "TRANSPORT CALCULATION..." << endl;	
	while (simple.correctNonOrthogonal())
		{
			#include "s1Eqn.H"
			#include "s2Eqn.H"
			#include "s3Eqn.H"
			#include "s4Eqn.H"
			#include "s5Eqn.H"
			#include "s6Eqn.H"
			#include "s7Eqn.H"
			#include "s8Eqn.H"
			#include "s9Eqn.H"
			#include "s10Eqn.H"
			#include "s11Eqn.H"
			#include "s12Eqn.H"
			#include "s13Eqn.H"
			#include "s14Eqn.H"
			#include "s15Eqn.H"
			#include "s16Eqn.H"
			#include "s17Eqn.H"
			#include "s18Eqn.H"
			#include "s19Eqn.H"
			#include "s20Eqn.H"
			#include "s21Eqn.H"
			#include "s22Eqn.H"
			#include "s23Eqn.H"
			#include "s24Eqn.H"
			#include "s25Eqn.H"
			#include "s26Eqn.H"
			#include "s27Eqn.H"
			#include "s28Eqn.H"
			#include "s29Eqn.H"
			#include "s30Eqn.H"
			#include "s31Eqn.H"
			#include "s32Eqn.H"
			#include "s33Eqn.H"
			#include "s34Eqn.H"
			#include "s35Eqn.H"
			#include "s36Eqn.H"
			#include "s37Eqn.H"
			#include "s38Eqn.H"
			#include "s39Eqn.H"
			#include "s40Eqn.H"
			#include "s41Eqn.H"
			#include "s42Eqn.H"
			#include "s43Eqn.H"
			#include "s44Eqn.H"
			#include "s45Eqn.H"
			#include "s46Eqn.H"
			#include "s47Eqn.H"
			#include "s48Eqn.H"
			#include "s49Eqn.H"
			#include "s50Eqn.H"
			#include "s51Eqn.H"
			#include "s52Eqn.H"
			#include "s53Eqn.H"
			#include "s54Eqn.H"
			#include "s55Eqn.H"
			#include "s56Eqn.H"
			#include "s57Eqn.H"
			#include "s58Eqn.H"
			#include "s59Eqn.H"
			#include "s60Eqn.H"
			#include "s61Eqn.H"
			#include "s62Eqn.H"
			#include "s63Eqn.H"
			#include "s64Eqn.H"
			#include "s65Eqn.H"
			#include "s66Eqn.H"
			#include "s67Eqn.H"
			#include "s68Eqn.H"
			#include "s69Eqn.H"
			#include "s70Eqn.H"
			#include "s71Eqn.H"
			#include "s72Eqn.H"
			#include "s73Eqn.H"
			#include "s74Eqn.H"
			#include "s75Eqn.H"
			#include "s76Eqn.H"
			#include "s77Eqn.H"
			#include "s78Eqn.H"
			#include "s79Eqn.H"
			#include "s80Eqn.H"
			#include "s81Eqn.H"
		}



        runTime.write();

        Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
            << "  ClockTime = " << runTime.elapsedClockTime() << " s"
            << nl << endl;
    }

    Info<< "End\n" << endl;

    return 0;
}


// ************************************************************************* //
