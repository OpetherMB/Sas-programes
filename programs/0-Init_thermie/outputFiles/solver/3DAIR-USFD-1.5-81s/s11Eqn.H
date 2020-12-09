fvScalarMatrix s11Eqn
(
fvm::ddt(s11)
+ fvm::div(phi, s11)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s11)
==
fvOptions(s11)
);

s11Eqn.relax();
fvOptions.constrain(s11Eqn);
s11Eqn.solve();
fvOptions.correct(s11);
