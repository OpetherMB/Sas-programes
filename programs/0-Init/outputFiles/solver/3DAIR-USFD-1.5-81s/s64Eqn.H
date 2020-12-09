fvScalarMatrix s64Eqn
(
fvm::ddt(s64)
+ fvm::div(phi, s64)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s64)
==
fvOptions(s64)
);

s64Eqn.relax();
fvOptions.constrain(s64Eqn);
s64Eqn.solve();
fvOptions.correct(s64);
