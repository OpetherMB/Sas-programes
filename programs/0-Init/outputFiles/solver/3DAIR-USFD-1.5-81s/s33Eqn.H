fvScalarMatrix s33Eqn
(
fvm::ddt(s33)
+ fvm::div(phi, s33)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s33)
==
fvOptions(s33)
);

s33Eqn.relax();
fvOptions.constrain(s33Eqn);
s33Eqn.solve();
fvOptions.correct(s33);
