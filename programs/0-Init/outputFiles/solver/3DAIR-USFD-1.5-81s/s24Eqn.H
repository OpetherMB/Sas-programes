fvScalarMatrix s24Eqn
(
fvm::ddt(s24)
+ fvm::div(phi, s24)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s24)
==
fvOptions(s24)
);

s24Eqn.relax();
fvOptions.constrain(s24Eqn);
s24Eqn.solve();
fvOptions.correct(s24);
