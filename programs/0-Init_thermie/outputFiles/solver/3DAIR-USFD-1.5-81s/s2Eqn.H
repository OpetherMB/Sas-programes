fvScalarMatrix s2Eqn
(
fvm::ddt(s2)
+ fvm::div(phi, s2)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s2)
==
fvOptions(s2)
);

s2Eqn.relax();
fvOptions.constrain(s2Eqn);
s2Eqn.solve();
fvOptions.correct(s2);
