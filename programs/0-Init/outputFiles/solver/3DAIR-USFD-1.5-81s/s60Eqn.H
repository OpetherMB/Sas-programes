fvScalarMatrix s60Eqn
(
fvm::ddt(s60)
+ fvm::div(phi, s60)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s60)
==
fvOptions(s60)
);

s60Eqn.relax();
fvOptions.constrain(s60Eqn);
s60Eqn.solve();
fvOptions.correct(s60);
