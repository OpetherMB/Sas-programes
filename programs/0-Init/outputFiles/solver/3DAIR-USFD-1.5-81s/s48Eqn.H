fvScalarMatrix s48Eqn
(
fvm::ddt(s48)
+ fvm::div(phi, s48)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s48)
==
fvOptions(s48)
);

s48Eqn.relax();
fvOptions.constrain(s48Eqn);
s48Eqn.solve();
fvOptions.correct(s48);
