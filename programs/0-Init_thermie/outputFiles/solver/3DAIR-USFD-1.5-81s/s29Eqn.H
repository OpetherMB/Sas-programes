fvScalarMatrix s29Eqn
(
fvm::ddt(s29)
+ fvm::div(phi, s29)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s29)
==
fvOptions(s29)
);

s29Eqn.relax();
fvOptions.constrain(s29Eqn);
s29Eqn.solve();
fvOptions.correct(s29);
