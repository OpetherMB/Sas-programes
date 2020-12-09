fvScalarMatrix s30Eqn
(
fvm::ddt(s30)
+ fvm::div(phi, s30)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s30)
==
fvOptions(s30)
);

s30Eqn.relax();
fvOptions.constrain(s30Eqn);
s30Eqn.solve();
fvOptions.correct(s30);
