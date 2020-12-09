fvScalarMatrix s62Eqn
(
fvm::ddt(s62)
+ fvm::div(phi, s62)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s62)
==
fvOptions(s62)
);

s62Eqn.relax();
fvOptions.constrain(s62Eqn);
s62Eqn.solve();
fvOptions.correct(s62);
