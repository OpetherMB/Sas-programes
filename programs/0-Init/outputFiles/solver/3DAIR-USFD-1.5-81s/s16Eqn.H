fvScalarMatrix s16Eqn
(
fvm::ddt(s16)
+ fvm::div(phi, s16)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s16)
==
fvOptions(s16)
);

s16Eqn.relax();
fvOptions.constrain(s16Eqn);
s16Eqn.solve();
fvOptions.correct(s16);
