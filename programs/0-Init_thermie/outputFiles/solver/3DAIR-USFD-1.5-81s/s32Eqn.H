fvScalarMatrix s32Eqn
(
fvm::ddt(s32)
+ fvm::div(phi, s32)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s32)
==
fvOptions(s32)
);

s32Eqn.relax();
fvOptions.constrain(s32Eqn);
s32Eqn.solve();
fvOptions.correct(s32);
