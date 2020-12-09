fvScalarMatrix s25Eqn
(
fvm::ddt(s25)
+ fvm::div(phi, s25)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s25)
==
fvOptions(s25)
);

s25Eqn.relax();
fvOptions.constrain(s25Eqn);
s25Eqn.solve();
fvOptions.correct(s25);
