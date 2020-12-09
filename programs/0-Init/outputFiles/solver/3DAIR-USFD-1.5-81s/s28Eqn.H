fvScalarMatrix s28Eqn
(
fvm::ddt(s28)
+ fvm::div(phi, s28)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s28)
==
fvOptions(s28)
);

s28Eqn.relax();
fvOptions.constrain(s28Eqn);
s28Eqn.solve();
fvOptions.correct(s28);
