fvScalarMatrix s40Eqn
(
fvm::ddt(s40)
+ fvm::div(phi, s40)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s40)
==
fvOptions(s40)
);

s40Eqn.relax();
fvOptions.constrain(s40Eqn);
s40Eqn.solve();
fvOptions.correct(s40);
