fvScalarMatrix s44Eqn
(
fvm::ddt(s44)
+ fvm::div(phi, s44)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s44)
==
fvOptions(s44)
);

s44Eqn.relax();
fvOptions.constrain(s44Eqn);
s44Eqn.solve();
fvOptions.correct(s44);
