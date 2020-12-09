fvScalarMatrix s47Eqn
(
fvm::ddt(s47)
+ fvm::div(phi, s47)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s47)
==
fvOptions(s47)
);

s47Eqn.relax();
fvOptions.constrain(s47Eqn);
s47Eqn.solve();
fvOptions.correct(s47);
