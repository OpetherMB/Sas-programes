fvScalarMatrix s18Eqn
(
fvm::ddt(s18)
+ fvm::div(phi, s18)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s18)
==
fvOptions(s18)
);

s18Eqn.relax();
fvOptions.constrain(s18Eqn);
s18Eqn.solve();
fvOptions.correct(s18);
