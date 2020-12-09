fvScalarMatrix s19Eqn
(
fvm::ddt(s19)
+ fvm::div(phi, s19)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s19)
==
fvOptions(s19)
);

s19Eqn.relax();
fvOptions.constrain(s19Eqn);
s19Eqn.solve();
fvOptions.correct(s19);
