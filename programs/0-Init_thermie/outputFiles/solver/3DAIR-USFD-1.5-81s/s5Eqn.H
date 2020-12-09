fvScalarMatrix s5Eqn
(
fvm::ddt(s5)
+ fvm::div(phi, s5)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s5)
==
fvOptions(s5)
);

s5Eqn.relax();
fvOptions.constrain(s5Eqn);
s5Eqn.solve();
fvOptions.correct(s5);
