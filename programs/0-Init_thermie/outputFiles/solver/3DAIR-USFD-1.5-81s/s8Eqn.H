fvScalarMatrix s8Eqn
(
fvm::ddt(s8)
+ fvm::div(phi, s8)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s8)
==
fvOptions(s8)
);

s8Eqn.relax();
fvOptions.constrain(s8Eqn);
s8Eqn.solve();
fvOptions.correct(s8);
