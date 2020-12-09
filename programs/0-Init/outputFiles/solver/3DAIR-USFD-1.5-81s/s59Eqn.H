fvScalarMatrix s59Eqn
(
fvm::ddt(s59)
+ fvm::div(phi, s59)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s59)
==
fvOptions(s59)
);

s59Eqn.relax();
fvOptions.constrain(s59Eqn);
s59Eqn.solve();
fvOptions.correct(s59);
