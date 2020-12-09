fvScalarMatrix s51Eqn
(
fvm::ddt(s51)
+ fvm::div(phi, s51)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s51)
==
fvOptions(s51)
);

s51Eqn.relax();
fvOptions.constrain(s51Eqn);
s51Eqn.solve();
fvOptions.correct(s51);
