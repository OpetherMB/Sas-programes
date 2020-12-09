fvScalarMatrix s77Eqn
(
fvm::ddt(s77)
+ fvm::div(phi, s77)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s77)
==
fvOptions(s77)
);

s77Eqn.relax();
fvOptions.constrain(s77Eqn);
s77Eqn.solve();
fvOptions.correct(s77);
