fvScalarMatrix s41Eqn
(
fvm::ddt(s41)
+ fvm::div(phi, s41)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s41)
==
fvOptions(s41)
);

s41Eqn.relax();
fvOptions.constrain(s41Eqn);
s41Eqn.solve();
fvOptions.correct(s41);
