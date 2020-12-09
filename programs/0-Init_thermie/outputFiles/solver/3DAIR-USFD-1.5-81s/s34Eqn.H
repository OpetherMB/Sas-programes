fvScalarMatrix s34Eqn
(
fvm::ddt(s34)
+ fvm::div(phi, s34)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s34)
==
fvOptions(s34)
);

s34Eqn.relax();
fvOptions.constrain(s34Eqn);
s34Eqn.solve();
fvOptions.correct(s34);
