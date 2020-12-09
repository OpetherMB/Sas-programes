fvScalarMatrix s27Eqn
(
fvm::ddt(s27)
+ fvm::div(phi, s27)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s27)
==
fvOptions(s27)
);

s27Eqn.relax();
fvOptions.constrain(s27Eqn);
s27Eqn.solve();
fvOptions.correct(s27);
