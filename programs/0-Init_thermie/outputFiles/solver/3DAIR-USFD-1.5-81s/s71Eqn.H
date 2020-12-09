fvScalarMatrix s71Eqn
(
fvm::ddt(s71)
+ fvm::div(phi, s71)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s71)
==
fvOptions(s71)
);

s71Eqn.relax();
fvOptions.constrain(s71Eqn);
s71Eqn.solve();
fvOptions.correct(s71);
