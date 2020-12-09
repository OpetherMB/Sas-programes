fvScalarMatrix s61Eqn
(
fvm::ddt(s61)
+ fvm::div(phi, s61)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s61)
==
fvOptions(s61)
);

s61Eqn.relax();
fvOptions.constrain(s61Eqn);
s61Eqn.solve();
fvOptions.correct(s61);
