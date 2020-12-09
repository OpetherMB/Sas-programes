fvScalarMatrix s39Eqn
(
fvm::ddt(s39)
+ fvm::div(phi, s39)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s39)
==
fvOptions(s39)
);

s39Eqn.relax();
fvOptions.constrain(s39Eqn);
s39Eqn.solve();
fvOptions.correct(s39);
