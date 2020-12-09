fvScalarMatrix s72Eqn
(
fvm::ddt(s72)
+ fvm::div(phi, s72)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s72)
==
fvOptions(s72)
);

s72Eqn.relax();
fvOptions.constrain(s72Eqn);
s72Eqn.solve();
fvOptions.correct(s72);
