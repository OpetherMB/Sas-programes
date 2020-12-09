fvScalarMatrix s74Eqn
(
fvm::ddt(s74)
+ fvm::div(phi, s74)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s74)
==
fvOptions(s74)
);

s74Eqn.relax();
fvOptions.constrain(s74Eqn);
s74Eqn.solve();
fvOptions.correct(s74);
