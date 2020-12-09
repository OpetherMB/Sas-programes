fvScalarMatrix s80Eqn
(
fvm::ddt(s80)
+ fvm::div(phi, s80)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s80)
==
fvOptions(s80)
);

s80Eqn.relax();
fvOptions.constrain(s80Eqn);
s80Eqn.solve();
fvOptions.correct(s80);
