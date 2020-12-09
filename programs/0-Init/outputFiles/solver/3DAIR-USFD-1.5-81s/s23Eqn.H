fvScalarMatrix s23Eqn
(
fvm::ddt(s23)
+ fvm::div(phi, s23)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s23)
==
fvOptions(s23)
);

s23Eqn.relax();
fvOptions.constrain(s23Eqn);
s23Eqn.solve();
fvOptions.correct(s23);
