fvScalarMatrix s58Eqn
(
fvm::ddt(s58)
+ fvm::div(phi, s58)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s58)
==
fvOptions(s58)
);

s58Eqn.relax();
fvOptions.constrain(s58Eqn);
s58Eqn.solve();
fvOptions.correct(s58);
