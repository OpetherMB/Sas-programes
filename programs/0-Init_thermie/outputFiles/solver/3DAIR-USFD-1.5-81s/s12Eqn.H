fvScalarMatrix s12Eqn
(
fvm::ddt(s12)
+ fvm::div(phi, s12)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s12)
==
fvOptions(s12)
);

s12Eqn.relax();
fvOptions.constrain(s12Eqn);
s12Eqn.solve();
fvOptions.correct(s12);
