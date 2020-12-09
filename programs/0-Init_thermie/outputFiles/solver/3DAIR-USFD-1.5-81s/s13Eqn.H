fvScalarMatrix s13Eqn
(
fvm::ddt(s13)
+ fvm::div(phi, s13)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s13)
==
fvOptions(s13)
);

s13Eqn.relax();
fvOptions.constrain(s13Eqn);
s13Eqn.solve();
fvOptions.correct(s13);
