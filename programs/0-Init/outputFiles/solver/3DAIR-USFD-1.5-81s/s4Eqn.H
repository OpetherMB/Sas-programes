fvScalarMatrix s4Eqn
(
fvm::ddt(s4)
+ fvm::div(phi, s4)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s4)
==
fvOptions(s4)
);

s4Eqn.relax();
fvOptions.constrain(s4Eqn);
s4Eqn.solve();
fvOptions.correct(s4);
