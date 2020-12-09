fvScalarMatrix s35Eqn
(
fvm::ddt(s35)
+ fvm::div(phi, s35)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s35)
==
fvOptions(s35)
);

s35Eqn.relax();
fvOptions.constrain(s35Eqn);
s35Eqn.solve();
fvOptions.correct(s35);
