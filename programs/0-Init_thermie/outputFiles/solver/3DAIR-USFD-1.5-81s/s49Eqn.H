fvScalarMatrix s49Eqn
(
fvm::ddt(s49)
+ fvm::div(phi, s49)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s49)
==
fvOptions(s49)
);

s49Eqn.relax();
fvOptions.constrain(s49Eqn);
s49Eqn.solve();
fvOptions.correct(s49);
