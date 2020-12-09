fvScalarMatrix s68Eqn
(
fvm::ddt(s68)
+ fvm::div(phi, s68)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s68)
==
fvOptions(s68)
);

s68Eqn.relax();
fvOptions.constrain(s68Eqn);
s68Eqn.solve();
fvOptions.correct(s68);
