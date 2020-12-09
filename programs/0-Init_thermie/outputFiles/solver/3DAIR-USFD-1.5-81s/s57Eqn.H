fvScalarMatrix s57Eqn
(
fvm::ddt(s57)
+ fvm::div(phi, s57)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s57)
==
fvOptions(s57)
);

s57Eqn.relax();
fvOptions.constrain(s57Eqn);
s57Eqn.solve();
fvOptions.correct(s57);
