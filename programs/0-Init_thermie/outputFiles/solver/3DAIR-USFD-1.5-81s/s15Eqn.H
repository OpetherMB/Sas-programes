fvScalarMatrix s15Eqn
(
fvm::ddt(s15)
+ fvm::div(phi, s15)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s15)
==
fvOptions(s15)
);

s15Eqn.relax();
fvOptions.constrain(s15Eqn);
s15Eqn.solve();
fvOptions.correct(s15);
