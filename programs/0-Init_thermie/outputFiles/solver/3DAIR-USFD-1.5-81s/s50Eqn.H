fvScalarMatrix s50Eqn
(
fvm::ddt(s50)
+ fvm::div(phi, s50)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s50)
==
fvOptions(s50)
);

s50Eqn.relax();
fvOptions.constrain(s50Eqn);
s50Eqn.solve();
fvOptions.correct(s50);
