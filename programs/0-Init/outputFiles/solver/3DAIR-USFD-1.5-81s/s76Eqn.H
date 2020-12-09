fvScalarMatrix s76Eqn
(
fvm::ddt(s76)
+ fvm::div(phi, s76)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s76)
==
fvOptions(s76)
);

s76Eqn.relax();
fvOptions.constrain(s76Eqn);
s76Eqn.solve();
fvOptions.correct(s76);
