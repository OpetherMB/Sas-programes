fvScalarMatrix s46Eqn
(
fvm::ddt(s46)
+ fvm::div(phi, s46)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s46)
==
fvOptions(s46)
);

s46Eqn.relax();
fvOptions.constrain(s46Eqn);
s46Eqn.solve();
fvOptions.correct(s46);
