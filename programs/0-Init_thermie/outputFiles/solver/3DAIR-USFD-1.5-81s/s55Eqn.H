fvScalarMatrix s55Eqn
(
fvm::ddt(s55)
+ fvm::div(phi, s55)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s55)
==
fvOptions(s55)
);

s55Eqn.relax();
fvOptions.constrain(s55Eqn);
s55Eqn.solve();
fvOptions.correct(s55);
