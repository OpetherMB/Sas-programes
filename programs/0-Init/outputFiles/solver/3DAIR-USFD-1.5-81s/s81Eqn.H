fvScalarMatrix s81Eqn
(
fvm::ddt(s81)
+ fvm::div(phi, s81)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s81)
==
fvOptions(s81)
);

s81Eqn.relax();
fvOptions.constrain(s81Eqn);
s81Eqn.solve();
fvOptions.correct(s81);
