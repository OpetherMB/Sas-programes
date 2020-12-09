fvScalarMatrix s26Eqn
(
fvm::ddt(s26)
+ fvm::div(phi, s26)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s26)
==
fvOptions(s26)
);

s26Eqn.relax();
fvOptions.constrain(s26Eqn);
s26Eqn.solve();
fvOptions.correct(s26);
