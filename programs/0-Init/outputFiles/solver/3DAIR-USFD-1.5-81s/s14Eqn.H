fvScalarMatrix s14Eqn
(
fvm::ddt(s14)
+ fvm::div(phi, s14)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s14)
==
fvOptions(s14)
);

s14Eqn.relax();
fvOptions.constrain(s14Eqn);
s14Eqn.solve();
fvOptions.correct(s14);
