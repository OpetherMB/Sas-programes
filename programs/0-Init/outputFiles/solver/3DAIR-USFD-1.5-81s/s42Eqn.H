fvScalarMatrix s42Eqn
(
fvm::ddt(s42)
+ fvm::div(phi, s42)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s42)
==
fvOptions(s42)
);

s42Eqn.relax();
fvOptions.constrain(s42Eqn);
s42Eqn.solve();
fvOptions.correct(s42);
