fvScalarMatrix s36Eqn
(
fvm::ddt(s36)
+ fvm::div(phi, s36)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s36)
==
fvOptions(s36)
);

s36Eqn.relax();
fvOptions.constrain(s36Eqn);
s36Eqn.solve();
fvOptions.correct(s36);
