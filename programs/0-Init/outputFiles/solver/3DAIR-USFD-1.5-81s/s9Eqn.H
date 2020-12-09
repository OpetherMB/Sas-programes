fvScalarMatrix s9Eqn
(
fvm::ddt(s9)
+ fvm::div(phi, s9)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s9)
==
fvOptions(s9)
);

s9Eqn.relax();
fvOptions.constrain(s9Eqn);
s9Eqn.solve();
fvOptions.correct(s9);
