fvScalarMatrix s75Eqn
(
fvm::ddt(s75)
+ fvm::div(phi, s75)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s75)
==
fvOptions(s75)
);

s75Eqn.relax();
fvOptions.constrain(s75Eqn);
s75Eqn.solve();
fvOptions.correct(s75);
