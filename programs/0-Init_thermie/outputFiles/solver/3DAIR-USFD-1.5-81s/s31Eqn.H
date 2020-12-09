fvScalarMatrix s31Eqn
(
fvm::ddt(s31)
+ fvm::div(phi, s31)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s31)
==
fvOptions(s31)
);

s31Eqn.relax();
fvOptions.constrain(s31Eqn);
s31Eqn.solve();
fvOptions.correct(s31);
