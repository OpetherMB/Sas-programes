fvScalarMatrix s69Eqn
(
fvm::ddt(s69)
+ fvm::div(phi, s69)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s69)
==
fvOptions(s69)
);

s69Eqn.relax();
fvOptions.constrain(s69Eqn);
s69Eqn.solve();
fvOptions.correct(s69);
