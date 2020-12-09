fvScalarMatrix s38Eqn
(
fvm::ddt(s38)
+ fvm::div(phi, s38)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s38)
==
fvOptions(s38)
);

s38Eqn.relax();
fvOptions.constrain(s38Eqn);
s38Eqn.solve();
fvOptions.correct(s38);
