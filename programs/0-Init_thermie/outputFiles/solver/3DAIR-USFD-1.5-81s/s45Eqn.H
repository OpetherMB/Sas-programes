fvScalarMatrix s45Eqn
(
fvm::ddt(s45)
+ fvm::div(phi, s45)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s45)
==
fvOptions(s45)
);

s45Eqn.relax();
fvOptions.constrain(s45Eqn);
s45Eqn.solve();
fvOptions.correct(s45);
