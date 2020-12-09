fvScalarMatrix s73Eqn
(
fvm::ddt(s73)
+ fvm::div(phi, s73)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s73)
==
fvOptions(s73)
);

s73Eqn.relax();
fvOptions.constrain(s73Eqn);
s73Eqn.solve();
fvOptions.correct(s73);
