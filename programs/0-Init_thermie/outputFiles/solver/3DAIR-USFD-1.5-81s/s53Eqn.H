fvScalarMatrix s53Eqn
(
fvm::ddt(s53)
+ fvm::div(phi, s53)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s53)
==
fvOptions(s53)
);

s53Eqn.relax();
fvOptions.constrain(s53Eqn);
s53Eqn.solve();
fvOptions.correct(s53);
