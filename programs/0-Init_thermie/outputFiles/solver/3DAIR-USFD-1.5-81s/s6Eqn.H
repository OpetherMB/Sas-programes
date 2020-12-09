fvScalarMatrix s6Eqn
(
fvm::ddt(s6)
+ fvm::div(phi, s6)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s6)
==
fvOptions(s6)
);

s6Eqn.relax();
fvOptions.constrain(s6Eqn);
s6Eqn.solve();
fvOptions.correct(s6);
