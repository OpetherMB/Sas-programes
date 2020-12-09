fvScalarMatrix s10Eqn
(
fvm::ddt(s10)
+ fvm::div(phi, s10)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s10)
==
fvOptions(s10)
);

s10Eqn.relax();
fvOptions.constrain(s10Eqn);
s10Eqn.solve();
fvOptions.correct(s10);
