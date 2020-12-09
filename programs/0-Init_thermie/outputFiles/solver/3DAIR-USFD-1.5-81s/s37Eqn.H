fvScalarMatrix s37Eqn
(
fvm::ddt(s37)
+ fvm::div(phi, s37)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s37)
==
fvOptions(s37)
);

s37Eqn.relax();
fvOptions.constrain(s37Eqn);
s37Eqn.solve();
fvOptions.correct(s37);
