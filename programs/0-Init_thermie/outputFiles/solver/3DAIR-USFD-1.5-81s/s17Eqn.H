fvScalarMatrix s17Eqn
(
fvm::ddt(s17)
+ fvm::div(phi, s17)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s17)
==
fvOptions(s17)
);

s17Eqn.relax();
fvOptions.constrain(s17Eqn);
s17Eqn.solve();
fvOptions.correct(s17);
