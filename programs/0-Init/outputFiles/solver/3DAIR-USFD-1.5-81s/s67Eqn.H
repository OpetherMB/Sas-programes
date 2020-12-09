fvScalarMatrix s67Eqn
(
fvm::ddt(s67)
+ fvm::div(phi, s67)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s67)
==
fvOptions(s67)
);

s67Eqn.relax();
fvOptions.constrain(s67Eqn);
s67Eqn.solve();
fvOptions.correct(s67);
