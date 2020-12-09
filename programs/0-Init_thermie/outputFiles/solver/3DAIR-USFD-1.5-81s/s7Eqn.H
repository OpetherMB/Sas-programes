fvScalarMatrix s7Eqn
(
fvm::ddt(s7)
+ fvm::div(phi, s7)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s7)
==
fvOptions(s7)
);

s7Eqn.relax();
fvOptions.constrain(s7Eqn);
s7Eqn.solve();
fvOptions.correct(s7);
