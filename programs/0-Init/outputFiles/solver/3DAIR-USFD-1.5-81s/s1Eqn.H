fvScalarMatrix s1Eqn
(
fvm::ddt(s1)
+ fvm::div(phi, s1)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s1)
==
fvOptions(s1)
);

s1Eqn.relax();
fvOptions.constrain(s1Eqn);
s1Eqn.solve();
fvOptions.correct(s1);
