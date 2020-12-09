fvScalarMatrix s65Eqn
(
fvm::ddt(s65)
+ fvm::div(phi, s65)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s65)
==
fvOptions(s65)
);

s65Eqn.relax();
fvOptions.constrain(s65Eqn);
s65Eqn.solve();
fvOptions.correct(s65);
