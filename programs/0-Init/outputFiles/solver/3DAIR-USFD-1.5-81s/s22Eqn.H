fvScalarMatrix s22Eqn
(
fvm::ddt(s22)
+ fvm::div(phi, s22)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s22)
==
fvOptions(s22)
);

s22Eqn.relax();
fvOptions.constrain(s22Eqn);
s22Eqn.solve();
fvOptions.correct(s22);
