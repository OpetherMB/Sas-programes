fvScalarMatrix s63Eqn
(
fvm::ddt(s63)
+ fvm::div(phi, s63)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s63)
==
fvOptions(s63)
);

s63Eqn.relax();
fvOptions.constrain(s63Eqn);
s63Eqn.solve();
fvOptions.correct(s63);
