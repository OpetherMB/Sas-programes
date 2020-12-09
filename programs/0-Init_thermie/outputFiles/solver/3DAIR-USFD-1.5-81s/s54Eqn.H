fvScalarMatrix s54Eqn
(
fvm::ddt(s54)
+ fvm::div(phi, s54)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s54)
==
fvOptions(s54)
);

s54Eqn.relax();
fvOptions.constrain(s54Eqn);
s54Eqn.solve();
fvOptions.correct(s54);
