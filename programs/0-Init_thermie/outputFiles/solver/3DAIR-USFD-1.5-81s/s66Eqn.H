fvScalarMatrix s66Eqn
(
fvm::ddt(s66)
+ fvm::div(phi, s66)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s66)
==
fvOptions(s66)
);

s66Eqn.relax();
fvOptions.constrain(s66Eqn);
s66Eqn.solve();
fvOptions.correct(s66);
